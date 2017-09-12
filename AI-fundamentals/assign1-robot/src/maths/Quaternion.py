import numpy

from .Vector import Vector


class Quaternion(Vector):
    __w = 0
    __rmul__ = __mul__

    def __init__(self, w, x, y, z):
        super().__init__(x, y, z)
        self.__w = w

    def __mul__(self, other):
        if isinstance(other, Quaternion):
            return Quaternion(self.w * other.w - self.x * other.x - self.y * other.y - self.z * other.z,
                              self.__w * other.x + self.x * other.w + self.y * other.z - self.z * other.y,
                              self.__w * other.y - self.x * other.z + self.y * other.w + self.z * other.x,
                              self.__w * other.z + self.x * other.y - self.y * other.x + self.z * other.w)
        elif isinstance(other, Vector):
            axis = Vector(self.x, self.y, self.z)
            uv = axis * other
            uuv = axis * uv
            uv *= (2.0 * self.__w)
            uuv *= 2.0
            return other + uv + uuv
        else:
            raise TypeError('trying to multiply a quaternion by something else than a quaternion or a vector')

    @property
    def w(self):
        return self.__w

    @classmethod
    def from_two_vectors(cls, u, v):
        w = numpy.cross(u.as_np_array(), v.as_np_array())
        q = cls(1. + u * v, w[0], w[1], w[2])
        return q.normalize()

    def normalize(self):
        return (self.__w + self.x + self.y + self.z) / \
               numpy.sqrt(self.__w * self.__w + self.x * self.x + self.y * self.y + self.z * self.z)

    def conjugate(self):
        return Quaternion(-self.x, -self.y, -self.z, self.w)

    def heading(self):
        return self.rotate(Vector.x_forward())

    def rotate(self, v):
        rotated = (self * Quaternion(v.x, v.y, v.z, 0)) * self.conjugate()
        return Vector(rotated.x, rotated.y, rotated.z)
