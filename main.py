import asyncio
import mapping  # assuming you renamed the sensor file
import numpy as np
import heapq
import time
import picar_4wd as fc
import object_detection
from threading import Thread
import astar as ass

stop_signal = False  # Flag to indicate if the robot should stop
person = False

# async def run_object_detection():
#     global stop_signal, person
#     while True:
#         # Run the object detection
#         results = object_detection.run(
#             model='/home/bumza/picar-4wd/BumzaScripts/efficientdet_lite0.tflite',
#             max_results=5,
#             score_threshold=0.3,
#             camera_id=2,
#             width=1280,
#             height=720,
#             detection_callback=None
#         )

#         # Check for specific objects
#         for objects in results.detection_result_list:
#             if objects == "stop sign":
#                 stop_signal = True
#                 fc.stop() # Stop the car immediately
#                 time.sleep(3) 
#                 print("Detected:", objects)
#                 break
#             if objects == "person":
#                 fc.stop()
#                 print("Detected:", objects)
#                 break

#         await asyncio.sleep(1)  # Wait before next detection

def main():
    # global ass.CAR_X, ass.CAR_Y

    # Start the object detection in a separate thread
    # Thread(target=asyncio.run, args=(run_object_detection(),)).start()
    next_while = False
    while True:
        grid = mapping.ultrasonicToTwoDim()
        path = ass.run_a_star(grid, (ass.CAR_Y, ass.CAR_X), (ass.GOAL_Y, ass.GOAL_X))
        
        if path:
            for y, x in path:
                grid[y][x] = 2

            np.savetxt('BumzaScripts/data/mapping.txt', grid, fmt="%d", delimiter="")


            move_path = ass.path_to_moves(path)
            for move in move_path:
                ass.move_in_path(move)
                # if stop_signal:
                #     next_while = True
                #     print("Stopping due to detection.")
                #     break  # Exit the move loop if stop signal is set
                # if person:
                #     next_while = True
                #     print("Stopping due to detection.")
                #     break  # Exit the move loop if stop signal is set

                # if CM_COUNTER >= 100:  # Example limit for total distance
                #     print("Goal reached based on CM_COUNTER.")
                #     fc.stop()
                #     return
            if next_while:
                continue
        else:
            print("No path found.")
            break

if __name__ == "__main__":
    main()
