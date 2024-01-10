import cv2
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from ultralytics import YOLO


class VideoPlayerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Video Player App")

        self.video_path = None
        self.video_capture = None
        self.current_frame = None

        self.canvas = tk.Canvas(self.master)
        self.canvas.pack()

        self.load_video_button = tk.Button(self.master, text="Load Video", command=self.load_video)
        self.load_video_button.pack()

        self.play_button = tk.Button(self.master, text="Play", command=self.play_video)
        self.play_button.pack()

        # Variable to store the frame rate
        self.fps = 30

    def load_video(self):
        self.video_path = filedialog.askopenfilename()
        self.video_capture = cv2.VideoCapture(self.video_path)

        # Update the frame rate variable
        self.fps = self.video_capture.get(cv2.CAP_PROP_FPS)

        # Define the codec and create VideoWriter object
        fourcc = cv2.VideoWriter_fourcc(*'MP4V')
        self.out = cv2.VideoWriter('output.mp4', fourcc, self.fps,
                                   (int(self.video_capture.get(3)), int(self.video_capture.get(4))))

        self.play_video()  # Automatically start playing after loading the video

    def play_video(self):
        ret, frame = self.video_capture.read()
        if ret:
            # Add the functionality to detect people here
            frame = self.detect_people(frame)

            self.current_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.show_frame()

            # Write the frame to the output video
            self.out.write(frame)

            # Calculate the delay based on the frame rate
            delay = int(1000 / self.fps)

            self.master.after(delay,
                              self.play_video)  # Call the function again after 'delay' milliseconds to play the video continuously
        else:
            self.video_capture.release()
            self.out.release()  # Release the VideoWriter when done

    def detect_people(self, frame):
        # Use YOLOv8 to detect people in the frame
        model = YOLO("yolov8s.pt")
        results = model(frame, save=False, conf=0.5)
        result_np = results[0].numpy()

        for i in range(len(results[0])):
            boxes = results[0].boxes
            box = boxes[i]
            clsID = box.cls.numpy()[0]

            if clsID == 0:  # If the object is a person, draw a bounding box
                bb = box.xyxy.numpy()[0]
                cv2.rectangle(frame,
                              (int(bb[0]), int(bb[1])),
                              (int(bb[2]), int(bb[3])),
                              (0, 255, 0),
                              2)

        return frame

    def show_frame(self):
        img = Image.fromarray(self.current_frame)
        img = ImageTk.PhotoImage(img)
        self.canvas.config(width=img.width(), height=img.height())
        self.canvas.create_image(0, 0, anchor=tk.NW, image=img)
        self.canvas.image = img


if __name__ == "__main__":
    root = tk.Tk()
    app = VideoPlayerApp(root)
    root.mainloop()
