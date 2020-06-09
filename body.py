import numpy as np
import math

G = 6.67430 / 10 ** 11
class Body:


    def __init__(self, mass = 0, position = np.zeros(3), speed = np.zeros(3), stopped = True):
        self.mass = mass
        self.position = position
        self.old_position = position
        self.speed = speed
        self.stop = stopped

    def __str__(self):
        return f"Mass is {self.mass}, position is {self.position}";

    def __ne__(self, other):
        if(type(other) == Body):
            return(any(self.position - other.position) or any(self.old_position - other.old_position) or self.mass != other.mass)

    def changePosition(self, new_position = np.zeros(3)):
        self.old_position = self.position
        self.position = new_position

    def forceCount(self, obj):
        #F = G * (m1 * m2) / r^2
        r_vec = obj.position - self.position
        r_vec = r_vec.astype(np.float64)
        if(not any(r_vec)):
            return np.zeros(3)
        gravity_c = G * obj.mass * self.mass
        r2 = np.sum(r_vec ** 2)
        r_vec /= np.linalg.norm(r_vec)
        force = r_vec * gravity_c / r2
        return force

