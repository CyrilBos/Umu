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
            return json.loads(laser_data)['Echoes']
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

    def next_optimized_waypoint(self, pos_path, cur_i):
        lasers_angles = self.get_laser_scan_angles()
        lasers = self.get_laser_scan()

        for i in range(cur_i, len(pos_path)):
            cur_pos = self.get_pos()
            tar_pos = pos_path[i][0]

            tar_angle = atan2(cur_pos.cross(tar_pos), cur_pos.dot(tar_pos))
            min_ind = 0
            min = tar_angle - lasers_angles[0]
            #search for the nearest angle in laser_angles
            #could be simplified with a calculation instead of this iteration
            for j in range(1, len(lasers_angles)):
                dist = tar_angle - lasers_angles[j]
                if dist < min:
                    min = dist
                    min_ind = j
            if lasers[min_ind] < cur_pos.distance_to(tar_pos):
                #if the laser hits an obstacle, return the index of the previous position on the path
                return i - 1
        return len(pos_path)-1

    def pure_pursuit(self, pos_path, delta_pos=0.1):
        i = 0
        while (i < len(pos_path)):
            i = self.next_optimized_waypoint(pos_path, i)

            print(i)
            cur_pos, cur_rot = self.get_pos_and_orientation()
            tar_pos = pos_path[i]

            print('Target position: {}'.format(tar_pos))
            print('Current position: {}'.format(cur_pos))

            angle = 2 * atan2(cur_rot.z, cur_rot.w)
            print('Angle: {}'.format(angle))

            rcs_tar_pos = Vector(0, 0, tar_pos.z)


            #GP_x
            rcs_tar_pos.x = (tar_pos.x - cur_pos.x) * cos(angle) + (tar_pos.y - cur_pos.y) * sin(angle)
            #GP_y
            rcs_tar_pos.y = ((tar_pos.y - cur_pos.y) - (rcs_tar_pos.x * sin(angle))) / cos(angle)

            lin_spd = 0.75

            #ang_spd = lin_spd / (l^2 / 2y) = lin_spd / r
            ang_spd = lin_spd / ((pow(rcs_tar_pos.x, 2) + pow(rcs_tar_pos.y, 2)) / (2 * rcs_tar_pos.y))

            print('Angular speed: {}'.format(ang_spd))

            #sleep duration between each request = time to travel distance delta_min  at speed lin_spd
            slp_dur = delta_pos / lin_spd
            try:
                self.post_speed(ang_spd, lin_spd)
                sleep(slp_dur)
                cur_pos = self.get_pos()
                sleep(slp_dur)
                while pow(cur_pos.distance_to(tar_pos), 2) > delta_pos: #@Dorian why pow2?
                    cur_pos = self.get_pos()
                    sleep(slp_dur)

            except self.UnexpectedResponse as ex:
                print('Unexpected response from server when sending speed commands:', ex)
            i+=1

        self.stop()


    def stop(self):
        self.post_speed(0, 0)
