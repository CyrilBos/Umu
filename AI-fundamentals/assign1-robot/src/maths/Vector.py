import numpy

from .Quaternion import Quaternion


class Vector:
    def __init__(self, x, y, z):
        self._npa = numpy.array([x, y, z])

    def __mul__(self, other):
        res = self._npa * other.as_np_array()
        return Vector(res[0], res[1], res[2])

    def __add__(self, other):
        if isinstance(other, Vector):
            return Vector(self.x + other.x,
                          self.y + other.y,
                          self.z + other.z)

    @property
    def x(self):
        return self._npa[0]

    @property
    def y(self):
        return self._npa[1]

    @property
    def z(self):
        return self._npa[2]

    @classmethod
    def from_quaternion(cls, q):
        if isinstance(q, Quaternion):
            return Vector(q.x, q.y, q.z)

    @classmethod
    def x_forward(cls):
        return Vector(1.0, 0.0, 0.0)

    def as_np_array(self):
        return self._npa
