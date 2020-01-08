from OpenGL.GL import glCallList, glColor3f, glMaterialfv, glMultMatrixf, glPopMatrix, glPushMatrix, \
    GL_EMISSION, GL_FRONT

import random
import numpy as np

import color
import transformation
from aabb import AABB
from primitive import G_OBJ_CUBE, G_OBJ_SPHERE


class Node:
    ''' Base class for scene elements '''
    def __init__(self):
        self.color_index = random.randint(color.MIN_COLOR, color.MAX_COLOR)
        self.aabb = AABB([0.0, 0.0, 0.0], [0.5, 0.5, 0.5])
        self.translation_matrix = np.identity(4)
        self.scaling_matrix = np.identity(4)
        self.selected = False

    def render(self):
        ''' Renders the item to the screen '''
        glPushMatrix()

        # use the ModelView matrix to convert from the 
        # model coordinate space to the view coordinate space
        glMultMatrixf(np.transpose(self.translation_matrix))
        glMultMatrixf(self.scaling_matrix)
        
        glColor3f(*color.COLORS[self.color_index])

        if self.selected:
            # emit light if the node is selected
            glMaterialfv(GL_FRONT, GL_EMISSION, [0.3, 0.3, 0.3])

        self.render_self()

        if self.selected:
            glMaterialfv(GL_FRONT, GL_EMISSION, [0.0, 0.0, 0.0])

        glPopMatrix()

    def render_self(self):
        raise NotImplementedError("The Abstract Node Class doesn't define 'render_self'")

    def pick(self, start, direction, mat):
        ''' Return whether or not the ray hits the object '''
        # transform the ModelView matrix by the current translation
        _mat = np.dot(np.dot(mat, self.translation_matrix), 
                      np.linalg.inv(self.scaling_matrix))
        return self.aabb.ray_hit(start, direction, _mat)

    def select(self, select=None):
       ''' Toggles or sets selected state '''
       if select is not None:
           self.selected = select
       else:
           self.selected = not self.selected

    def rotate_color(self, forward):
        self.color_index += 1 if forward else -1
        if self.color_index > color.MAX_COLOR:
            self.color_index = color.MIN_COLOR
        elif self.color_index < color.MIN_COLOR:
            self.color_index = color.MAX_COLOR

    def scale(self, up):
        s = 1.1 if up else 0.9
        self.scaling_matrix = np.dot(self.scaling_matrix, 
                                     transformation.scaling([s, s, s]))
        self.aabb.scale(s)

    def translate(self, x, y, z):
        self.translation_matrix = np.dot(self.translation_matrix, 
                                         transformation.translation([x, y, z]))

#########################################

class Primitive(Node):
    def __init__(self):
        super(Primitive, self).__init__()
        self.call_list = None

    def render_self(self):
        glCallList(self.call_list)


class Sphere(Primitive):
    ''' Sphere primitive '''

    def __init__(self):
        super(Sphere, self).__init__()
        self.call_list = G_OBJ_SPHERE


class Cube(Primitive):
    ''' Cube primitive '''

    def __init__(self):
        super(Cube, self).__init__()
        self.call_list = G_OBJ_CUBE

#########################################

class HierarchicalNode(Node):
    def __init__(self):
        super(HierarchicalNode, self).__init__()
        self.child_nodes = []

    def render_self(self):
        for child in self.child_nodes:
            child.render()


class SnowFigure(HierarchicalNode):
    def __init__(self):
        super(SnowFigure, self).__init__()
        self.child_nodes = [Sphere(), Sphere(), Sphere()]
        
        self.child_nodes[0].translate(0, -0.6, 0) # scale 1.0
        
        self.child_nodes[1].translate(0, 0.1, 0)
        self.child_nodes[1].scaling_matrix = np.dot(self.scaling_matrix, 
                                                    transformation.scaling([0.8, 0.8, 0.8]))
        
        self.child_nodes[2].translate(0, 0.75, 0)
        self.child_nodes[2].scaling_matrix = np.dot(self.scaling_matrix, 
                                                    transformation.scaling([0.7, 0.7, 0.7]))
        
        for child_node in self.child_nodes:
            child_node.color_index = color.MIN_COLOR
        
        self.aabb = AABB([0.0, 0.0, 0.0], [0.5, 1.1, 0.5])