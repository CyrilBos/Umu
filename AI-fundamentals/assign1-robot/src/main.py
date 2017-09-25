"""
Example demonstrating how to communicate with Microsoft Robotic Developer
Studio 4 via the Lokarria http interface. 

Author: Erik Billing (billing@cs.umu.se)

Updated by Ola Ringdahl 204-09-11
"""
import sys

import time
from model import Vector, Quaternion
from controller import Controller, PathLoader

import getopt

path_filename = 'paths/Path-around-table.json'

#if set to True, instead of a fixed lookahead it will try to optimize as much as possible by detecting obstacles
optimize_path = False

mrds_url = 'localhost:50000'
headers = {"Content-type": "application/json", "Accept": "text/json"}

if __name__ == '__main__':
    try:
        opts, args = getopt.getopt(sys.argv[1:], '', ['path=', 'optimized'])
    except getopt.GetoptError as err:
        print(err)
        sys.exit(2)
    print(opts)
    print(args)
    for name, value in opts:
        if name == 'optimized':
            optimize_path = True
        if name == '--path':
            path_filename = value

    try:
        print('Loading path: filename', path_filename)
        path_loader = PathLoader(path_filename)
    except Exception as ex:
        print('Failed to load path {}: '.format(path_filename), ex)
        exit()

    controller = Controller(mrds_url, headers)

    pos_path = path_loader.positionPath(timestamps=False)
    rot_path = path_loader.orientationPath()


    print('Sending commands to MRDS server listening at', mrds_url)
    begin_time = time.time()

    if optimize_path:
        print('Starting obstacle optimized pure pursuit')
        controller.optimized_pure_pursuit(pos_path)
    else:
        print('Starting fixed lookahead pure pursuit')
        controller.fixed_pure_pursuit(pos_path)

    end_time = time.time()

    print('Path done in {}'.format(end_time - begin_time))
