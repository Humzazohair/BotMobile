# Handles the ultrasonic 
import picar_4wd as fc
import numpy as np
import time
import math

DEBUG_MODE = False
# Set to 91 to ensure we sweep to 90 degrees (range is non-inclusive)
MAX_ANGLE = 91
MIN_ANGLE = -90

STEP_SIZE = 5

STEP_PAUSE = 0.2

ROBOT_X  = 50
ROBOT_Y = 0

# Defines 50 x 50 grid
GRID_SIZE = 100




###### High level Overview ######
# Sweep Surroundings to get distances at angles (polar coordinates)
# Convert Polar coordinates to Cartesian Coordinates
# 
def sweepSurroundings():
    distances = []
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

def plotPointInGrid(grid, point):
    # Point stored as (x, y)
    # Size of grid assumed to be 100x100
    x, y = point
    if  0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE:        
        grid[GRID_SIZE - 1 - y, x] = True

def distanceBetweenPoints(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

# Interpolates between two points using the slope 
def interpolatePointsUsingSlope(point1, point2):
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
    grid_size = grid.shape[0]  # Assuming grid is a square

    # Calculate the boundaries of the padding box
    min_x = max(x - padding, 0)
    max_x = min(x + padding, grid_size - 1)
    min_y = max(y - padding, 0)
    max_y = min(y + padding, grid_size - 1)

    # Set the padding region to 1
    for dy in range(min_y, max_y + 1):
        for dx in range(min_x, max_x + 1):
            grid[grid_size - 1 - dy, dx] = 1  # Flip y to match your previous logic

    return grid

# Main function for main.py with Ultrasonic data only
def ultrasonicToTwoDim():
    hit_grid = np.zeros((GRID_SIZE, GRID_SIZE))
    hit_list = sweepSurroundings()

    hit_list_cartesian = []
    for i in range(len(hit_list)):
        angle = MIN_ANGLE + i * STEP_SIZE
        hit_coordinates = convertHitToCartesian(angle, hit_list[i])
        hit_list_cartesian.append(hit_coordinates)

    for i in range(len(hit_list_cartesian) - 1):
        point1 = hit_list_cartesian[i]
        point2 = hit_list_cartesian[i + 1]
        distance = distanceBetweenPoints(point1, point2)

        # Check for              
        p1 = hit_list[i]
        p2 = hit_list[i + 1]
        if distance <= 4:
            interpolated_points = interpolatePointsUsingSlope(point1, point2)
            
            for point in interpolated_points:
                plotPointInGrid(hit_grid, point)
                pad_hit(hit_grid, point)  # Pad around each interpolated point

        else:
            plotPointInGrid(hit_grid, point1)
            pad_hit(hit_grid, point1)  # Pad around hit1
            
            plotPointInGrid(hit_grid, point2)
            pad_hit(hit_grid, point2)  # Pad around hit2
    
    for i in range(40,60):
        for j in range(90,100):
                hit_grid[0 + j][0 + i] = 0

    if DEBUG_MODE:
        np.savetxt('BumzaScripts/data/mapping.txt', hit_grid, fmt="%d", delimiter="")

    print(hit_list_cartesian)
    
    return hit_grid


if __name__ == '__main__':
    ultrasonicToTwoDim()

    # interpolatePointsUsingSlope()
    # print(interpolatePointsUsingSlope((1,1), (8,8)))
    # print(sweepSurroundings())
    # angle = 90
    # dist = fc.get_distance_at(angle)
    # spot_x = ROBOT_X + (np.sin(np.radians(angle)) * dist * -1) 
    # spot_y = ROBOT_Y + (np.cos(np.radians(angle)) * dist) 
    # print(convertHitToCartesian(angle, dist))         
    # print(spot_x, spot_y)

    # point_to_plot = (50, 0)
    # hit_grid = np.zeros((100, 100), dtype=bool)
    # hit_grid[99 - point_to_plot[1], point_to_plot[0]] = 1
    # plotPointInGrid(hit_grid, point_to_plot)
    # np.savetxt('BumzaScripts/data/mapping.txt', hit_grid, fmt="%d")

    # print("got here")



    

