import socket

HOST = "192.168.1.32"  # IP address of your Raspberry PI
PORT = 65432           # Port to listen on (non-privileged ports are > 1023)

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
                        print("Received data:", data)
                        client.sendall(data)  # Echo back to client
        except KeyboardInterrupt:
            print("\nServer shutting down.")
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    start_server()
