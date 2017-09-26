"""
Example demonstrating how to communicate with Microsoft Robotic Developer
Studio 4 via the Lokarria http interface. 

Author: Erik Billing (billing@cs.umu.se)

Updated by Ola Ringdahl 204-09-11
"""
import logging
import argparse
import time

from model import Vector, Quaternion
from controller import FixedController, ObstacleController, PathLoader

#url which the MRDS server listens on
mrds_url = 'localhost:50000'

# filename of the path to load. Can be set by appending option --path=filename to this script
path_filepath = 'paths/Path-around-table-and-back.json'

# can be set to True by appending argument --obstacle to this script
# if set to True, instead of a fixed lookahead it will try to optimize as much as possible by detecting obstacles
# if set to False, the controller will skip positions with a fixed lookahead independent of the obstacle detection
obstacle_detection = False

# Optimized parameters for each path when using fixed lookahead pure pursuit algorithm
# the lists respect the format [linear_speed, lookahead, delta_pos]
# these parameters are described in FixedController class (in file controller/fixed_controller.py)
# if using another filename, will use default values
PARAMETERS = {
    'Path-around-table-and-back.json': [1, 5, 0.75],
    'Path-around-table.json': [1.5, 5, 0.25],
    'Path-to-bed.json': [1, 5, 0.75],
    'Path-from-bed.json': [0.5, 5, 1],
}

LOG_LEVEL_STRINGS = ['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG']
logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':
    #Parsing arguments for script options
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', type=str, help='filename of the path to load')
    parser.add_argument('--obstacle', action='store_true', default=False,
                        help='use obstacle detection to optimize the path')
    parser.add_argument('--level', type=str, help='Python logger level (ERROR, INFO, DEBUG). Defaults to info. \
                                                  Setting to debug will provide more information such as current position \
                                                   of the robot (among others). \
                                                  Setting to error will provide less information (only exception catching). ')

    args = parser.parse_args()

    logger = logging.getLogger(__name__)
    #Setting up depending on options values
    if args.obstacle:
        obstacle_detection = True
    if args.path:
        path_filepath = args.path
    if args.level:
        logger.setLevel(args.level)
        logging.getLogger('controller').setLevel(LOG_LEVEL_STRINGS.index(args.level))


    # if not placed in same folder, parses the filename of the filepath of the path
    # used to get the optimized parameters for each path
    if '/' in path_filepath:
        path_filename = path_filepath[path_filepath.rindex('/') + 1:]
    else:
        path_filename = path_filepath
    logger.debug('Filename of path: ' + path_filename)

    #Load the path
    try:
        logger.info('Loading path: {}'.format(path_filepath))
        path_loader = PathLoader(path_filepath)
    except Exception as ex:
        logger.error('Failed to load path {}:\n {}'.format(path_filepath, ex))
        exit()

    pos_path = path_loader.positionPath(timestamps=False)

    logger.info('Sending commands to MRDS server listening at {}'.format(mrds_url))

    if obstacle_detection:
        controller = ObstacleController(mrds_url)
        logger.info('Starting obstacle optimized pure pursuit')
    else:
        if path_filename in PARAMETERS:
            controller = FixedController(mrds_url, PARAMETERS[path_filename][0], PARAMETERS[path_filename][1],
                                         PARAMETERS[path_filename][2])
        else:
            controller = FixedController(mrds_url)
        logger.info('Starting fixed lookahead pure pursuit')

    #Start stopwatch and start sending instructions to the robot
    begin_time = time.time()
    controller.pure_pursuit(pos_path)
    end_time = time.time()

    logger.info('Path done in {}'.format(end_time - begin_time))
