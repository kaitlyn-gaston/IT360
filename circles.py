if __name__ == '__build__':
	raise Exception

import sys
try:
  from OpenGL.GLUT import *
  from OpenGL.GL import *
  from OpenGL.GLU import *
  from math import *
except:
  print ('''
ERROR: PyOpenGL not installed properly.
        ''')
  sys.exit()


def display():
   # clear all pixels
   glClearColor(0.870, 0.905, 0.937, 0)
   glClear (GL_COLOR_BUFFER_BIT)
   
   drawCircle(1,2,2)
   drawCircle(1,4,5)
   # don't wait!
   # start processing buffered OpenGL routines
   glFlush ()

#draws circles (black border first)
def drawCircle(r, x, y):
   glColor3f (0.0, 0.0, 0.0)
   glBegin(GL_POLYGON)      
   for i in range(32):
      cosx = (r+0.05) * cos(i*(2*pi)/32) + x
      siny  = (r+0.05) * sin(i*(2*pi)/32) + y
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

def init():
   # select clearing color
   glClearColor (0.0, 0.0, 0.0, 0.0)

   # initialize viewing values
   glMatrixMode(GL_PROJECTION)
   glLoadIdentity()
   glOrtho(0.0, 10.0, 0.0, 10.0, -10.0, 10.0)

glutInit(sys.argv)
glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
glutInitWindowSize(300, 300)
glutInitWindowPosition(100, 100)
glutCreateWindow("hello")
init()
glutDisplayFunc(display)
glutKeyboardFunc(keyboard)
glutMainLoop()