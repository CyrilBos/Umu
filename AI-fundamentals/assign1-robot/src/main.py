"""
Example demonstrating how to communicate with Microsoft Robotic Developer
Studio 4 via the Lokarria http interface. 

Author: Erik Billing (billing@cs.umu.se)

Updated by Ola Ringdahl 204-09-11
"""
import sys


import time
from model import Vector,Quaternion
from utils import PathLoader
from controller import Controller


path_filename = 'paths/Path-around-table.json'

mrds_url = 'localhost:50000'
headers = {"Content-type": "application/json", "Accept": "text/json"}


if __name__ == '__main__':
    if len(sys.argv) > 1:
        path_filename = sys.argv[1]

    try:
        print('Loading path: filename', path_filename)
        path_loader = PathLoader(path_filename)
    except Exception as ex:
        print('Failed to load path {}. Exiting'.format(path_filename), ex)
        exit()

    pos_path = path_loader.positionPath(timestamps=True)
    rot_path = path_loader.orientationPath()

    controller = Controller(mrds_url, headers)

    print('Sending commands to MRDS server', mrds_url)
    begin_time = time.time()

    controller.pure_pursuit(pos_path)

    end_time = time.time()

    print('Path done in {}'.format(end_time - begin_time))

    """
    try:
        print('Telling the robot to go streight ahead.')
        response = postSpeed(0, 0.1)

        print('Telling the robot to go in a circle.')

    except UnexpectedResponse as ex:
        print('Unexpected response from server when sending speed commands:', ex)

    try:
        laser = getLaser()
        laserAngles = getLaserAngles()
        print('The rightmost laser bean has angle %.3f deg from x-axis (streight forward) and distance %.3f meters.' % (
            laserAngles[0], laser['Echoes'][0]
        ))
        print('Beam 1: %.3f Beam 269: %.3f Beam 270: %.3f' % (
        laserAngles[0] * 180 / pi, laserAngles[269] * 180 / pi, laserAngles[270] * 180 / pi))
    except UnexpectedResponse as ex:
        print('Unexpected response from server when reading laser data:', ex)

    try:
        pose, orientation = getPoseAndOrientation()
        print('Current position: ', pose)
        print('Current orientation: ', orientation)
        for t in range(30):

            time.sleep(1)
    except UnexpectedResponse as ex:
        print('Unexpected response from server when reading position:', ex)
    """
