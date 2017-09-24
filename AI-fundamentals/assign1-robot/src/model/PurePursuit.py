from math import atan2, cos, sin

from .Vector import Vector
from .Quaternion import Quaternion


def get_ang_spd(cur_pos, cur_rot, tar_pos, lin_spd):
    """
        Computes the angular speed using pure pursuit formulas
    """
    # angle = 2 * atan2(cur_rot.z, cur_rot.w)
    q = Quaternion(cur_rot.w, Vector(0, 0, cur_rot.z)).heading()
    angle = atan2(q.y, q.x)

    rcs_tar_pos = tar_pos.convert_to_rcs(cur_pos, cur_rot)

    ang_spd = lin_spd / ((pow(rcs_tar_pos.x, 2) + pow(rcs_tar_pos.y, 2)) / (2 * rcs_tar_pos.y))

    return ang_spd
