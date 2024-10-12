# main.py located in the current directory
import sys
import os

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import mapping

DEBUG_FILE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/data/"

# Tests convertHitToCartesian(angle, hit_distance)
def test_cartesian_convert():

    angle = -30
    distance = 10
    expected_y = 8
    expected_x = 55

    expected = (expected_x, expected_y) 
    assert expected == mapping.convertHitToCartesian(angle, distance)

# Tests plotPointInGrid(grid, point)
def test_plot_point():
    
    expected_grid = np.zeros((100,100))
    expected_grid[99][50] = 1
    expected_grid[0][0] = 1

    grid = np.zeros((100, 100))
    mapping.plotPointInGrid(grid, (50, 0))
    mapping.plotPointInGrid(grid, (0, 99))
    assert np.array_equal(expected_grid, grid)

# Tests distanceBetweenPoints(point1, point2)
def test_distance_between():
    point1 = (5, 9)
    point2 = (17, 14)

    expectedDistance = 13
    actualDistance = mapping.distanceBetweenPoints(point1, point2)

    assert expectedDistance == actualDistance

# Tests interpolatePointsUsingSlope(point1, point2)
def test_interpolate():
    start = (1, 1)
    end = (9, 9)

    expected_points = [(i, i) for i in range(1, 10)]
    actual_points = mapping.interpolatePointsUsingSlope(start, end)
    reversed_points = mapping.interpolatePointsUsingSlope(end, start)

    assert expected_points == actual_points
    assert expected_points == reversed_points

    start = (1, 1)
    end = None
    assert [start] == mapping.interpolatePointsUsingSlope(start, end)
    assert [start] == mapping.interpolatePointsUsingSlope(end, start)

# Tests pad_hit(grid, point, padding = 8)
def test_pad_hit():
    expected_grid = np.zeros((100, 100))
    point1 = (40, 60)
    point1_padding = 4
    for i in range(36, 45):
        for j in range(56, 65):
            mapping.plotPointInGrid(grid = expected_grid, point = (i, j))
    
    grid = np.zeros((100, 100))
    grid = mapping.pad_hit(grid = grid, point = point1, padding = point1_padding)

    mapping.plotPointInGrid(expected_grid, point1, 2)
    mapping.plotPointInGrid(grid, point1, 2)    
    # np.savetxt(DEBUG_FILE_PATH + "expected.txt", expected_grid, fmt="%d", delimiter="")
    # np.savetxt(DEBUG_FILE_PATH + "actual.txt", grid, fmt="%d", delimiter="")

    assert np.array_equal(expected_grid, grid)

# Not really a test
def test_interpolate_and_pad():

    grid = np.zeros((100, 100))

    point1 = (40, 60)
    point2 = (70, 80)
    interpolated_points = mapping.interpolatePointsUsingSlope(point1, point2)
            
    for point in interpolated_points:
        mapping.plotPointInGrid(grid, point)
        # pad_hit(hit_grid, point)  # Pad around each interpolated point
    

    np.savetxt(DEBUG_FILE_PATH + "interpolated_unpadded.txt", grid, fmt="%d", delimiter="")
    
    for point in interpolated_points:
        # mapping.plotPointInGrid(grid, point)
        mapping.pad_hit(grid, point)  # Pad around each interpolated point
    np.savetxt(DEBUG_FILE_PATH + "interpolated_padded.txt", grid, fmt="%d", delimiter="")


mapping.ultrasonicToTwoDim()

# test_interpolate_and_pad()