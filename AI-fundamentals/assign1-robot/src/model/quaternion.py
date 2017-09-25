import numpy

from .vector import Vector


class Quaternion:
    __w = 0

    def __init__(self, w, vector):
        if not isinstance(vector, Vector):
            raise (TypeError('Parameter vector of init is not a vector'))
        self.__unit_vector = vector
        self.__w = w

    def __mul__(self, other):
        """
                elif isinstance(other, Vector):
                    axis = Vector(self.x, self.y, self.z)
                    uv = axis * other
                    uuv = axis * uv
                    uv *= (2.0 * self.__w)
                    uuv *= 2.0
                    return other + uv + uuv
                """

        if isinstance(other, Quaternion):
            return Quaternion(self.w * other.w - self.x * other.x - self.y * other.y - self.z * other.z,
                              Vector(self.__w * other.x + self.x * other.w + self.y * other.z - self.z * other.y,
                                     self.__w * other.y - self.x * other.z + self.y * other.w + self.z * other.x,
                                     self.__w * other.z + self.x * other.y - self.y * other.x + self.z * other.w))
        else:
            raise TypeError('trying to multiply a quaternion by something else than a quaternion or a vector')

    def __rmul__(self, other):
        return self.__mul__(other)

    def __str__(self):
        return "Quaternion<{}, [{},{},{}]>".format(self.w, self.x, self.y, self.z)

    @property
    def unit_vector(self):
        return self.__unit_vector

    @property
    def x(self):
        return self.__unit_vector.x

    @property
    def y(self):
        return self.__unit_vector.y

    @property
    def z(self):
        return self.__unit_vector.z

    @property
    def w(self):
        return self.__w

    @staticmethod
    def from_two_vectors(u, v):
        w = numpy.cross(u.as_np_array(), v.as_np_array())
        q = Quaternion(1. + u * v, Vector(w[0], w[1], w[2]))
        return q.normalize()

    @staticmethod
    def from_dict(dict):
        return Quaternion(dict['W'], Vector(dict['X'], dict['Y'], dict['Z']))

    def normalize(self):
        return (self.__w + self.x + self.y + self.z) / \
               numpy.sqrt(self.__w * self.__w + self.x * self.x + self.y * self.y + self.z * self.z)

    def conjugate(self):
        return Quaternion(self.w, Vector(-self.x, -self.y, -self.z))

    def heading(self):
        return self.rotate(Vector.x_forward())

    def rotate(self, v):
        rotated = (self * Quaternion(0, Vector(v.x, v.y, v.z))) * self.conjugate()
        return Vector(rotated.x, rotated.y, rotated.z)

    def as_vector(self):
        return Vector(self.x, self.y, self.z)
