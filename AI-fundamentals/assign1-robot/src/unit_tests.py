import unittest

from maths import Vector
from maths import Quaternion

from lokarriaexample import qmult, conjugate, rotate
from path import Path


def are_vect_dict_equal(quat, quat_dict):
    return quat.x == quat_dict['X'] and quat.y == quat_dict['Y'] and quat.z == quat_dict['Z']

def are_quat_dict_equal(quat, quat_dict):
    return quat.x == quat_dict['X'] and quat.y == quat_dict['Y'] and quat.z == quat_dict['Z'] and quat.w == quat_dict['W']

class TestMathsModule(unittest.TestCase):
    p = Path('Path-around-table-and-back.json')
    vect_dicts = p.positionPath(dict=True)
    vects = p.positionPath()
    quat_dicts = p.orientationPath(dict=True)
    quats = p.orientationPath()

    def test_loading(self):
        for i in range(len(self.quats)):
            if not are_quat_dict_equal(self.quats[i], self.quat_dicts[i]):
                print(i)
                print(self.quats[i])
                print(self.quat_dicts[i])
                self.assertTrue(False)
        for i in range(len(self.vects)):
            if not are_vect_dict_equal(self.vects[i], self.vect_dicts[i]):
                self.assertTrue(False)
        self.assertTrue(True)

    def test_conjugation(self):
        self.assertTrue(are_quat_dict_equal(self.quats[0].conjugate(), conjugate(self.quat_dicts[0])))

    def test_multplication(self):
        self.assertTrue(are_quat_dict_equal(self.quats[0] * self.quats[1], qmult(self.quat_dicts[0], self.quat_dicts[1])))

    def test_rotation(self):
        self.assertTrue(are_vect_dict_equal(self.quats[0].rotate(self.vects[0]), rotate(self.quat_dicts[0], self.vect_dicts[0])))

if __name__ == '__main__':
    unittest.main()
