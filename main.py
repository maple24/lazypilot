"""
curl -X POST -H "Content-Type: application/json" -d '{"message": "Your message here"}' http://localhost:8000/update_message/
"""
from WebCamApp import WebCamApp
from api import run_fastapi
import multiprocessing


if __name__ == "__main__":
    # init process queue
    queue = multiprocessing.Queue()

    # Start FastAPI server in a separate process
    fastapi_process = multiprocessing.Process(target=run_fastapi, args=(queue,))
    fastapi_process.start()

    # webcam process
    webcam_process = multiprocessing.Process(target=WebCamApp, args=(queue,))
    webcam_process.start()

    # Wait for the Tkinter process to finish (i.e., window is closed)
    fastapi_process.join()
    webcam_process.join()
