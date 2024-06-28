from ultralytics import YOLO
import cv2
import cvzone
import math
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart


def video_detection(path_x):
    video_capture = path_x
    cap = cv2.VideoCapture(video_capture)
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))

    model1 = YOLO(
        "/Users/soggynut/Downloads/election/main-project/YOLO-Weights/yolov8n.pt")
    model2 = YOLO(
        "/Users/soggynut/Downloads/election/main-project/YOLO-Weights/best.pt")
    model_knife = YOLO(
        "/Users/soggynut/Downloads/election/main-project/YOLO-Weights/knife_weights.pt")

    classNames = ["person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck", "boat",
                  "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat",
                  "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella",
                  "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite", "baseball bat",
                  "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle", "wine glass", "cup",
                  "fork", "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli",
                  "carrot", "hot dog", "pizza", "donut", "cake", "chair", "sofa", "pottedplant", "bed",
                  "diningtable", "toilet", "tvmonitor", "laptop", "mouse", "remote", "keyboard", "cell phone",
                  "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors",
                  "teddy bear", "hair drier", "toothbrush", " mobile phone" , "knife"
                  ]
    classNames2 = ["Fire", "", ""]
    classNames_knife = ["knife"]

    while True:
        success, img = cap.read()
        results1 = model1(img, stream=True)
        for r in results1:
            boxes = r.boxes
            for box in boxes:
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                print(x1, y1, x2, y2)
                cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
                # Fall detection logic
                if classNames[int(box.cls[0])] == "person" and (y2 - y1) < (x2 - x1):
                    # Height is greater than width, indicating a potential fall
                    fall_label = "Fall Detected"
                    cv2.putText(img, fall_label, (x1, y1 - 30), 0, 1,
                                [0, 0, 255], thickness=2, lineType=cv2.LINE_AA)

                    # Send email notification
                   # SendMail(img)

                conf = math.ceil((box.conf[0] * 100)) / 100
                cls = int(box.cls[0])
                class_name = classNames[cls]
                label = f'{class_name}{conf}'
                t_size = cv2.getTextSize(label, 0, fontScale=1, thickness=2)[0]
                c2 = x1 + t_size[0], y1 - t_size[1] - 3
                cv2.rectangle(img, (x1, y1), c2, [
                              255, 0, 255], -1, cv2.LINE_AA)  # filled
                cv2.putText(img, label, (x1, y1 - 2), 0, 1,
                            [255, 255, 255], thickness=1, lineType=cv2.LINE_AA)

        results2 = model2(img, stream=True)
        for r in results2:
            boxes = r.boxes
            for box in boxes:
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                print(x1, y1, x2, y2)
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 3)

                conf = math.ceil((box.conf[0] * 100)) / 100
                cls = int(box.cls[0])
                class_name = classNames2[cls]
                label = f'{class_name}{conf}'
                t_size = cv2.getTextSize(label, 0, fontScale=1, thickness=2)[0]
                c2 = x1 + t_size[0], y1 - t_size[1] - 3
                cv2.rectangle(img, (x1, y1), c2, [
                              0, 255, 0], -1, cv2.LINE_AA)  # filled
                cv2.putText(img, label, (x1, y1 - 2), 0, 1,
                            [255, 255, 255], thickness=1, lineType=cv2.LINE_AA)

        results_knife = model_knife(img, stream=True)
        for r in results_knife:
            boxes = r.boxes
            for box in boxes:
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                print(x1, y1, x2, y2)
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 3)

                conf = math.ceil((box.conf[0] * 100)) / 100
                cls = int(box.cls[0])
                class_name = classNames_knife[cls]
                label = f'{class_name}{conf}'
                t_size = cv2.getTextSize(label, 0, fontScale=1, thickness=2)[0]
                c2 = x1 + t_size[0], y1 - t_size[1] - 3
                cv2.rectangle(img, (x1, y1), c2, [
                              0, 0, 255], -1, cv2.LINE_AA)  # filled
                cv2.putText(img, label, (x1, y1 - 2), 0, 1,
                            [255, 255, 255], thickness=1, lineType=cv2.LINE_AA)

        yield img

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

"""def SendMail(img):
    # Save the image locally
    cv2.imwrite("fall_detected.jpg", img)

    img_data = open("fall_detected.jpg", 'rb').read()
    msg = MIMEMultipart()
    msg['Subject'] = 'Fall Alert'
    msg['From'] = 'adityapillai8010@gmail.com'
    msg['To'] = ''

    text = MIMEText("Fall Detected. Send HELP")
    msg.attach(text)
    image = MIMEImage(img_data, name=os.path.basename("fall_detected.jpg"))
    msg.attach(image)

    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login("", "")
    s.sendmail("adityapillai8010@gmail.com",
               "", msg.as_string())
    s.quit()"""
