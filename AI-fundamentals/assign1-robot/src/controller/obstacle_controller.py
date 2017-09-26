from logging import getLogger

from .controller import Controller
from model import Vector, pure_pursuit

logger = getLogger('controller')

class ObstacleController(Controller):
    def pure_pursuit(self, pos_path):
        """
            Implements the pure pursuit algorithm using obstacle detection to aim for the furthest position possible.

            :param pos_path: path loaded into Vector
            :type pos_path: list
            :
        """
        pos_index = -1
        last_pos_index = len(pos_path) - 1
        while pos_index < last_pos_index:
            cur_pos, cur_rot = self.get_pos_and_orientation()
            pos_index = self.next_optimized_waypoint(cur_pos, cur_rot, pos_path, pos_index)
            logger.info("Target position path index: {}".format(pos_index))
            self.travel(cur_pos, pos_path[pos_index], self._lin_spd, pure_pursuit.get_ang_spd(cur_pos, cur_rot, pos_path[pos_index], self._lin_spd))
            pos_index+=1
        self.stop()


    def next_optimized_waypoint(self, cur_pos, cur_rot, pos_path, cur_pos_index):
        """
            Returns the furthest point from path without an obstacle. Stops at the first position where the laser of nearest
            angle (laser angle ~= aimed position angle) detects an obstacle (laser distance < aimed position distance).
            :param pos_path: path loadsed into Vector
            :param type: list
            :param step: lookahead value, i.e the number of positions skipped

        """
        lasers_angles = self.get_laser_scan_angles()
        lasers = self.get_laser_scan()['Echoes']

        #Go through every position on the path starting at the position next to the current one
        for i in range(cur_pos_index+1, len(pos_path)):
            tar_pos = pos_path[i]
            #convert potential aimed position to RCS
            rcs_tar_pos = pure_pursuit.convert_to_rcs(tar_pos, cur_pos, cur_rot)

            rcs_origin = Vector(0, 0, 0)
            #compute angle between current robot position
            tar_angle = rcs_origin.get_angle(rcs_tar_pos)

            min_ind = 0
            min = tar_angle - lasers_angles[0]
            # search for the nearest angle in laser_angles (
            # could be simplified with a calculation instead of this iteration
            for j in range(1, len(lasers_angles)):
                dist = tar_angle - lasers_angles[j]
                if dist < min:
                    min = dist
                    min_ind = j

            if lasers[min_ind] < cur_pos.distance_to(tar_pos):
                # if the laser hits an obstacle, return the index of the previous position on the path
                return i - 1
        # reached the last position on the path
        return len(pos_path) - 1