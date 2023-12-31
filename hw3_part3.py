if __name__ == '__build__':
	raise Exception

import sys
try:
  from OpenGL.GLUT import *
  from OpenGL.GL import *
  from OpenGL.GLU import *
  from math import *
  import random
  import time
  import collections
except:
  print ('''
ERROR: PyOpenGL not installed properly.
        ''')
  sys.exit()

# globals
x = []
y = []
vx = []
vy = []
directionX = []
directionY = []
MAX_FORCE = 0.01
MAX_SPEED = 1.5
TIME_STEP = 0.5
for i in range(300):
    directionX.append(random.uniform(-0.05, 0.05))
    directionY.append(random.uniform(-0.05, 0.05))
    x.append(random.randint(1, 49))
    y.append(random.randint(1, 49))
    vx.append(random.uniform(0.5,2.0)*random.uniform(0.0,0.1))
    vy.append(random.uniform(0.5,2.0)*random.uniform(0.0,0.1))

def distance (x1,y1,x2,y2):
    return sqrt((x2-x1)*(x2-x1)+(y2-y1)*(y2-y1))

def agentAtPoint(x1,y1):
    for i in range(300):
        if (distance(x1,y1,x,y) < 10):
            return True
    return True

#Source code: http://mauveweb.co.uk/posts/2011/05/introduction-to-spatial-hashes.html
class SpatialHash(object):
    def __init__(self, cell_size=10.0):
        self.cell_size = float(cell_size)
        self.d = {}

    #def __call__(self):
        #if self.potential_collisions(self,r,obj) >= 2:

    def _add(self, cell_coord, o):
        """Add the object o to the cell at cell_coord."""
        try:
            self.d.setdefault(cell_coord, set()).add(o)
        except KeyError:
            self.d[cell_coord] = set((o,))

    def _cells_for_rect(self, r):
        """Return a set of the cells into which r extends."""
        cells = set()
        cy = floor(r.y1 / self.cell_size)
        while (cy * self.cell_size) <= r.y2:
            cx = floor(r.x1 / self.cell_size)
            while (cx * self.cell_size) <= r.x2:
                cells.add((int(cx), int(cy)))
                cx += 1.0
            cy += 1.0
        return cells

    def add_rect(self, r, obj):
        """Add an object obj with bounds r."""
        cells = self._cells_for_rect(r)
        for c in cells:
            self._add(c, obj)

    def potential_collisions(self, r, obj):
        cells = self._cells_for_rect(r)
        potentials = set()
        for c in cells:
            potentials.update(self.d.get(c, set()))
        potentials.discard(obj) # obj cannot intersect itself
        return potentials

#prints fps to console
class FPS:
    def __init__(self,averageof=50):
        self.frametimestamps = collections.deque(maxlen=averageof)
    def __call__(self):
        self.frametimestamps.append(time.time())
        if(len(self.frametimestamps) > 1):
            return round(len(self.frametimestamps)/(self.frametimestamps[-1]-self.frametimestamps[0]),1)
        else:
            return 0.0

fps = FPS()
shash = SpatialHash()

def display():
    global x, y, directionX, directionY

    time.sleep(0.01)
    print(fps())

   # clear all pixels
    glClearColor(0.870, 0.905, 0.937, 0)
    glClear (GL_COLOR_BUFFER_BIT)
    
    for i in range(300):
        
        x[i] = x[i] + directionX[i]
        y[i] = y[i] + directionY[i]
        
        drawCircle(0.3, x[i], y[i])

        if x[i] > 50:
            x[i] = 0
        if y[i] > 50:
            y[i] = 0
        if x[i] < 0:
            x[i] = 50
        if y[i] < 0:
            y[i] = 50

        f_avoid_x = 0
        f_avoid_y = 0
        f_avoid_ctr = 0
        interacting_agents_cntr = 0
        v_x = vx[i]
        v_y = vy[i]
        zeta = 1.0023
        f_goal_x = (directionX[i] - v_x) / zeta
        f_goal_y = (directionY[i] - v_y) / zeta
        for j in range(300):
            if(i == j):
                continue
            dist = distance(x[i], y[i], x[j], y[j])
            if dist > 0 and dist < 1.6:
                d_ab = max(dist-0.3,0.01)
                k = max(1.6-d_ab,0)
                x_ab = (x[i]-x[j])/dist
                y_ab = (y[i]-y[j])/dist

                interacting_agents_cntr += 1
                f_avoid_x += k*x_ab/d_ab
                f_avoid_y += k*y_ab/d_ab
                f_avoid_ctr += 1
        
        if f_avoid_ctr > 0:
            f_avoid_x = (f_avoid_x/f_avoid_ctr) * 2
            f_avoid_y = (f_avoid_y/f_avoid_ctr) * 2

        force_sum_x = f_goal_x + f_avoid_x * 2
        force_sum_y = f_goal_y + f_avoid_y * 2
        f_avoid_mag = sqrt(force_sum_x*force_sum_x + force_sum_y*force_sum_y)
        if(f_avoid_mag > MAX_FORCE):
            force_sum_x = (MAX_FORCE*force_sum_x/f_avoid_mag) * 2
            force_sum_y = (MAX_FORCE*force_sum_y/f_avoid_mag) * 2
        v_x += TIME_STEP * force_sum_x
        v_y += TIME_STEP * force_sum_y
        speed = sqrt(v_x*v_x + v_y*v_y)
        if(speed > MAX_SPEED):
            v_x = MAX_SPEED * v_x / speed
            v_y = MAX_SPEED * v_y / speed
        vx[i] = v_x
        vy[i] = v_y
        x[i] += (TIME_STEP*v_x)
        y[i] += (TIME_STEP*v_y)

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
   glOrtho(0.0, 50.0, 0.0, 50.0, -50.0, 10.0)
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