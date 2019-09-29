"""
Generates a quintic polynomial trajectory.

Author: Daniel Ingram (daniel-s-ingram)
"""

import numpy as np

class TrajectoryGenerator():
    def __init__(self, start_pos, des_pos, T, start_vel=[0,0,0], des_vel=[0,0,0], start_acc=[0,0,0], des_acc=[0,0,0]):
        self.start_x,     self.start_y,     self.start_z,     *_ = start_pos
        self.des_x,       self.des_y,       self.des_z,       *_ = des_pos
        self.start_x_vel, self.start_y_vel, self.start_z_vel, *_ = start_vel
        self.des_x_vel,   self.des_y_vel,   self.des_z_vel,   *_ = des_vel
        self.start_x_acc, self.start_y_acc, self.start_z_acc, *_ = start_acc
        self.des_x_acc,   self.des_y_acc,   self.des_z_acc,   *_ = des_acc
        self.T = T

    def solve(self):
        A = np.array([[0, 0, 0, 0, 0, 1], [   self.T**5,    self.T**4,   self.T**3,    self.T**2, self.T, 1],
                      [0, 0, 0, 0, 1, 0], [ 5*self.T**4,  4*self.T**3, 3*self.T**2,  2*self.T,       1,   0],
                      [0, 0, 0, 2, 0, 0], [20*self.T**3, 12*self.T**2, 6*self.T,            2,       0,   0]])

        b_x = np.array([[self.start_x],     [self.des_x],
                        [self.start_x_vel], [self.des_x_vel],
                        [self.start_x_acc], [self.des_x_acc]])

        b_y = np.array([[self.start_y],     [self.des_y],
                        [self.start_y_vel], [self.des_y_vel],
                        [self.start_y_acc], [self.des_y_acc]])

        b_z = np.array([[self.start_z],     [self.des_z],
                        [self.start_z_vel], [self.des_z_vel],
                        [self.start_z_acc], [self.des_z_acc]])

        self.x_c = np.linalg.solve(A, b_x)
        self.y_c = np.linalg.solve(A, b_y)
        self.z_c = np.linalg.solve(A, b_z)