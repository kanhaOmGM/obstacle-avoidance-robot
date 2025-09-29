# obstacle-avoidance-robot
Simulating a robot avoiding obstacles using python, and external libraries like numpy and pygame
Robot Obstacle Avoidance Simulator
A Python simulation of a differential drive robot with ultrasonic sensor-based obstacle avoidance.
Requirements

Python 3
pygame
numpy

Usage
Run the simulation:
bashpython main.py
Features

Differential drive kinematics - Two-wheeled robot with independent wheel control
Ultrasonic sensor simulation - 250-pixel range with 40-degree field of view
Obstacle avoidance - Automatic backward curved motion when obstacles detected within 100 pixels
Real-time visualization - pygame-based rendering with sensor ray visualization

Configuration
Main parameters can be adjusted in main.py:
MAP_DIMENSIONS = (600, 1200)  # Window size
start = (100, 200)             # Starting position
sensor = 250, math.radians(40) # Range and FOV
Robot parameters in classes.py:
pythonself.maxspeed = 0.03 * self.m2p  # Maximum speed
self.min_obs_dis = 100           # Obstacle detection threshold
self.count_down = 5              # Avoidance duration (seconds)

The robot continuously:

Scans for obstacles using simulated ultrasonic sensor
Moves forward when path is clear
Executes backward curved motion for 5 seconds when obstacle detected within threshold
Returns to forward motion after avoidance maneuver
