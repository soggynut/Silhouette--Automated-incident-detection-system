from ultralytics import YOLO
import cv2
import math


def calculate_distance(box1, box2):
    # Calculate the Euclidean distance between the centers of two boxes
    x1_center, y1_center = (box1[0] + box1[2]) / 2, (box1[1] + box1[3]) / 2
    x2_center, y2_center = (box2[0] + box2[2]) / 2, (box2[1] + box2[3]) / 2
    distance = math.sqrt((x2_center - x1_center)**2 +
                         (y2_center - y1_center)**2)
    return distance


def video_detection(path_x):
    video_capture = path_x
    cap = cv2.VideoCapture(video_capture)
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))

    model = YOLO(
        "/Users/soggynut/Downloads/election/main-project/YOLO-Weights/yolov8n.pt")
    classNames = ["person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck", "boat",
                  "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat",
                  "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella",
                  "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite", "baseball bat",
                  "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle", "wine glass", "cup",
                  "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli",
                  "carrot", "hot dog", "pizza", "donut", "cake", "chair", "sofa", "pottedplant", "bed",
                  "diningtable", "toilet", "tvmonitor", "laptop", "mouse", "remote", "keyboard", "cell phone",
                  "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors",
                  "teddy bear", "hair drier", "toothbrush"
                  ]

    while True:
        success, img = cap.read()
        results = model(img, stream=True)
        cars = []
        for r in results:
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

                if classNames[int(box.cls[0])] == "car":
                    cars.append((x1, y1, x2, y2))

                cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 255), 3)

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

                # Check for crashes
            for i in range(len(cars)):
                for j in range(i + 1, len(cars)):
                    distance = calculate_distance(cars[i], cars[j])
                    if distance < 10 and (cars[i][2] > cars[j][0] and cars[i][0] < cars[j][2]) and (
                            cars[i][3] > cars[j][1] and cars[i][1] < cars[j][3]):
                        # Distance is less than a threshold and rectangles intersect - crash detected
                        crash_label = "Crash Detected"
                        cv2.putText(img, crash_label, (cars[i][0], min(cars[i][1], cars[j][1]) - 30), 0, 1,
                                    [0, 0, 255], thickness=2, lineType=cv2.LINE_AA)
        yield img


cv2.destroyAllWindows()
