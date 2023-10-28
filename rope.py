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
except BaseException:
    print('''
ERROR: PyOpenGL not installed properly.
        ''')
    sys.exit()


screen_dimx = 550
screen_dimy = 550
screen_leftx = -15
screen_rightx = 15
screen_topy = -15
screen_bottomy = 15

time_delta = 1 / 64.
particle_radii = 0.3
Fextx = -0.2
dragged_particle = None
is_dragging = False
particle_distance = particle_radii * 2.5


class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = 0.0
        self.vy = 0.0
        self.px = x
        self.py = y
        self.inv_mass = 1.0


class Constraint:
    def __init__(self, id1, id2, distance):
        self.id1 = id1
        self.id2 = id2
        self.distance = distance
        self.stiffness = 0.1


class PointConstraint:
    def __init__(self, id1, x, y):
        self.id1 = id1
        self.x = x
        self.y = y


particles = [Particle(i * particle_radii * 2.1, 0.0) for i in range(15)]


point_constraints = [PointConstraint(0,
                                     0.0,
                                     0.0)]


distance_constraints = [
    Constraint(
        i,
        i + 1,
        particle_distance) for i in range(
            len(particles) - 1)]


def draw_rope():
    glBegin(GL_LINES)
    for i in range(len(particles) - 1):
        glVertex2f(particles[i].x, particles[i].y)
        glVertex2f(particles[i + 1].x, particles[i + 1].y)
    glEnd()


def draw_circle_outline(r, x, y):
    i = 0.0
    glLineWidth(3)
    glBegin(GL_LINE_LOOP)
    while i <= 360.0:
        glVertex2f(r * cos(PI * i / 180.0) + x,
                   r * sin(PI * i / 180.0) + y)
        i += 360.0 / 18.0
    glEnd()


def draw_arrow():
    global Fextx
    if Fextx > 0:
        x = -5
        y = 5
        glLineWidth(1)
        glBegin(GL_TRIANGLE_FAN)
        glVertex2f(x, y + 4 * particle_radii)
        glVertex2f(x, y - 4 * particle_radii)
        glVertex2f(x + 4 * particle_radii, y)
        glEnd()
        glBegin(GL_QUADS)
        glVertex2f(x, y + 2 * particle_radii)
        glVertex2f(x - 5 * particle_radii, y + 2 * particle_radii)
        glVertex2f(x - 5 * particle_radii, y - 2 * particle_radii)
        glVertex2f(x, y - 2 * particle_radii)
        glEnd()
    elif Fextx < 0:
        x = 5
        y = 5
        glLineWidth(1)
        glBegin(GL_TRIANGLE_FAN)
        glVertex2f(x, y + 4 * particle_radii)
        glVertex2f(x, y - 4 * particle_radii)
        glVertex2f(x - 4 * particle_radii, y)
        glEnd()
        glBegin(GL_QUADS)
        glVertex2f(x, y + 2 * particle_radii)
        glVertex2f(x + 5 * particle_radii, y + 2 * particle_radii)
        glVertex2f(x + 5 * particle_radii, y - 2 * particle_radii)
        glVertex2f(x, y - 2 * particle_radii)
        glEnd()


def draw_circle(r, x, y):
    i = 0.0
    glLineWidth(1)
    glBegin(GL_TRIANGLE_FAN)
    glVertex2f(x, y)
    while i <= 360.0:
        glVertex2f(r * cos(PI * i / 180.0) + x,
                   r * sin(PI * i / 180.0) + y)
        i += 360.0 / 18.0
    glEnd()


def drawParticles():
    global dragged_particle
    global particles
    glColor3f(1.0, 1.0, 1.0)
    for particle in particles:
        draw_circle(particle_radii, particle.x, particle.y)
    draw_rope()
    if dragged_particle is not None:
        glColor3f(1.0, 0.0, 0.0)
        draw_circle_outline(
            particle_radii,
            dragged_particle.x,
            dragged_particle.y)


def timer(value):
    global Fextx
    if Fextx == 0:
        Fextx = 0.2
    elif Fextx == 0.2:
        Fextx = -0.2
    elif Fextx == -0.2:
        Fextx = 0
    glutTimerFunc(3800, timer, 0)


def distance(x1, y1, x2, y2):
    return sqrt((x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1))


def point_constraint(particle1, x2, y2):
    global particles
    correction_x1 = 0.0
    correction_y1 = 0.0
    #TODO: Complete this code
    if particle1 == particles[0]:
        particle1.inv_mass = 0
        particle1.vx = 0
        particle1.vy = 0
    return (correction_x1, correction_y1)


