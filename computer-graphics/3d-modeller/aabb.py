from OpenGL.GL import glCallList, glMatrixMode, glPolygonMode, glPopMatrix, glPushMatrix, glTranslated, \
    GL_FILL, GL_FRONT_AND_BACK, GL_LINE, GL_MODELVIEW

import math
import numpy as np

from primitive import G_OBJ_CUBE

EPSILON = 0.000001


class AABB(object):
    ''' Axis Aligned Bounding Box (AABB) '''

    def __init__(self, center, size):
        self.center = np.array(center)
        self.size = np.array(size)

    def scale(self, scale):
        self.size *= scale

    def ray_hit(self, origin, direction, modelmatrix):
        ''' Returns wether or not the ray hits the AABB (and the distance if it does) '''
        aabb_min = self.center - self.size
        aabb_max = self.center + self.size
        tmin = 0.0
        tmax = 100000.0

        # Oriented Bounding Box (OBB)
        obb_pos_worldspace = np.array(modelmatrix[0:3, 3])
        delta = (obb_pos_worldspace - origin)

        # test intersection with 2 planes perpendicular to the OBB's x-axis
        xaxis = np.array(modelmatrix[0, 0:3])

        e = np.dot(xaxis, delta)
        f = np.dot(direction, xaxis)
        if math.fabs(f) > EPSILON:
            t1 = (e + aabb_min[0]) / f
            t2 = (e + aabb_max[0]) / f
            if t1 > t2:
                t1, t2 = t2, t1
            if t2 < tmax:
                tmax = t2
            if t1 > tmin:
                tmin = t1
            if tmax < tmin:
                return False, 0
        elif (aabb_min[0] - e > EPSILON) or (aabb_max[0] - e < -EPSILON):
            return False, 0

        # intersection in the y-axis
        yaxis = np.array(modelmatrix[1, 0:3])

        e = np.dot(yaxis, delta)
        f = np.dot(direction, yaxis)
        if math.fabs(f) > EPSILON:
            t1 = (e + aabb_min[1]) / f
            t2 = (e + aabb_max[1]) / f
            if t1 > t2:
                t1, t2 = t2, t1
            if t2 < tmax:
                tmax = t2
            if t1 > tmin:
                tmin = t1
            if tmax < tmin:
                return False, 0
        elif (aabb_min[1] - e > EPSILON) or (aabb_max[1] - e < -EPSILON):
            return False, 0

        # intersection in the z-axis
        zaxis = np.array(modelmatrix[2, 0:3])

        e = np.dot(zaxis, delta)
        f = np.dot(direction, zaxis)
        if math.fabs(f) > EPSILON:
            t1 = (e + aabb_min[2]) / f
            t2 = (e + aabb_max[2]) / f
            if t1 > t2:
                t1, t2 = t2, t1
            if t2 < tmax:
                tmax = t2
            if t1 > tmin:
                tmin = t1
            if tmax < tmin:
                return False, 0
        elif (aabb_min[2] - e > EPSILON) or (aabb_max[2] - e < -EPSILON):
            return False, 0

        return True, tmin

    def render(self):
        ''' Render the AABB '''
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()

        glTranslated(*self.center[0:3])
        glCallList(G_OBJ_CUBE)

        glPopMatrix()
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
