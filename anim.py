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

# globals
x = []
y = []
directionX = []
directionY = []
for i in range(2):
    directionX.append(random.uniform(-0.001, 0.001))
    directionY.append(random.uniform(-0.001, 0.001))
    x.append(random.randint(1, 9))
    y.append(random.randint(1, 9))

def display():
    global x, y, directionX, directionY
   # clear all pixels
    glClearColor(0.870, 0.905, 0.937, 0)
    glClear (GL_COLOR_BUFFER_BIT)
    
    for i in range(2):
        
        x[i] = x[i] + directionX[i]
        y[i] = y[i] + directionY[i]
        
        drawCircle(1, x[i], y[i])

        if x[i] > 10:
            x[i] = 0
        if y[i] > 10:
            y[i] = 0
        if x[i] < 0:
            x[i] = 10
        if y[i] < 0:
            y[i] = 10
       
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
   glutIdleFunc(display)

glutInit(sys.argv)
glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
glutInitWindowSize(500, 500)
glutInitWindowPosition(100, 100)
glutCreateWindow("hello")
init()
glutDisplayFunc(display)
glutKeyboardFunc(keyboard)

glutMainLoop()