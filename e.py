

import random
import numpy as np
import matplotlib.pyplot as plt

class Vehicle2D(object):
    def __init__(self, length=10.0):
        """
        Creates 2D vehicle model and initializes location (0,0) & orientation 0.
        """
        self.x = 0.0
        self.y = 0.0
        self.orientation = 0.0
        self.length = length
        self.steering_noise = 0.0
        self.distance_noise = 0.0
        self.steering_drift = 0.0

    def set(self, x, y, orientation):
        """
        Sets the vehicle coordinates and orientation.
        """
        self.x = x
        self.y = y
        self.orientation = orientation % (2.0 * np.pi)

    def set_noise(self, steering_noise, distance_noise):
        """
        Sets the noise parameters.
        """
        self.steering_noise = steering_noise
        self.distance_noise = distance_noise

    def set_steering_drift(self, drift):
        """
        Sets the systematical steering drift parameter
        """
        self.steering_drift = drift

    def move(self, steering, distance, tolerance=0.001, max_steering_angle=np.pi / 4.0):
        """
        steering = front wheel steering angle, limited by max_steering_angle (max 45 degrees)
        distance = total distance driven, must be non-negative
        """
        if steering > max_steering_angle:
            steering = max_steering_angle
        if steering < -max_steering_angle:
            steering = -max_steering_angle
        if distance < 0.0:
            distance = 0.0

        # apply noise
        steering2 = random.gauss(steering, self.steering_noise)
        distance2 = random.gauss(distance, self.distance_noise)

        # apply steering drift
        steering2 += self.steering_drift

        # Execute motion
        turn = np.tan(steering2) * distance2 / self.length

        if abs(turn) < tolerance:
            # approximate by straight line motion
            self.x += distance2 * np.cos(self.orientation)
            self.y += distance2 * np.sin(self.orientation)
        else:
            # approximate bicycle model for motion
            radius = distance2 / turn
            cx = self.x - (np.sin(self.orientation) * radius)
            cy = self.y + (np.cos(self.orientation) * radius)
            self.orientation = (self.orientation + turn) % (2.0 * np.pi)
            self.x = cx + (np.sin(self.orientation) * radius)
            self.y = cy - (np.cos(self.orientation) * radius)

    def compute_error(self, track):
        # Compute the closest distance to the track and the CTE
        closest_dist = float('inf')
        closest_index = 0
        for i in range(len(track)):
            dist = np.linalg.norm(np.array([self.x, self.y]) - np.array(track[i]))
            if dist < closest_dist:
                closest_dist = dist
                closest_index = i

        closest_point = track[closest_index]
        error = self.y - closest_point[1]
        return error

    def run_PID(self, track, K_p, K_d, K_i, n=500, speed=1.0):
        x_trajectory = []
        y_trajectory = []

        prev_error = self.compute_error(track)
        cumulative_error = 0
        for _ in range(n):
            current_error = self.compute_error(track)
            cumulative_error += current_error
            diff = current_error - prev_error
            prev_error = current_error
            steer = -K_p * current_error - K_d * diff - K_i * cumulative_error
            self.move(steer, speed)
            x_trajectory.append(self.x)
            y_trajectory.append(self.y)

        return x_trajectory, y_trajectory

    def __repr__(self):
        return '[x=%.5f y=%.5f orient=%.5f]' % (self.x, self.y, self.orientation)

# Initialize vehicle
vehicle = Vehicle2D()
vehicle.set(0, 1, 0)
vehicle.set_steering_drift(10 / 180. * np.pi)

# Define the track
track_length = 1000
targets = []
track_x = []
track_y = []
for i in range(300):
    targets.append([i, 0])
    track_x.append(i)
    track_y.append(0)
for i in range(300, 600):
    targets.append([i, 2])
    track_x.append(i)
    track_y.append(2)
for i in range(600, track_length):
    targets.append([i, 0])
    track_x.append(i)
    track_y.append(0)

# PID controller parameters
K_p = 0.1
K_d = 3.0
K_i = 0.0001
x_trajectory, y_trajectory = vehicle.run_PID(targets, K_p, K_d, K_i, track_length)

# Plot the results
fig, ax1 = plt.subplots(1, 1, figsize=(8, 4))
ax1.plot(x_trajectory, y_trajectory, 'g', linewidth=2, label='PID controller')
ax1.plot(track_x, track_y, 'r', label='target')
plt.legend()
plt.show()