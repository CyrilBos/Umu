import http.client
import json
from math import atan2, cos, sin, pow, sqrt, pi
from time import sleep

from model import Vector, Quaternion
from model import pure_pursuit


class Controller:
    """
        This is the Controller base class containing methods to send requests to the MRDS server
    """
    class UnexpectedResponse(Exception):
        pass

    def __init__(self, mrds_url, headers, lin_spd=1.0, delta_pos=0.75):
        """
            Initializes a new instance of Controller.
            :param mrds_url: url which the MRDS server listens on
            :type mrds_url: str
            :param headers: headers to send with every request sent to the MRDS server
            :type headers: str
            :param lin_spd:
            :type lin_spd: float
            :param step:
            :type step: int
            :param delta_pos:
            :type delta_pos: float

        """
        self.__mrds = http.client.HTTPConnection(mrds_url)
        self.__headers = headers
        self._lin_spd = lin_spd
        self._delta_pos = delta_pos

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

    def travel(self, cur_pos, tar_pos, lin_spd, ang_spd, delta_pos=1):
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




    def stop(self):
        self.post_speed(0, 0)
