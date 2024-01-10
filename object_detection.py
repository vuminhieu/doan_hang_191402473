import cv2
from ultralytics import YOLO

def detect_yolov8(frame):
    my_file = open("label.txt", "r")
    data = my_file.read()
    class_list = data.split("\n")
    my_file.close()

    model = YOLO("yolov8s.pt")
    results = model(frame, save=False, conf=0.45)

    result_np = results[0].numpy()
    if len(result_np) != 0:
        for i in range(len(results[0])):
            boxes = results[0].boxes
            box = boxes[i]
            clsID = box.cls.numpy()[0]
            conf = box.conf.numpy()[0]
            bb = box.xyxy.numpy()[0]
            if clsID != 0:
                continue
            cv2.rectangle(frame,
                          (int(bb[0]), int(bb[1])),
                          (int(bb[2]), int(bb[3])),
                          (0, 0, 255),
                          2)
            font = cv2.FONT_HERSHEY_COMPLEX
            cv2.putText(frame,
                        class_list[int(clsID)]
                        + " "
                        + str(round(conf, 3))
                        + "%",
                        (int(bb[0]), int(bb[1]) - 10),
                        font,
                        0.5,
                        (0, 0, 0),
                        1)

    return frame
