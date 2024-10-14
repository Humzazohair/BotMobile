# this file contains functions for data that will be sent from the pi to the client
import socket
import json
# import picar_4wd as fc

HOST = "192.168.1.32"  # IP address of your Raspberry PI
PORT = 65432           # Port to listen on (non-privileged ports are > 1023)
STOP = "STOP"
FORWARD = "FORWARD"
BACKWARD = "BACKWARD"
LEFT = "LEFT"
RIGHT = "RIGHT"
POWER = 100
DATAFORCLIENT = {
    "Distance" : 0, 
    "Balaji" : "Gay"  
                }

def car_action(action):
    # if(action == STOP):
    #     fc.stop()
    # elif(action == FORWARD):
    #     fc.forward(POWER)
    # elif(action == LEFT):
    #     fc.turn_left(POWER)
    # elif(action == RIGHT):
    #     fc.turn_right(POWER)
    # elif(action == BACKWARD):
    #     fc.backward(POWER)
    pass

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Server listening on {HOST}:{PORT}")

        try:
            while True:
                client, clientInfo = s.accept()
                print("Connected by:", clientInfo)
                with client:
                    while True:
                        data = client.recv(1024)
                        if not data:
                            print("Client disconnected:", clientInfo)
                            break
                        decoded_data = data.decode("utf-8").strip()
                        # Check if the data is "UP"
                        if decoded_data == STOP:
                            print(f"Received {STOP} command")
                            car_action(STOP)

                        if decoded_data == FORWARD:
                            print(f"Received {FORWARD} command")
                            car_action(FORWARD)
                            DATAFORCLIENT["Distance"] += 1
                        if decoded_data == LEFT:
                            print(f"Received {LEFT} command")
                            car_action(LEFT)
                        if decoded_data == RIGHT:
                            print(f"Received {RIGHT} command")
                            car_action(RIGHT)  
                        if decoded_data == BACKWARD:
                            print(f"Received {BACKWARD} command")
                            car_action(BACKWARD)                     
                        else:
                            print(f"Received data: {decoded_data}")

                        

                        print("Received data:", data)
                        JSONDATAFORCLIENT = json.dumps(DATAFORCLIENT)
                        client.sendall(JSONDATAFORCLIENT) # Echo back to client

        except:
            print(f"An error occurred: ")
            print("Closing socket")
            client.close()
            s.close() 

if __name__ == "__main__":
    start_server()
