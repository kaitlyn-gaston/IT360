if __name__ == '__build__':
	raise Exception

import sys
try:
  from OpenGL.GLUT import *
  from OpenGL.GL import *
  from OpenGL.GLU import *
  from math import *
  import random
except:
  print ('''
ERROR: PyOpenGL not installed properly.
        ''')
  sys.exit()

x = 0.6
y = 0.4 
r = 0.1

def dist(mousex, mousey):
    global x,y,r
    return sqrt((mousex-x)**2 + (mousey-y)**2)

def display():
   global x,y,r
   # clear all pixels
   glClearColor(0.870, 0.905, 0.937, 0)
   glClear (GL_COLOR_BUFFER_BIT)

   drawCircle(r,x,y)
   # drawCircle(r,x,y)
   # don't wait!
   # start processing buffered OpenGL routines
   glFlush ()

#draws circles (black border first)
def drawCircle(r, x, y):
   glColor3f (0.0, 0.0, 0.0)
   glBegin(GL_POLYGON)      
   for i in range(32):
      cosx = (r+0.01) * cos(i*(2*pi)/32) + x
      siny  = (r+0.01) * sin(i*(2*pi)/32) + y
      glVertex2f(cosx,siny)
   glEnd()
   glColor3f (0.807, 0.0, 0.0)
   glBegin(GL_POLYGON)  
   for i in range(32):
      cosx = r * cos(i*(2*pi)/32) + x
      siny  = r * sin(i*(2*pi)/32) + y
      glVertex2f(cosx,siny)
   glEnd()

def keyboard(key, x, y):
   if key == b'q' or key == b'\x1b': # if key is 'q' or escape
      sys.exit(0)

def drag(mousex, mousey):
   global x, y, r
   projectX = (mousex/300)
   projectY = 1 - (mousey/300)
   if dist(projectX, projectY) <= r:
      x = projectX
      y = projectY
      drawCircle(r,x,y)

def init():
    # select clearing color
    glClearColor (0.0, 0.0, 0.0, 0.0)

    # initialize viewing values
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 1.0, 0.0, 1.0, -1.0, 1.0)
    
    glutIdleFunc(display)

glutInit(sys.argv)
glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
glutInitWindowSize(300, 300)
glutInitWindowPosition(100, 100)
glutCreateWindow("hello")
init()
glutDisplayFunc(display)
glutKeyboardFunc(keyboard)
# glutMouseFunc(mouse)
glutMotionFunc(drag)
glutMainLoop()