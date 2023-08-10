from WebcamApp import run_webcam
from api import run_fastapi
import multiprocessing


if __name__ == "__main__":
    # Init process queue
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
