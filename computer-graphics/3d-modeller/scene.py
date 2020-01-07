import sys
import numpy

from node import Sphere, Cube, SnowFigure

class Scene:
    PLACE_DEPTH = 15.0  # default depth from the camera to place an object at

    def __init__(self):
        self.node_list = []  # nodes that are displayed
        self.selected_node = None

    def add_node(self, node):
        ''' Add a new node to the scene '''
        self.node_list.append(node)

    def render(self):
        ''' Render the scene '''
        for node in self.node_list:
            node.render()
