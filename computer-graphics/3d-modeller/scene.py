import numpy as np

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

    def pick(self, start, direction, mat):
        ''' Execute selection '''
        if self.selected_node is not None:
            self.selected_node.select(False)
            self.selected_node = None

        # keep track of the closest hit
        min_dist, closest_node = float('inf'), None
        for node in self.node_list:
            hit, distance = node.pick(start, direction, mat)
            if hit and distance < min_dist:
                min_dist, closest_node = distance, node

        # if we hit something, keep track of it
        if closest_node is not None:
            closest_node.select()
            closest_node.depth = min_dist
            closest_node.selected_loc = start + direction * min_dist
            self.selected_node = closest_node

    def rotate_selected_color(self, forward):
        ''' Rotate the color of the currently selected node '''
        if self.selected_node is not None:
            self.selected_node.rotate_color(forward)

    def scale_selected(self, up):
        ''' Scale the current selection '''
        if self.selected_node is not None:
            self.selected_node.scale(up)

    def move_selected(self, start, direction, inv_modelview):
        ''' Move the selected node, if there is one '''
        if self.selected_node is not None:
            # find the current depth and location of the selected node
            node = self.selected_node
            depth = node.depth
            old_loc = node.selected_loc

            # the new location is the same the depth, along the new ray
            new_loc = start + direction * depth

            # transform the translation with the ModelView matrix
            translation = new_loc - old_loc
            pre_translation = np.array([*translation[0:3], 0])
            translation = inv_modelview.dot(pre_translation)

            # translate the node and track its location
            node.translate(*translation[0:3])
            node.selected_loc = new_loc

    def place(self, shape, start, direction, inv_modelview):
        ''' Place a new node '''
        new_node = None

        if shape == 'sphere':
            new_node = Sphere()
        elif shape == 'cube':
            new_node = Cube()
        elif shape == 'figure':
            new_node = SnowFigure()

        if new_node is not None:
            self.add_node(new_node)

            # place the node at the cursor in camera-space
            translation = start + direction * self.PLACE_DEPTH

            # convert the translation to world-space
            pre_translation = np.array([*translation[0:3], 1])
            translation = inv_modelview.dot(pre_translation)

            new_node.translate(*translation[0:3])
