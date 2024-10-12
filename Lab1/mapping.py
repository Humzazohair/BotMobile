# Handles the ultrasonic 
import picar_4wd as fc
import numpy as np
import time
import math
import os

DEBUG_MODE = True
# Set to 91 to ensure we sweep to 90 degrees (range is non-inclusive)
MAX_ANGLE = 91
MIN_ANGLE = -90

STEP_SIZE = 10

STEP_PAUSE = 0.2

ROBOT_X  = 50
ROBOT_Y = 0

# Defines 50 x 50 grid
GRID_SIZE = 100

DEBUG_FILE_PATH = os.path.dirname(os.path.abspath(__file__)) + "/data/mapping.txt"
THRESHOLD = 100
PADDING = 7

###### High level Overview ######
# Sweep Surroundings to get distances at angles (polar coordinates)
# Convert Polar coordinates to Cartesian Coordinates
# 

def sweepSurroundings():
    distances = []
    fc.set_servo_angle(MIN_ANGLE)
    time.sleep(0.5)
    for angle in range(MIN_ANGLE, MAX_ANGLE, STEP_SIZE):
        dist = fc.get_distance_at(angle)
        distances.append(dist)
        time.sleep(STEP_PAUSE)

    distances = np.array(distances)
    return distances


def convertHitToCartesian(angle, hit_distance):
    radians = np.radians(angle)
    # Scale by -1 due to -90 corresponding to straight right and 
    # 90 degree corresponding to straight left
    x = ROBOT_X + (np.sin(radians) * hit_distance * -1)
    
    y = ROBOT_Y + (np.cos(radians) * hit_distance)

    return (int(x),int(y))

def plotPointInGrid(grid, point, marker = 1):
    # Point stored as (x, y)
    # Size of grid assumed to be 100x100
    x, y = point
    if  0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE:        
        grid[GRID_SIZE - 1 - y, x] = marker

def distanceBetweenPoints(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

# Interpolates between two points using the slope 
def interpolatePointsUsingSlope(point1, point2):
    if(point1 == None or point2 == None):
        return [i for i in [point1, point2] if i != None]
    
    x1, y1 = point1
    x2, y2 = point2
    points = []

    if x1 == x2:  # Vertical line case
        for y in range(min(y1, y2), max(y1, y2) + 1):
            points.append((x1, y))
    else:
        slope = (y2 - y1) / (x2 - x1)
        for x in range(min(x1, x2), max(x1, x2) + 1):
            y = int(y1 + slope * (x - x1))
            points.append((x, y))
    
    return points


def pad_hit(grid, point, padding= 8):
    """Pad the hit grid by adding a square padding around the hit."""
    x, y = point

    # Calculate the boundaries of the padding box
    min_x = max(x - padding, 0)
    max_x = min(x + padding, GRID_SIZE - 1)
    min_y = max(y - padding, 0)
    max_y = min(y + padding, GRID_SIZE - 1)

    for dy in range(min_y, max_y + 1):
        for dx in range(min_x, max_x + 1):
            plotPointInGrid(grid, (dx, dy))  # Flip y to match your previous logic

    return grid

def convertHitsToCartesian(hit_list):
    cartesian_hits = []
    for i in range(len(hit_list)):
        if(hit_list[i] < 0):
            cartesian_hits.append(None)
            continue
        angle = MIN_ANGLE + i * STEP_SIZE
        hit_coordinates = convertHitToCartesian(angle, hit_list[i])
        cartesian_hits.append(hit_coordinates)

    return cartesian_hits

# Main function for main.py with Ultrasonic data only
def ultrasonicToTwoDim():
    hit_grid = np.zeros((GRID_SIZE, GRID_SIZE))

    # Scan around with the ultrasonic sensor to make sure there's no obstacles nearby
    hit_list = sweepSurroundings()
    filtered_hit_list = [hit if hit < THRESHOLD else -2 for hit in hit_list]
    # Convert any hits to cartesian coordinates
    hit_list_cartesian = convertHitsToCartesian(filtered_hit_list)

    for i in range(len(hit_list_cartesian) - 1):
        point1 = hit_list_cartesian[i]
        point2 = hit_list_cartesian[i + 1]

        interpolated_points = interpolatePointsUsingSlope(point1, point2)
        
        if point1 == None or point2 == None or distanceBetweenPoints(point1, point2) > 6:
            if point1 != None: pad_hit(hit_grid, point1, padding = PADDING)
            if point2 != None: pad_hit(hit_grid, point2, padding = PADDING)
        else:
            for point in interpolated_points:
                # Pad around each interpolated point
                pad_hit(hit_grid, point, padding = PADDING)

    if DEBUG_MODE:
        np.savetxt(DEBUG_FILE_PATH, hit_grid, fmt="%d", delimiter="")
    
    return hit_grid


if __name__ == '__main__':
    ultrasonicToTwoDim()




    

