from math import atan2, sqrt, pow, cos, sin


class Vector:
    def __init__(self, x, y, z):
        self._x = x
        self._y = y
        self._z = z

    def __eq__(self, other):
        return isinstance(other, Vector) and self.x == other.x and self.y == other.y and self.z == other.z

    def __str__(self):
        return "Vector<[{},{},{}]>".format(self.x, self.y, self.z)

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value

    @property
    def z(self):
        return self._z

    @z.setter
    def z(self, value):
        self._z = value

    @staticmethod
    def from_dict(vec_dict):
        return Vector(vec_dict['X'], vec_dict['Y'], vec_dict['Z'])

    @staticmethod
    def x_forward():
        return Vector(1.0, 0.0, 0.0)

    def get_angle(self, vec):
        return atan2(vec.x - self.x, vec.y - self.y)

    def distance_to(self, vec):
        return sqrt(pow(vec.x - self.x, 2) + pow(vec.y - self.y, 2) + pow(vec.z - self.z, 2))

    def convert_to_rcs(self, cur_pos, cur_rot):
        angle = 2 * atan2(cur_rot.z, cur_rot.w)
        rcs_pos = Vector(0, 0, self.z)

        rcs_pos.x = (self.x - cur_pos.x) * cos(angle) + (self.y - cur_pos.y) * sin(angle)
        rcs_pos.y = -(self.x - cur_pos.x) * sin(angle) + (self.y - cur_pos.y) * cos(angle)

        return rcs_pos
