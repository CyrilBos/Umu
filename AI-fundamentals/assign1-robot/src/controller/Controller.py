import http.client
import json
from math import atan2, cos, sin, pow, sqrt, pi
from time import sleep

from model import Vector, Quaternion, PurePursuit


class Controller:
    class UnexpectedResponse(Exception):
        pass

    def __init__(self, mrds_url, headers):
        self.__mrds = http.client.HTTPConnection(mrds_url)
        self.__headers = headers

    def post_speed(self, angular_speed, linear_speed):
        """
        Sends a speed command to the MRDS server

        :param angular_speed: value of angular speed
        :type angular_speed: float
        :param linear_speed: value of linear speed
        :type linear_speed: float
        """
        params = json.dumps({'TargetAngularSpeed': angular_speed, 'TargetLinearSpeed': linear_speed})
        self.__mrds.request('POST', '/lokarria/differentialdrive', params, self.__headers)
        response = self.__mrds.getresponse()
        status = response.status
        response.close()
        if status == 204:
            return response
        else:
            raise self.UnexpectedResponse(response)

    def get_pos(self):
        """Reads the current position from the MRDS"""
        self.__mrds.request('GET', '/lokarria/localization')
        response = self.__mrds.getresponse()
        if response.status == 200:
            pos_data = json.loads(response.read())
            response.close()
            return Vector.from_dict(pos_data['Pose']['Position'])
        else:
            raise self.UnexpectedResponse(response)

    def get_pos_and_orientation(self):
        """Reads the current position and orientation from the MRDS"""
        self.__mrds.request('GET', '/lokarria/localization')
        response = self.__mrds.getresponse()
        if response.status == 200:
            pos_data = json.loads(response.read())
            response.close()
            return Vector.from_dict(pos_data['Pose']['Position']), Quaternion.from_dict(pos_data['Pose']['Orientation'])

        else:
            raise self.UnexpectedResponse(response)

    def get_laser_scan(self):
        """Requests the current laser scan from the MRDS server and parses it into a dict"""
        self.__mrds.request('GET', '/lokarria/laser/echoes')
        response = self.__mrds.getresponse()
        if response.status == 200:
            laser_data = response.read()
            response.close()
            return json.loads(laser_data)
        else:
            return self.UnexpectedResponse(response)

    def get_laser_scan_angles(self):
        """Requests the current laser properties from the MRDS server and parses it into a dict"""
        self.__mrds.request('GET', '/lokarria/laser/properties')
        response = self.__mrds.getresponse()
        if response.status == 200:
            laser_data = response.read()
            response.close()
            properties = json.loads(laser_data)
            beamCount = int((properties['EndAngle'] - properties['StartAngle']) / properties['AngleIncrement'])
            a = properties['StartAngle']  # +properties['AngleIncrement']
            angles = []
            while a <= properties['EndAngle']:
                angles.append(a)
                a += pi / 180  # properties['AngleIncrement']
            # angles.append(properties['EndAngle']-properties['AngleIncrement']/2)
            return angles
        else:
            raise self.UnexpectedResponse(response)

    def travel(self, cur_pos, tar_pos, lin_spd, ang_spd, delta_pos=1.0):
        """
        Routine to travel at given speed to targeted position until nearby enough. at given speeds at given speeds
        :param cur_pos: current position of the robot
        :type cur_pos: Vector
        :param tar_pos: targeted position to travel to
        :type lin_spd:

        """
        slp_dur = delta_pos / (lin_spd * 1000)
        response = self.post_speed(ang_spd, lin_spd)
        sleep(slp_dur)
        try:
            while cur_pos.distance_to(tar_pos) > delta_pos:
                cur_pos = self.get_pos()
                sleep(slp_dur)

        except self.UnexpectedResponse as ex:
            print('Unexpected response from server when sending speed commands:', ex)

        self.stop()

    def get_lin_spd(self):#, cur_time, tar_time, cur_pos, tar_pos):
        """
            Computes the linear speed by using timestamps coded in the path
        """
        # cur_time = pos_path[i-step][1]
        # tar_time = pos_path[i][1]
        # return cur_pos.distance_to(tar_pos) / ((tar_time - cur_time) * 1000)
        return 1


    def fixed_pure_pursuit(self, pos_path, step=10):
        """
            Implements the pure pursuit algorithm with a fixed lookahead (step parameter).
            The robot aims for "step" position ahead on the path.
            Various values of step and lin_spd
            :param pos_path: list of Vector
            :type pos_path: list
            :param step: lookahead value, i.e the number of positions skipped
            :type step: int
        """
        for i in range(0, len(pos_path), step):
            # cur_time = pos_path[i-step][1]
            # tar_time = pos_path[i][1]
            # lin_spd = cur_pos.distance_to(tar_pos) / ((tar_time - cur_time) * 1000)
            lin_spd = self.get_lin_spd()
            cur_pos, cur_rot = self.get_pos_and_orientation()
            self.travel(cur_pos, pos_path[i], lin_spd, PurePursuit.get_ang_spd(cur_pos, cur_rot, pos_path[i], lin_spd))


    def optimized_pure_pursuit(self, pos_path):
        """
            Implements the pure pursuit algorithm using obstacle detection to aim for the furthest position possible.

            Various values of step and lin_spd
            :param pos_path: path loaded into Vector
            :type pos_path: list
            :
        """
        i = 0
        while (i < len(pos_path)):
            cur_pos, cur_rot = self.get_pos_and_orientation()
            i = self.next_optimized_waypoint(cur_pos, cur_rot, pos_path, i)

            print("Target position path index: {}".format(i))
            lin_spd = self.get_lin_spd()
            self.travel(cur_pos, pos_path[i], lin_spd, PurePursuit.get_pure_pursuit_ang_spd(cur_pos, cur_rot, pos_path[i], lin_spd))


    def next_optimized_waypoint(self, cur_pos, cur_rot, pos_path, cur_i):
        """
            Returns the furthest point from path without an obstacle. Stops at the first position where the laser of nearest
            angle (laser angle ~= aimed position angle) detects an obstacle (laser distance < aimed position distance).
            :param pos_path: path loadsed into Vector
            :param type: list
            :param step: lookahead value, i.e the number of positions skipped

        """
        lasers_angles = self.get_laser_scan_angles()
        lasers = self.get_laser_scan()['Echoes']

        for i in range(cur_i, len(pos_path)):
            tar_pos = pos_path[i]

            rcs_tar_pos = tar_pos.convert_to_rcs(cur_pos, cur_rot)

            rcs_origin = Vector(0, 0, 0)

            tar_angle = rcs_origin.get_angle(rcs_tar_pos)

            min_ind = 0
            min = tar_angle - lasers_angles[0]
            # search for the nearest angle in laser_angles
            # could be simplified with a calculation instead of this iteration
            for j in range(1, len(lasers_angles)):
                dist = tar_angle - lasers_angles[j]
                if dist < min:
                    min = dist
                    min_ind = j

            if lasers[min_ind] < cur_pos.distance_to(tar_pos):
                # if the laser hits an obstacle, return the index of the previous position on the path
                return i - 1
        return len(pos_path) - 1

    def stop(self):
        self.post_speed(0, 0)
