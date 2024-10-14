# this file contains functions for data that will be sent from the pi to the client
import socket
import json
import picar_4wd as fc
# import BotMobile.Lab2.frontend_tutorial.pi_temp as pi_temp 
import pi_temp
import threading
import time

HOST = "192.168.1.32"  # IP address of your Raspberry PI
PORT = 65432           # Port to listen on (non-privileged ports are > 1023)

STOP = "STOP"
FORWARD = "FORWARD"
BACKWARD = "BACKWARD"
LEFT = "LEFT"
RIGHT = "RIGHT"
SPEED = 0
# global DATAFORCLIENT 
DATAFORCLIENT = {
    "Direction" : "Stopped", 
    "PI_Temp" : 0.0,
    "Speed" : "100",
    "Distance": "",  
}

def set_power(SPEED):
    global DATAFORCLIENT
    power = SPEED 
    DATAFORCLIENT["Speed"] = SPEED
    print(f"power is now {power}")

def get_pi_temperature():
    global DATAFORCLIENT
    temp = pi_temp.get_temp()
    DATAFORCLIENT["PI_Temp"] = temp
    
def get_ultrasonic_distance():
    global DATAFORCLIENT
    DATAFORCLIENT["Distance"] = fc.get_distance_at(0)

def car_action(action, power):
    
    global DATAFORCLIENT
    # STOP_BOOL = False
    if(action == STOP):
        fc.stop()
        DATAFORCLIENT["Direction"] = "Stopped"

    elif(action == FORWARD):
        fc.forward(power)
        DATAFORCLIENT["Direction"] = "Forwards"

    elif(action == LEFT):
        fc.turn_left(power)
        DATAFORCLIENT["Direction"] = "Turning Left"

    elif(action == RIGHT):
        fc.turn_right(power)
        DATAFORCLIENT["Direction"] = "Turning Right"

    elif(action == BACKWARD):
        fc.backward(power)
        DATAFORCLIENT["Direction"] = "Backwards"

    elif(type(action) == int):
        set_power(action)

def processData(data, power):
    decoded_data = data.decode("utf-8").strip()

    if decoded_data == STOP:
        print(f"Received {STOP} command")
        car_action(STOP, power)

    elif decoded_data == FORWARD:
        print(f"Received {FORWARD} command")
        car_action(FORWARD, power)
    elif decoded_data == LEFT:
        print(f"Received {LEFT} command")
        car_action(LEFT, power)
    elif decoded_data == RIGHT:
        print(f"Received {RIGHT} command")
        car_action(RIGHT, power)  
    elif decoded_data == BACKWARD:
        print(f"Received {BACKWARD} command")
        car_action(BACKWARD, power)                     
    else:
        try:
            speed = int(decoded_data)
            car_action(min(max(speed, 0), 100), power)
            return min(max(speed, 0), 100)

        except ValueError:
            print("failed to decode data as speed")
            pass

        print(f"Received data: {decoded_data}")

    return power

def send_data_to_pi(client):
    global DATAFORCLIENT
    with client:
        while True:
            get_pi_temperature()
            get_ultrasonic_distance()
            JSONDATAFORCLIENT = json.dumps(DATAFORCLIENT)
            client.sendall(JSONDATAFORCLIENT.encode('utf-8')) # Echo back to client
            time.sleep(1)

def receive_data_from_pi(client):
    power = 100
    with client:
        while True:
            data = client.recv(1024)
            if not data:
                # print("Client disconnected:", clientInfo)
                break
            
            power = processData(data, power)

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Server listening on {HOST}:{PORT}")
        
        try:
            while True:
                client, clientInfo = s.accept()
                recv_thread = threading.Thread(target=receive_data_from_pi, args=(client,))
                recv_thread.start()

                # # Start a thread to handle sending data
                send_thread = threading.Thread(target=send_data_to_pi, args = (client,))
                send_thread.start()

                # # Wait for both threads to finish
                recv_thread.join()
                send_thread.join()

                # print("Connected by:", clientInfo)
                # with client:
                #     while True:
                #         data = client.recv(1024)
                #         if not data:
                #             print("Client disconnected:", clientInfo)
                #             break
                        
                #         power = processData(data, power)

                #         print("Received data:", data)
                #         get_pi_temperature()
                #         JSONDATAFORCLIENT = json.dumps(DATAFORCLIENT)
                #         client.sendall(JSONDATAFORCLIENT.encode('utf-8')) # Echo back to client

        except KeyboardInterrupt:
            print("Closing socket")
            client.close()
            s.close() 
        except ConnectionError as e:
            print(f"Connection error: {e}")
            client.close()
            s.close() 

if __name__ == "__main__":
    start_server()
