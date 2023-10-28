#!/usr/bin/python

# This is statement is required by the build system to query build info
if __name__ == '__build__':
	raise Exception

import sys
import math
from math import cos as cos
from math import sin as sin
from math import pi as PI
from math import sqrt as sqrt

try:
  from OpenGL.GLUT import *
  from OpenGL.GL import *
  from OpenGL.GLU import *
except:
  print ('''
ERROR: PyOpenGL not installed properly.
        ''')
  sys.exit()


screen_dimx = 550
screen_dimy = 550
screen_leftx = -15
screen_rightx = 15
screen_topy = -15
screen_bottomy = 15

time_delta = 1/64.
particle_radii = 1.3
dragged_particle = None
is_dragging = False
particle_distance = particle_radii * 2.5

class Particle:
	def __init__(self,x,y):
		self.x=x
		self.y=y
		self.vx=0.0
		self.vy=0.0
		self.px=x
		self.py=y
		self.r = particle_radii
		self.inv_mass = 1.0

class Constraint:
	def __init__(self,id1,id2,distance):
		self.id1=id1
		self.id2=id2
		self.distance=distance
		self.stiffness = 0.1

class PointConstraint:
	def __init__(self,id1,x,y):
		self.id1=id1
		self.x=x
		self.y=y

particles = [Particle(-10*particle_radii + i*particle_radii * 2.2, 0.0) for i in range(10)]


def draw_circle_outline(r,x,y):
	i = 0.0
	glLineWidth(3)
	glBegin(GL_LINE_LOOP)
	while i<=360.0:
		glVertex2f(r*cos(PI*i/180.0) + x,
		           r*sin(PI*i/180.0) + y)
		i+=360.0/18.0
	glEnd()

def draw_circle(r,x,y):
	i = 0.0
	glLineWidth(1)
	glBegin(GL_TRIANGLE_FAN)
	glVertex2f(x,y)
	while i<=360.0:
		glVertex2f(r*cos(PI*i/180.0) + x,
		           r*sin(PI*i/180.0) + y)
		i+=360.0/18.0
	glEnd()

def drawParticles():
	global dragged_particle
	global particles
	glColor3f (0.125, 0.125, 0.125)
	for particle in particles:
		draw_circle(particle_radii, particle.x,particle.y)
	if dragged_particle is not None:
		glColor3f (1.0, 0.0, 0.0)
		draw_circle_outline(particle_radii, dragged_particle.x,dragged_particle.y)

def distance(x1,y1,x2,y2):
	return sqrt( (x2-x1)*(x2-x1) + (y2-y1)*(y2-y1))


def point_constraint(particle1, x2, y2):
	correction_x1 = 0.0
	correction_y1 = 0.0
	px1 = particle1.px #predicted x position of particle 1
	py1 = particle1.py #predicted y position of particle 1
	coef1 = - 1.0
	coef2 = 0.0
	currdist = distance(px1,py1,x2,y2)
	if currdist > 0.001:
		dist_diff = currdist # - constraint_distance
		coef = dist_diff / currdist
		correction_x1 = coef1 * coef * (px1-x2)
		correction_y1 = coef1 * coef * (py1-y2)
	return (correction_x1,correction_y1)


def collision_constraint(particle1,
                         particle2):
    correction_x1 = 0.0
    correction_y1 = 0.0
    correction_x2 = 0.0
    correction_y2 = 0.0
    # TODO: Complete this code
    # Write your distance constraint code here
    dist = distance(particle1.x, particle1.y, particle2.x, particle2.y)
    result = dist-(particle2.r*2)
    if result <= 0:
        if abs(dist == 0):
            dist = 0.01
        change = result/dist
        correction_x1 = -(particle1.inv_mass/(particle1.inv_mass+particle2.inv_mass))*change*((particle1.x-particle2.x))
        correction_x2 = (particle2.inv_mass/(particle1.inv_mass+particle2.inv_mass))*change*((particle1.x-particle2.x))
        correction_y1 = -(particle1.inv_mass/(particle1.inv_mass+particle2.inv_mass))*change*((particle1.y-particle2.y))
        correction_y2 = (particle2.inv_mass/(particle1.inv_mass+particle2.inv_mass))*change*((particle1.y-particle2.y))
    return (correction_x1, correction_y1, correction_x2, correction_y2)

def resolve_collision_constraints():
	for p1 in particles:
		for p2 in particles:
			delta_x1, delta_y1, delta_x2, delta_y2 = collision_constraint(p1,p2)
			collision_constraint(p1,p2)
			p1.px +=  delta_x1
			p1.py +=  delta_y1
			p2.px +=  delta_x2
			p2.py +=  delta_y2

def pbd_main_loop():
	global particles
	gravity = 0.0
	for particle in particles:
        # apply external forces - line 5
		particle.vx += 0.0
		particle.vy += (gravity ) * time_delta
        # damp velocities - line 6
		particle.vx *= 0.8
		particle.vy *= 0.8
        # get initial projected positions - line 7
		particle.px = particle.x + particle.vx * time_delta
		particle.py = particle.y + particle.vy * time_delta
    #line 8
	resolve_collision_constraints()
	for particle in particles:
        # line 13
		particle.vx = (particle.px - particle.x) / time_delta
		particle.vy = (particle.py - particle.y) / time_delta
        # line 14
		particle.x = particle.px
		particle.y = particle.py
	glutPostRedisplay()

def display():
   glClear (GL_COLOR_BUFFER_BIT)
   drawParticles()
   glFlush ();

def particle_clicked(x,y):
	res = None
	for particle in particles:
		if distance(x,y, particle.x,particle.y) <= particle_radii:
			return particle
	return res


def translate_to_world_coords(screenx,screeny):
	x, y, _  = gluUnProject(screenx, screeny,0)
	y = -y
	return (x,y)


def mouse(button, state, screenx, screeny):
	global dragged_particle,is_dragging
	x,y = translate_to_world_coords(screenx,screeny)
	if dragged_particle is not None:
		if state == 0:
			is_dragging = not is_dragging
			dragged_particle.inv_mass = 1.0
		if state == 1 and not is_dragging:
			dragged_particle = None
	else:
		particle = particle_clicked(x,y)
		dragged_particle = particle
		if state == 0 and dragged_particle is not None:
			is_dragging = not is_dragging
			dragged_particle.inv_mass = 1.0
		if state == 1 and not is_dragging:
			dragged_particle = None

def mousePassive(screenx,screeny):
	global dragged_particle, is_dragging
	x,y = translate_to_world_coords(screenx,screeny)
	if is_dragging:
		if dragged_particle is not None:
			dragged_particle.x = x
			dragged_particle.y = y

def keyboard(key, x, y):
    if key:
        sys.exit(0)


def init():
   glClearColor (0.972, 0.972, 0.972, 0.0)
   glMatrixMode(GL_MODELVIEW)
   glLoadIdentity()
   glMatrixMode(GL_PROJECTION)
   glLoadIdentity()
   gluOrtho2D(screen_leftx,
              screen_rightx,
			  screen_bottomy,
			  screen_topy)

glutInit(sys.argv)
glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
glutInitWindowSize(screen_dimx, screen_dimy)
glutInitWindowPosition(100, 100)
glutCreateWindow("Collision Constraint")
init()
glutDisplayFunc(display)
glutKeyboardFunc(keyboard)
glutMouseFunc(mouse)
glutPassiveMotionFunc(mousePassive)
glutIdleFunc(pbd_main_loop)
glutMainLoop()
