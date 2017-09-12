
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


    def __str__(self):
        return "Vector<[{},{},{}]>".format(self.x, self.y, self.z)

    @property
    def x(self):
        return self._npa[0]

    @property
    def y(self):
        return self._npa[1]

    @property
    def z(self):
        return self._npa[2]

    @staticmethod
    def from_dict(dict):
        return Vector(dict['X'], dict['Y'], dict['Z'])

    @staticmethod
    def x_forward():
        return Vector(1.0, 0.0, 0.0)

    def as_np_array(self):
        return self._npa
