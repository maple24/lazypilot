import socket

class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.host, self.port))

    def start(self):
        try:
            while True:
                message = input("Enter message to send (type 'exit' to quit): ")
                if message.lower() == "exit":
                    break
                self.client_socket.sendall(message.encode())
                
                data = self.client_socket.recv(1024)
                if not data:
                    print("Server closed the connection.")
                    break
                print(f"Received from server: {data.decode()}")

        except ConnectionResetError:
            print("Server closed the connection unexpectedly.")
        except KeyboardInterrupt:
            print("Connection closed by the user.")
        finally:
            self.client_socket.close()

if __name__ == "__main__":
    host = "127.0.0.1"  # Change this to the server's IP address
    port = 12345
    client = Client(host, port)
    client.start()
