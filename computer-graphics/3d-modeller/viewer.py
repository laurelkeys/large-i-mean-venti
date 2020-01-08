from OpenGL.GL import glCallList, glClear, glClearColor, glColorMaterial, glCullFace, glDepthFunc, glDisable, glEnable,\
                      glFlush, glGetFloatv, glLightfv, glLoadIdentity, glMatrixMode, glMultMatrixf, glPopMatrix, \
                      glPushMatrix, glTranslated, glViewport, \
                      GL_AMBIENT_AND_DIFFUSE, GL_BACK, GL_CULL_FACE, GL_COLOR_BUFFER_BIT, GL_COLOR_MATERIAL, \
                      GL_DEPTH_BUFFER_BIT, GL_DEPTH_TEST, GL_FRONT_AND_BACK, GL_LESS, GL_LIGHT0, GL_LIGHTING, \
                      GL_MODELVIEW, GL_MODELVIEW_MATRIX, GL_POSITION, GL_PROJECTION, GL_SPOT_DIRECTION
from OpenGL.constants import GLfloat_3, GLfloat_4
from OpenGL.GLU import gluPerspective, gluUnProject
from OpenGL.GLUT import glutCreateWindow, glutDisplayFunc, glutGet, glutInit, glutInitDisplayMode, \
                        glutInitWindowSize, glutMainLoop, \
                        GLUT_SINGLE, GLUT_RGB, GLUT_WINDOW_HEIGHT, GLUT_WINDOW_WIDTH

import numpy as np

from interaction import Interaction
from primitive import init_primitives, G_OBJ_PLANE
from node import Sphere, Cube, SnowFigure
from scene import Scene

# ref.: http://aosabook.org/en/500L/a-3d-modeller.html

# All CAD tools must include at least the three features:
# - a data structure to represent the design,
# - the ability to display it to the screen, and
# - a method to interact with the design.
#
# With that in mind, let's explore how we can represent a 3D design,
# display it to the screen, and interact with it, in 500 lines of Python.
#
# We define a matrix which converts points in the models (also called a mesh) 
# from the model spaces into the world space, called the model matrix. 
# We also define the view matrix, which converts from the world space into the eye space. 
# We combine these two matrices to obtain the ModelView matrix.

class Viewer:
    def __init__(self):
        ''' Initialize the viewer '''
        self.init_interface()
        self.init_opengl()
        self.init_scene()
        self.init_interaction()
        init_primitives()

    def init_interface(self):
        ''' Initialize the window and register the render function '''
        glutInit()
        glutInitWindowSize(640, 480)
        glutCreateWindow("3D Modeller")
        glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
        glutDisplayFunc(self.render)

    def init_opengl(self):
        ''' Initialize the OpenGL settings to render the scene '''
        self.inverseModelView = np.identity(4)
        self.modelView = np.identity(4)

        glEnable(GL_CULL_FACE)
        glCullFace(GL_BACK)
        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LESS)

        glEnable(GL_LIGHT0)
        glLightfv(GL_LIGHT0, GL_POSITION, GLfloat_4(0, 0, 1, 0))
        glLightfv(GL_LIGHT0, GL_SPOT_DIRECTION, GLfloat_3(0, 0, -1))

        glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
        glEnable(GL_COLOR_MATERIAL)
        glClearColor(0.4, 0.4, 0.4, 0.0)

    def init_scene(self):
        ''' Initialize the scene object and initial scene '''
        self.scene = Scene()
        self.create_sample_scene()

    def create_sample_scene(self):
        cube_node = Cube()
        cube_node.translate(2, 0, 2)
        cube_node.color_index = 2
        self.scene.add_node(cube_node)

        sphere_node = Sphere()
        sphere_node.translate(-2, 0, 2)
        sphere_node.color_index = 3
        self.scene.add_node(sphere_node)

        hierarchical_node = SnowFigure()
        hierarchical_node.translate(-2, 0, -2)
        self.scene.add_node(hierarchical_node)

    def init_interaction(self):
        ''' Initialize user interaction and callbacks '''
        self.interaction = Interaction()
        self.interaction.register_callback('pick', self.pick)
        self.interaction.register_callback('move', self.move)
        self.interaction.register_callback('place', self.place)
        self.interaction.register_callback('rotate_color', self.rotate_color)
        self.interaction.register_callback('scale', self.scale)

    def main_loop(self):
        glutMainLoop() # OpenGL Utility Toolkit (GLUT)
    
    def render(self):
        ''' The render pass for the scene '''
        self.init_view()

        glEnable(GL_LIGHTING)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # load the ModelView matrix from the current state of the trackball
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()
        loc = self.interaction.translation
        glTranslated(*loc[0:3])
        glMultMatrixf(self.interaction.trackball.matrix)

        # store the inverse of the currebt ModelView
        currentModelView = np.array(glGetFloatv(GL_MODELVIEW_MATRIX))
        self.modelView = np.transpose(currentModelView)
        self.inverseModelView = np.linalg.inv(np.transpose(currentModelView))

        # render the scene (calls the render function for each object)
        self.scene.render()

        # draw the grid
        glDisable(GL_LIGHTING)
        glCallList(G_OBJ_PLANE)
        glPopMatrix()

        # flush the buffers so that the scene can be drawn
        glFlush()

    def init_view(self):
        ''' Initialize the projection matrix '''
        x_size, y_size = glutGet(GLUT_WINDOW_WIDTH), glutGet(GLUT_WINDOW_HEIGHT)
        aspect_ratio = x_size / y_size

        # load teh projection matrix (always the same)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        glViewport(0, 0, x_size, y_size)
        gluPerspective(70, aspect_ratio, 0.1, 1000.0)
        glTranslated(0, 0, -15)

    def get_ray(self, x, y):
        ''' Generate a ray beginning at the near plane, 
            in the direction that the (x, y) coordinates are facing '''
        self.init_view()

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        # get two points on the line
        start = np.array(gluUnProject(x, y, 0.001))
        end   = np.array(gluUnProject(x, y, 0.999))

        # convert the points into a ray
        direction = end - start
        direction = direction / np.linalg.norm(direction)

        return start, direction

    def pick(self, x, y):
        ''' Select and pick an object in the scene '''
        start, direction = self.get_ray(x, y)
        self.scene.pick(start, direction, self.modelView)

    def move(self, x, y):
        ''' Execute a move command on the scene '''
        start, direction = self.get_ray(x, y)
        self.scene.move_selected(start, direction, self.inverseModelView)

    def rotate_color(self, forward):
        ''' Rotate the color of the selected node '''
        self.scene.rotate_selected_color(forward)

    def scale(self, up):
        ''' Scale the selected node '''
        self.scene.scale_selected(up)

    def place(self, shape, x, y):
        ''' Execute a placement of a new primitive into the scene '''
        start, direction = self.get_ray(x, y)
        self.scene.place(shape, start, direction, self.inverseModelView)


if __name__ == "__main__":
    viewer = Viewer()
    viewer.main_loop()
