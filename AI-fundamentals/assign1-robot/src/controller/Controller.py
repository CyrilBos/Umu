import http.client
import json
from math import atan2, cos, sin, pow, sqrt, pi
from time import sleep

from model import Vector, Quaternion


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
        """Reads the current position and orientation from the MRDS"""
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

    def pure_pursuit(self, pos_path, step=10, delta_pos=0.1):
        for i in range(0, len(pos_path), step):
            cur_pos, cur_rot = self.get_pos_and_orientation()
            cur_time = pos_path[i-step][1]
            tar_pos  = pos_path[i][0]
            tar_time = pos_path[i][1]

            print('Target position: {}'.format(tar_pos))
            print('Current position: {}'.format(cur_pos))

            angle = 2 * atan2(cur_rot.z, cur_rot.w)
            print('Angle: {}'.format(angle))

            rcs_tar_pos = Vector(0,0,tar_pos.z)
            rcs_tar_pos.x = (tar_pos.x - cur_pos.x) * cos(angle) + (tar_pos.y - cur_pos.y) * sin(angle)
            rcs_tar_pos.y = ((tar_pos.y - cur_pos.y) - (rcs_tar_pos.x * sin(angle))) / cos(angle)

            lin_spd = 0.75#cur_pos.distance_to(tar_pos) / ((tar_time - cur_time) * 1000)
            ang_spd = lin_spd / ((pow(rcs_tar_pos.x, 2) + pow(rcs_tar_pos.y, 2)) / (2 * rcs_tar_pos.y))

            print('Angular speed: {}'.format(ang_spd))

            slp_dur = delta_pos/(lin_spd*1000)
            try:
                response = self.post_speed(ang_spd, lin_spd)
                sleep(slp_dur)
                cur_pos = self.get_pos()
                sleep(slp_dur)
                while pow(cur_pos.distance_to(tar_pos), 2) > delta_pos:
                    cur_pos = self.get_pos()
                    sleep(slp_dur)

            except self.UnexpectedResponse as ex:
                print('Unexpected response from server when sending speed commands:', ex)

        self.stop()




        """
        for i in range(len(pos_path)):
            cur_pos, cur_rot = self.get_pose_and_heading()
            cur_heading = cur_rot.heading()
            tar_rot = rot_path[0].heading()
            while cur_rot != tar_rot:
                self.rotate_to(tar_rot)
                while cur_pos != pos_path[i]:
                    print('Current position: {}\nTarget position: {}'.format(cur_pos, pos_path[i]))
                    try:
                        response = self.post_speed(0.0, 0.4)
                        cur_pos, cur_rot = self.get_pose_and_heading()
                    except self.UnexpectedResponse as ex:
                        print('Unexpected response from server when sending speed commands:', ex)
        """

    def stop(self):
        self.post_speed(0, 0)
