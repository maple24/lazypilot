import cv2
import tkinter as tk
from tkinter import ttk  # Import ttk submodule for Notebook
from PIL import Image, ImageTk
import threading
import queue
import numpy as np


class WebcamApp:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)

        self.notebook = ttk.Notebook(
            window
        )  # Use ttk.Notebook instead of tkinter.Notebook
        self.notebook.pack(fill="both", expand=True)

        self.camera_page_1 = tk.Frame(self.notebook)
        self.camera_page_2 = tk.Frame(self.notebook)

        self.notebook.add(self.camera_page_1, text="Camera 1")
        self.notebook.add(self.camera_page_2, text="Camera 2")

        self.camera_1 = CameraPage(self.camera_page_1, "Camera 1", video_source=0)
        self.camera_2 = CameraPage(self.camera_page_2, "Camera 2", video_source=1)


# Camera page class
class CameraPage:
    def __init__(
        self, frame, frame_title, video_source=0, frame_width=640, frame_height=480
    ):
        self.frame = frame
        self.frame_title = frame_title
        self.video_source = video_source
        self.frame_width = frame_width
        self.frame_height = frame_height

        self.queue = queue.Queue()
        self.camera_event = threading.Event()
        self.camera_event.clear()  # Initially, camera is off

        self.vid = None  # VideoCapture object

        self.capture_thread = threading.Thread(target=self.capture_video)
        self.capture_thread.daemon = True
        self.capture_thread.start()

        self.canvas = tk.Canvas(self.frame, width=frame_width, height=frame_height)
        self.canvas.pack()

        self.toggle_button = tk.Button(
            self.frame, text="Start Camera", command=self.toggle_camera
        )
        self.toggle_button.pack()

        self.clear_button = tk.Button(
            self.frame, text="Clear View", command=self.clear_view
        )
        self.clear_button.pack()

        self.update()

    def capture_video(self):
        while True:
            if self.camera_event.is_set():
                if self.vid is None or not self.vid.isOpened():
                    self.vid = cv2.VideoCapture(self.video_source, cv2.CAP_DSHOW)
                ret, frame = self.vid.read()
                if ret:
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    frame = self.resize_frame(frame)
                    self.queue.put(frame)
                else:
                    break
            else:
                if self.vid is not None and self.vid.isOpened():
                    self.vid.release()
                    self.vid = None
                self.camera_event.wait()  # Wait for event to be set

    def toggle_camera(self):
        if self.camera_event.is_set():
            self.camera_event.clear()
            self.toggle_button.config(text="Start Camera")
            if self.vid is not None and self.vid.isOpened():
                self.vid.release()
                self.vid = None
        else:
            self.camera_event.set()
            self.toggle_button.config(text="Stop Camera")

    def clear_view(self):
        self.queue.queue.clear()  # Clear the queue to remove frames from view

    def resize_frame(self, frame):
        h, w, _ = frame.shape
        target_h, target_w = self.frame_height, self.frame_width
        top = (target_h - h) // 2
        bottom = top + h
        left = (target_w - w) // 2
        right = left + w
        resized_frame = np.zeros((target_h, target_w, 3), dtype=np.uint8)
        resized_frame[top:bottom, left:right] = frame
        return resized_frame

    def update(self):
        if not self.queue.empty():
            frame = self.queue.get()
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
        self.frame.after(10, self.update)


# Create a tkinter window
root = tk.Tk()
app = WebcamApp(root, "Multi-Camera App")

# Close the tkinter window gracefully
root.mainloop()
