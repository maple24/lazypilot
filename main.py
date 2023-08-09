"""
curl -X POST -H "Content-Type: application/json" -d '{"message": "Your message here"}' http://localhost:8000/update_message/
curl -X POST http://localhost:8000/publish/YourMessageHere
"""
from WebCamApp import WebCamApp
from Server import Server
from api import run_fastapi
import multiprocessing
from typing import Optional
import tkinter as tk

# def run_server(queue: Optional[multiprocessing.Queue] = None):
#     host = "127.0.0.1"  # Use "0.0.0.0" to listen on all available network interfaces
#     port = 12345
#     server = Server(host, port)
#     try:
#         server.start()
#     except KeyboardInterrupt:
#         print("Server stopped by the user.")
#     finally:
#         server.stop()


def run_webcam(queue: Optional[multiprocessing.Queue] = None):
    root = tk.Tk()
    WebCamApp(root, proc_q=queue)  # Pass the queue to TkinterApp
    root.mainloop()


if __name__ == "__main__":
    # init process queue
    queue = multiprocessing.Queue()

    # Start FastAPI server in a separate process
    fastapi_process = multiprocessing.Process(target=run_fastapi, args=(queue,))
    fastapi_process.start()

    # webcam process
    webcam_process = multiprocessing.Process(target=run_webcam, args=(queue,))
    webcam_process.start()

    # Wait for the Tkinter process to finish (i.e., window is closed)
    fastapi_process.join()
    webcam_process.join()
