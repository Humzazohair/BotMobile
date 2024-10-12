import mapping  # assuming you renamed the sensor file
import numpy as np
import time
import picar_4wd as fc
import object_detection
from threading import Thread, Lock, Event
import astar as ass
import socket


stop_signal = False  # Flag to indicate if the robot should stop

person = False
person_lock = Lock()

seen_stop_once = False
stop_sign = False
stop_sign_lock = Lock()


HALT = False
object_detection_results = []

host = socket.gethostname()
port = 8060  # initiate port no above 1024

def update_results(detection_result_list):
    global object_detection_results
    object_detection_results = detection_result_list


def run_object_detection(e):

    object_detection.run(
        model='/home/bumza/picar-4wd/BumzaScripts/efficientdet_lite0.tflite',
        max_results=5,
        score_threshold=0.3,
        camera_id="/dev/video2",
        width=1280,
        height=720,
        detection_callback=update_results,
        event = e
    )


def OBJDETECT(event):
    global person, stop_sign, seen_stop_once

    server_socket = socket.socket()  # get instance

    server_socket.bind((host, port))  # bind host address and port together

    # configure how many client the server can listen simultaneously
    server_socket.listen(2)
    print("server started")
    event.set()
    conn, address = server_socket.accept()  # accept new connection
    print("Connection from cv")
    try:
        while True:
            # receive data stream. it won't accept data packet greater than 1024 bytes
            data = conn.recv(1024).decode()
            if not data:
                # if data is not received break
                break
            data = str(data)

            res = data.split(",")
            try:
                object, confidence = res[0], float(res[1])
            except ValueError:
                continue
                
            # Person is detected case
            if object.strip().lower() == "person" and confidence > 0.6:
                print(f"Detected a person with confidence {confidence}!")
                with person_lock:
                    person = True
                time.sleep(2)

            # Person is not detected case
            else:
                with person_lock:
                    person = False

            # Stop Sign is detected case
            if object.strip().lower() == "stop sign" and confidence > 0.5 and not seen_stop_once:
                print(f"Detected a stop sign with confidence {confidence}!")
                time.sleep(1)
                seen_stop_once = True
                with stop_sign_lock:
                    stop_sign = True
                time.sleep(2)
            
    finally:
        conn.close()

def scan_and_astar():

    grid = mapping.ultrasonicToTwoDim()
    path = ass.run_a_star(grid, start=(ass.CAR_Y, ass.CAR_X), goal=(ass.GOAL_Y, ass.GOAL_X))
    # Adds path to grid if path exists
    if(path):
        for y, x in path:
            grid[y][x] = 2
        np.savetxt(mapping.DEBUG_FILE_PATH, grid, fmt="%d", delimiter="")

    return path, grid

def scan_map_move():
    global stop_sign
    global person

    while True:
        path, grid = scan_and_astar()

        move_path = ass.path_to_moves(path)

        prev_move = 'move_forward'
        seq = []
        times = 0
        for move in move_path:
            if move["action"] == 'move_forward':
                times += 1
            else:
                seq.append(f"{prev_move} {times} times")
                times = 0
                seq.append(f"{move['action']} {move['direction']}")

        print(seq)
        for i, move in enumerate(move_path):

            while person:
                fc.stop()
                time.sleep(5)

            # if there is a stop sign: stop wait two seconds, avoid,
            if stop_sign:
                fc.stop()
                time.sleep(3)
                with stop_sign_lock:
                    stop_sign = False

            if (i % 80 == 60):
                scan_and_astar()
            # move if there is no stop sign or person
            ass.move_in_path(move)


        print("FINISHED FIRST A STAR")
        exit()


def main():

    try:
        # this event activates when the server is online
        e = Event()
        object_detection_thread = Thread(target=OBJDETECT, args=(e,))
        cv_thread = Thread(target=run_object_detection, args=(e,))
        movement_thread = Thread(target=scan_map_move)

        object_detection_thread.start()
        cv_thread.start()
        movement_thread.start()
    finally:
        HALT = True

    cv_thread.join()
    object_detection_thread.join()
    movement_thread.join()

if __name__ == "__main__":
    try:
        main()
    finally:
        fc.stop()
