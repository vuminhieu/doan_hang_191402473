from tkinter import *
import cv2
from PIL import Image, ImageTk
import time
from tkinter import filedialog, Toplevel
from object_detection import detect_yolov8
from image_processing import equalize_brightness, phan_doan_bang_cat_nguong
class App:
    def __init__(self):
        self.img_eq = None
        self.img_eq2 = None
        self.img_process = None
        self.appName = "ĐỒ ÁN TỐT NGHIỆP - VŨ THỊ HẰNG"
        self.window = Tk()
        self.window.title(self.appName)

        self.button_frame = Frame(self.window)
        self.button_frame.pack(anchor=CENTER, expand=True, side=TOP)
        self.btn_open_file = Button(self.button_frame, text="Open Video File", width=30, bg='green', fg='white',activebackground='red', command=self.open_file)
        self.btn_open_file.pack(side=LEFT)
        self.btn_open_image = Button(self.button_frame, text="Open Image", width=30, bg='purple',fg='white',activebackground='red', command=self.open_image)
        self.btn_open_image.pack(side=LEFT)
        self.btn_equalize = Button(self.button_frame, text="Equalize", width=30, bg='orange', activebackground='red', command=self.open_equalize_dialog)
        self.btn_equalize.pack(side=LEFT)
        self.btn_process = Button(self.button_frame, text="Process", width=30, bg='pink', activebackground='red', command=self.open_process_dialog)
        self.btn_process.pack(side=LEFT)
        self.btn_save = Button(self.button_frame, text="Save", width=30, bg='gray', fg='white', activebackground='red', command=self.open_save)
        self.btn_save.pack(side=LEFT)
        self.btn_reset = Button(self.button_frame, text="Reset", width=30, activebackground='red', command=self.reset)
        self.btn_reset.pack(side=LEFT)

        self.label = Label(self.window, text='NGHIÊN CỨU ỨNG DỤNG XỬ LÝ ẢNH TRONG TÌM KIẾM NẠN NHÂN BẰNG DRONE', font=15, bg='blue', fg='white').pack(side=TOP, fill=BOTH)
        self.canvas = Canvas(self.window, width=400, height=500, bg='gray')
        self.canvas.pack()
        self.btn_snapshot = Button(self.window, text="Snapshot", width=30, bg='yellow',activebackground='red', command=self.snapshot)
        self.btn_snapshot.pack(anchor=CENTER, expand=True)
        self.btn_quit = Button(self.window, text="QUIT", fg="red", command=self.window.destroy)
        self.btn_quit.pack(side=BOTTOM)
        self.window.mainloop()
    def open_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.img = cv2.imread(file_path)
            self.update_image(self.img)
    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4;*.avi")])
        if file_path:
            self.vid = MyVideoCapture(file_path)
            self.update()

    def snapshot(self):
        check, frame = self.vid.getFrame()
        if check:
            process_frame = detect_yolov8(frame)
            directory = "D:/UTC DOCUMENTS/IMAGE PROCESSING/DEMO/Snapshot/"
            image_name = directory + "IMG-" + time.strftime("%H-%M-%S-%d-%m" + ".jpg")
            cv2.imwrite(image_name, cv2.cvtColor(process_frame, cv2.COLOR_BGR2RGB))
            msg = Label(self.window, text="Image saved: " + image_name, bg='green', fg='white')
            msg.place(x=410, y=593)
            self.window.after(2000, lambda: msg.destroy())
    def update_image(self, img):
        img_pil = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        img_pil = img_pil.resize((400, 500))
        tk_img = ImageTk.PhotoImage(img_pil)
        if hasattr(self, 'image_label'):
            self.image_label.destroy()
        self.image_label = Label(self.canvas, image=tk_img)
        self.image_label.image = tk_img
        self.image_label.pack()

    def update(self):
        is_true, frame = self.vid.getFrame()
        if is_true:
            frame = detect_yolov8(frame)
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
            self.canvas.create_image(0, 0, image=self.photo, anchor=NW)
        self.window.after(500, self.update)

    def open_equalize_dialog(self):
        self.equalize_dialog = Toplevel(self.window)
        self.equalize_dialog.title("Equalize")
        self.btn_histogram = Button(self.equalize_dialog, text='Histogram', bg='yellow', activebackground='red', width=30, command=self.histogram)
        self.btn_histogram.pack(side=TOP)
        self.frame = Frame(self.equalize_dialog)
        self.frame.pack()
        self.alpha_scale = Scale(self.frame, from_=1, to=3, length=200, orient=HORIZONTAL, label="Alpha", resolution=0.1)
        self.alpha_scale.set(1)
        self.alpha_scale.pack(side=LEFT)
        self.beta_scale = Scale(self.frame, from_=0, to=100, length=200, orient=HORIZONTAL, label="Beta")
        self.beta_scale.set(0)
        self.beta_scale.pack(side=LEFT)
        self.btn_ok = Button(self.frame, text="OK", width=30, bg='green',activebackground='red', command=self.equalize)
        self.btn_ok.pack(side=LEFT)

    def open_process_dialog(self):
        self.process_dialong = Toplevel(self.window)
        self.process_dialong.title("Process")
        self.threshold_scale = Scale(self.process_dialong, from_=0, to=255, length=200, orient=HORIZONTAL, label="Threshold", resolution=5)
        self.threshold_scale.pack(side=LEFT)
        self.btn_process_ok = Button(self.process_dialong, text='OK', width=30, bg='brown', activebackground='red', command=self.process)
        self.btn_process_ok.pack(side=LEFT)
    def process(self):
        threshold = self.threshold_scale.get()
        if self.img_eq is not None:
            img_to_process = cv2.cvtColor(self.img_eq, cv2.COLOR_BGR2GRAY)
            img_to_process = cv2.GaussianBlur(img_to_process, (3, 3), 0)
            img_to_process = phan_doan_bang_cat_nguong(img_to_process, threshold)
            img_pil = Image.fromarray(img_to_process)
            img_pil = img_pil.resize((400, 500))
            self.tk_img = ImageTk.PhotoImage(img_pil)
            if hasattr(self, 'image_label'):
                self.image_label.destroy()
            self.image_label = Label(self.canvas, image=self.tk_img)
            self.image_label.pack()
            self.img_process = img_pil
        elif self.img_eq2 is not None:
            img_to_process = cv2.cvtColor(self.img_eq2, cv2.COLOR_BGR2GRAY)
            img_to_process = cv2.GaussianBlur(img_to_process, (3, 3), 0)
            img_to_process = phan_doan_bang_cat_nguong(img_to_process, threshold)
            img_pil = Image.fromarray(img_to_process)
            img_pil = img_pil.resize((400, 500))
            self.tk_img = ImageTk.PhotoImage(img_pil)
            if hasattr(self, 'image_label'):
                self.image_label.destroy()
            self.image_label = Label(self.canvas, image=self.tk_img)
            self.image_label.pack()
            self.img_process = img_pil
    def equalize(self):
        alpha = self.alpha_scale.get()
        beta = self.beta_scale.get()
        print(f"Alpha: {alpha}, Beta: {beta}")
        self.img_eq = equalize_brightness(self.img, alpha, beta)
        self.update_image(self.img_eq)

    def histogram(self):
        img_yuv = cv2.cvtColor(self.img, cv2.COLOR_BGR2YUV)
        img_yuv[:, :, 0] = cv2.equalizeHist(img_yuv[:, :, 0])
        self.img_eq2 = cv2.cvtColor(img_yuv, cv2.COLOR_YUV2BGR)
        print("Ảnh đã được cân bằng")
        self.update_image(self.img_eq2)

    def reset(self):
        self.img = None
        self.img_eq = None
        self.img_eq2 = None
        self.vid = None
        self.canvas.delete("all")
        if hasattr(self, 'image_label'):
            self.image_label.destroy()
        if hasattr(self, 'tk_img'):
            del self.tk_img
        if hasattr(self, 'img_pil'):
            del self.img_pil
        if hasattr(self, 'vid'):
            self.vid.destroy()

    def open_save(self):
        if self.img_process is not None:
            directory = "D:/UTC DOCUMENTS/IMAGE PROCESSING/DEMO/Processed Image/"
            image_name = directory + "IMG-" + time.strftime("%H-%M-%S-%d-%m") + ".jpg"
            img_to_save = self.img_process.convert("L")  # Chuyển đổi đối tượng ảnh sang mode 'L' (grayscale)
            img_to_save.save(image_name)
            msg = Label(self.window, text="Image saved: " + image_name, bg='green', fg='white')
            msg.place(x=410, y=593)
            self.window.after(2000, lambda: msg.destroy())
class MyVideoCapture:
    def __init__(self, video_source=0):
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video file")
        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
    def getFrame(self):
        if self.vid.isOpened():
            is_true, frame = self.vid.read()
            if is_true:
                frame = cv2.resize(frame, (400, 500))
                return is_true, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            else:
                return is_true, None
        else:
            return False, None

    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()

if __name__ == "__main__":
    App()
