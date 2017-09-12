"""
Example demonstrating how to communicate with Microsoft Robotic Developer
Studio 4 via the Lokarria http interface. 

Author: Erik Billing (billing@cs.umu.se)

Updated by Ola Ringdahl 204-09-11
"""

MRDS_URL = 'localhost:50000'

import http.client, json, time
from math import sin, cos, pi, atan2
from maths import Vector
from maths import Quaternion

HEADERS = {"Content-type": "application/json", "Accept": "text/json"}


class UnexpectedResponse(Exception): pass


def postSpeed(angularSpeed, linearSpeed):
    """Sends a speed command to the MRDS server"""
    mrds = http.client.HTTPConnection(MRDS_URL)
    params = json.dumps({'TargetAngularSpeed': angularSpeed, 'TargetLinearSpeed': linearSpeed})
    mrds.request('POST', '/lokarria/differentialdrive', params, HEADERS)
    response = mrds.getresponse()
    status = response.status
    # response.close()
    if status == 204:
        return response
    else:
        raise UnexpectedResponse(response)


def getLaser():
    """Requests the current laser scan from the MRDS server and parses it into a dict"""
    mrds = http.client.HTTPConnection(MRDS_URL)
    mrds.request('GET', '/lokarria/laser/echoes')
    response = mrds.getresponse()
    if (response.status == 200):
        laserData = response.read()
        response.close()
        return json.loads(laserData)
    else:
        return response


def getLaserAngles():
    """Requests the current laser properties from the MRDS server and parses it into a dict"""
    mrds = http.client.HTTPConnection(MRDS_URL)
    mrds.request('GET', '/lokarria/laser/properties')
    response = mrds.getresponse()
    if (response.status == 200):
        laserData = response.read()
        response.close()
        properties = json.loads(laserData)
        beamCount = int((properties['EndAngle'] - properties['StartAngle']) / properties['AngleIncrement'])
        a = properties['StartAngle']  # +properties['AngleIncrement']
        angles = []
        while a <= properties['EndAngle']:
            angles.append(a)
            a += pi / 180  # properties['AngleIncrement']
        # angles.append(properties['EndAngle']-properties['AngleIncrement']/2)
        return angles
    else:
        raise UnexpectedResponse(response)


def getPoseAndOrientation():
    """Reads the current position and orientation from the MRDS"""
    mrds = http.client.HTTPConnection(MRDS_URL)
    mrds.request('GET', '/lokarria/localization')
    response = mrds.getresponse()
    if (response.status == 200):
        poseData = json.loads(response.read())
        response.close()
        return Vector.from_dict(poseData['Pose']['Position']), Quaternion.from_dict(poseData['Pose']['Orientation'])
    else:
        return UnexpectedResponse(response)


if __name__ == '__main__':
    print('Sending commands to MRDS server', MRDS_URL)
    try:
        print('Telling the robot to go streight ahead.')
        response = postSpeed(0, 0.1)
        print('Waiting for a while...')
        time.sleep(3)
        print('Telling the robot to go in a circle.')
        response = postSpeed(0.4, 0.1)
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
            pose, orientation = getPoseAndOrientation()
            heading = orientation.heading()
            print('Current heading vector: X:{}, Y:{}'.format(heading.x, heading.y))
            time.sleep(1)
    except UnexpectedResponse as ex:
        print('Unexpected response from server when reading position:', ex)