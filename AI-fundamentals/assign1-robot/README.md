# Genral information
The assignment group is composed of Cyril Bos (cybo0001) and Dorian Cuquemelle (docu0002), international students from ENSEIRB-MATMECA,
France.

The assignment was developed in Python 3(.6) and uses only standard library packages. 


# Usage
The following command will launch the main script controlling the robot using the default values written at the top of 
the main.py file.
> python main.py

Options can be issued as arguments of the script instead of modifying the file: 
> python main.py path=paths/Path-around-table.json --obstacle --level=DEBUG

The --obstacle option enables the obstacle detection algorithm by instantiating an ObstacleController instead of a 
FixedController. 

# Code structure
The code is divided into a module main.py and 2 packages controller and model. 

The package controller contains the classes Controller, FixedController and ObstacleController. Controller offers
methods to interact with the MRDS server (POST request for speed and GET requests of various information) and a travel 
method that monitors the movement of the robot till it reaches a position. 

The FixedController inherits from Controller and implements the Pure Pursuit algorithm with a fixed lookahead.
The ObstacleController also inherits from Controller but implements Pure Pursuit as much as it can

The package model holds a Vector and Quaternion classes as well as a pure_pursuit module. 
These two classes implement various methods needed to implement the path tracking algorithm. 

# Tests
the file unit_tests.py tests our implementation of the quaternion methods by comparing their results with the ones
provided by the professor (file lokarriaexample.py that has been translated to Python 3 with the 2to3 command on linux),
