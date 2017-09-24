from math import atan2, cos, sin

from .Vector import Vector
from .Quaternion import Quaternion


def get_ang_spd(cur_pos, cur_rot, tar_pos, lin_spd):
    # angle = 2 * atan2(cur_rot.z, cur_rot.w)
    q = Quaternion(cur_rot.w, Vector(0, 0, cur_rot.z)).heading()
    angle = atan2(q.y, q.x)

    rcs_tar_pos = Vector(0, 0, tar_pos.z)
    rcs_tar_pos.x = (tar_pos.x - cur_pos.x) * cos(angle) + (tar_pos.y - cur_pos.y) * sin(angle)
    rcs_tar_pos.y = -(tar_pos.x - cur_pos.x) * sin(angle) + (tar_pos.y - cur_pos.y) * cos(angle)

    ang_spd = lin_spd / ((pow(rcs_tar_pos.x, 2) + pow(rcs_tar_pos.y, 2)) / (2 * rcs_tar_pos.y))

    return ang_spd
