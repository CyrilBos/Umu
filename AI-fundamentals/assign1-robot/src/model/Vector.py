from math import atan2, sqrt, pow
import numpy


class Vector:
    def __init__(self, x, y, z):
        self._npa = numpy.array([x, y, z])

    def __mul__(self, other):
        if isinstance(other, Vector):
            res = self._npa * other.as_np_array()
            return Vector(res[0], res[1], res[2])
        else:
            res = self._npa * other
            return Vector(res[0], res[1], res[2])

    def __rmul__(self, other):
        return self.__mul__(other)

    def __add__(self, other):
        if isinstance(other, Vector):
            return Vector(self.x + other.x,
                          self.y + other.y,
                          self.z + other.z)
        else:
            raise NotImplemented()

    def __sub__(self, other):
        if isinstance(other, Vector):
            return Vector(self.x - other.x,
                          self.y - other.y,
                          self.z - other.z)
        else:
            raise NotImplemented()

    def __eq__(self, other):
        return isinstance(other, Vector) and self.x == other.x and self.y == other.y and self.z == other.z

    def __str__(self):
        return "Vector<[{},{},{}]>".format(self.x, self.y, self.z)

    @property
    def x(self):
        return self._npa[0]

    @x.setter
    def x(self, value):
        self._npa[0] = value

    @property
    def y(self):
        return self._npa[1]

    @y.setter
    def y(self, value):
        self._npa[1] = value

    @property
    def z(self):
        return self._npa[2]

    @z.setter
    def z(self, value):
        self._npa[2] = value

    @staticmethod
    def from_dict(dict):
        return Vector(dict['X'], dict['Y'], dict['Z'])

    @staticmethod
    def x_forward():
        return Vector(1.0, 0.0, 0.0)

    def as_np_array(self):
        return self._npa

    def get_angle(self, vec):
        return atan2(vec.x - self.x, vec.y - self.y)

    def distance_to(self, vec):
        return sqrt(pow(vec.x - self.x, 2) + pow(vec.y - self.y, 2) + pow(vec.z - self.z, 2))