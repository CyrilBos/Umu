"""
Example demonstrating how to communicate with Microsoft Robotic Developer
Studio 4 via the Lokarria http interface. 

Author: Erik Billing (billing@cs.umu.se)

Updated by Ola Ringdahl 204-09-11
"""
import sys

import time
from model import Vector, Quaternion
from controller import FixedController, ObstacleController, PathLoader

import argparse

# filename of the path to load. Can be set by --path=filename
path_filepath = 'paths/Path-around-table-and-back.json'

# if set to True, instead of a fixed lookahead it will try to optimize as much as possible by detecting obstacles
# can be set to true by using --optimized option as an argument of this script
# if set to False, the controller will skip positions with a fixed lookahead independent of the obstacle detection
optimize_path = False

mrds_url = 'localhost:50000'
headers = {"Content-type": "application/json", "Accept": "text/json"}

# Optimized parameters for each path when using fixed lookahead pure pursuit algorithm
#the lists respect the format [linear_speed, lookahead, delta_pos]
#these parameters are described in FixedController class (in file controller/fixed_controller.py)
# if using another filename, will use default values
PARAMETERS = {
    'Path-around-table-and-back.json': [1.5, 20, 0.5],
    'Path-around-table.json': [1.5, 5, 0.25],
    'Path-to-bed.json': [1, 5, 0.5],
    'Path-from-bed.json': [1.0, 10, 0.75],
}

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', type=str, help='filename of the path to load')
    parser.add_argument('--obstacle', action='store_true', default=False,
                        help='use obstacle detection to optimize the path')

    args = parser.parse_args()
    if args.obstacle:
        optimize_path = True
    if args.path:
        path_filepath = args.path

    # if not placed in same folder, parses the filename of the filepath of the path
    # used to get the optimized parameters for each path
    if '/' in path_filepath:
        path_filename = path_filepath[path_filepath.rindex('/')+1:]
    else:
        path_filename = path_filepath

    try:
        print('Loading path: filename', path_filepath)
        path_loader = PathLoader(path_filepath)
    except Exception as ex:
        print('Failed to load path {}: '.format(path_filepath), ex)
        exit()

    pos_path = path_loader.positionPath(timestamps=False)
    rot_path = path_loader.orientationPath()

    print('Sending commands to MRDS server listening at', mrds_url)

    if optimize_path:
        controller = ObstacleController(mrds_url, headers)
        print('Starting obstacle optimized pure pursuit')
    else:
        controller = FixedController(mrds_url, headers, PARAMETERS[path_filename][0], PARAMETERS[path_filename][1], PARAMETERS[path_filename][2])
        print('Starting fixed lookahead pure pursuit')

    begin_time = time.time()
    controller.pure_pursuit(pos_path)
    end_time = time.time()

    print('Path done in {}'.format(end_time - begin_time))
