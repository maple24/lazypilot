import socket
import select
import subprocess
from loguru import logger


class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(10)
        self.clients = [self.server_socket]
        logger.info(f"Server listening on {self.host}:{self.port}")

    def start(self):
        while True:
            readable, _, _ = select.select(self.clients, [], [])

            for sock in readable:
                if sock == self.server_socket:
                    conn, addr = self.server_socket.accept()
                    logger.success(f"Connected to {addr}")
                    self.clients.append(conn)
                else:
                    try:
                        data = sock.recv(1024)
                        if not data:
                            logger.info(f"Client {sock.getpeername()} disconnected.")
                            sock.close()
                            self.clients.remove(sock)
                        else:
                            message = data.decode()
                            logger.success(f"Received from {sock.getpeername()}: {message}")
                            self.handle_command(sock, message)
                    except (ConnectionResetError, ConnectionAbortedError):
                        logger.error(
                            f"Client {sock.getpeername()} forcibly closed the connection."
                        )
                        sock.close()
                        self.clients.remove(sock)

    def handle_command(self, sock, message):
        # Implement your command handling logic here
        try:
            if message.startswith("execute:"):
                command = message[len("execute:") :]
                result = subprocess.check_output(command, shell=True)
                self.send_message(sock, result)
            else:
                response = "Invalid command. Please use 'execute:<command>' to execute commands."
                self.send_message(sock, response.encode())
        except Exception as e:
            error_msg = f"Error executing command: {str(e)}"
            self.send_message(sock, error_msg.encode())
    
    def handle_method(self):
        ...

    def send_message(self, sock, message):
        sock.sendall(message)

    def stop(self):
        for client in self.clients:
            client.close()
        self.server_socket.close()


if __name__ == "__main__":
    host = "127.0.0.1"  # Use "0.0.0.0" to listen on all available network interfaces
    port = 12345
    server = Server(host, port)
    try:
        server.start()
    except KeyboardInterrupt:
        print("Server stopped by the user.")
    finally:
        server.stop()