def distance_constraint(particle1,
                        particle2,
                        constraint_distance):
    correction_x1 = 0.0
    correction_y1 = 0.0
    correction_x2 = 0.0
    correction_y2 = 0.0
    # TODO: Complete this code
    # Write your distance constraint code here
    dist = distance(particle1.x, particle1.y, particle2.x, particle2.y)
    result = dist-constraint_distance
    if result != 0:
        if abs(dist == 0):
            dist = 0.001
        change = result/dist
        correction_x1 = -(particle1.inv_mass/(particle1.inv_mass+particle2.inv_mass))*change*((particle1.x-particle2.x))
        correction_x2 = (particle2.inv_mass/(particle1.inv_mass+particle2.inv_mass))*change*((particle1.x-particle2.x))
        correction_y1 = -(particle1.inv_mass/(particle1.inv_mass+particle2.inv_mass))*change*((particle1.y-particle2.y))
        correction_y2 = (particle2.inv_mass/(particle1.inv_mass+particle2.inv_mass))*change*((particle1.y-particle2.y))
    return (correction_x1, correction_y1, correction_x2, correction_y2)


def pbd_main_loop():
    global particles, Fextx
    gravity = 9.8
    Fexty = 0.0
    for particle in particles:
        # apply external forces - line 5
        if particle != particles[0]:
            particle.vx += Fextx
            particle.vy += (Fexty + gravity) * time_delta
            # damp velocities - line 6
            particle.vx *= 0.99
            particle.vy *= 0.99
        # get initial projected positions - line 7
        particle.px = particle.x + particle.vx * time_delta
        particle.py = particle.y + particle.vy * time_delta

    # line 9
    i = 1
    while i < 4:
        #line 10
        for constraint in point_constraints:
            delta_x1, delta_y1 = point_constraint(particles[constraint.id1],
                                                  constraint.x, constraint.y)
            particles[constraint.id1].px += delta_x1
            particles[constraint.id1].py += delta_y1

        for constraint in distance_constraints:
            stiffness = 1 - (1 - constraint.stiffness)**(1 / i)
            delta_x1, delta_y1, delta_x2, delta_y2 = distance_constraint(
                particles[constraint.id1], particles[constraint.id2], constraint.distance)
            particles[constraint.id1].px += stiffness * delta_x1
            particles[constraint.id1].py += stiffness * delta_y1
            particles[constraint.id2].px += stiffness * delta_x2
            particles[constraint.id2].py += stiffness * delta_y2
        i += 1

    # line 12
    for particle in particles:
        # line 13
        particle.vx = (particle.px - particle.x) / time_delta
        particle.vy = (particle.py - particle.y) / time_delta
        # line 14
        particle.x = particle.px
        particle.y = particle.py
    glutPostRedisplay()


def display():
    glClear(GL_COLOR_BUFFER_BIT)
    drawParticles()
    draw_arrow()
    glFlush()


def particle_clicked(x, y):
    res = None
    for particle in particles:
        if distance(x, y, particle.x, particle.y) <= particle_radii:
            return particle
    return res


def translate_to_world_coords(screenx, screeny):
    x, y, _ = gluUnProject(screenx, screeny, 0)
    y = -y
    return (x, y)


def mouse(button, state, screenx, screeny):
    global dragged_particle, is_dragging
    x, y = translate_to_world_coords(screenx, screeny)
    if dragged_particle is not None:
        if state == 0:
            is_dragging = not is_dragging
            #dragged_particle.inv_mass = 1.0
        if state == 1 and not is_dragging:
            dragged_particle = None
    else:
        particle = particle_clicked(x, y)
        dragged_particle = particle
        if state == 0 and dragged_particle is not None:
            is_dragging = not is_dragging
            #dragged_particle.inv_mass = 1.0
        if state == 1 and not is_dragging:
            dragged_particle = None


def mousePassive(screenx, screeny):
    global dragged_particle, is_dragging
    x, y = translate_to_world_coords(screenx, screeny)
    if is_dragging:
        if dragged_particle is not None and dragged_particle.inv_mass == 1:
            dragged_particle.x = x
            dragged_particle.y = y
            dragged_particle.inv_mass = 0


def keyboard(key, x, y):
    if key:
        sys.exit(0)


def init():
    glClearColor(0.0, 0.0, 0.0, 0.0)
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
glutCreateWindow("Rope Simulation")
init()
glutDisplayFunc(display)
glutKeyboardFunc(keyboard)
glutMouseFunc(mouse)
glutPassiveMotionFunc(mousePassive)
timer(0)
glutIdleFunc(pbd_main_loop)
glutMainLoop()
