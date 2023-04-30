import cv2
import numpy as np
import os
from dotenv import load_dotenv
load_dotenv()

def load_yolo():
    net = cv2.dnn.readNet(f"{os.getenv('yolov4-tiny.weights')}", f"{os.getenv('yolov4-tiny.cfg')}")
    with open("models\coco.names", "r") as f:
        classes = [line.strip() for line in f.readlines()]
    return net, classes

def detect_objects(img, net, classes):
    height, width, _ = img.shape
    blob = cv2.dnn.blobFromImage(img, 1/255, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    output_layers_names = net.getUnconnectedOutLayersNames()
    layer_outputs = net.forward(output_layers_names)

    boxes = []
    confidences = []
    class_ids = []

    for output in layer_outputs:
        for detection in output:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.6:
                center_x, center_y, w, h = (detection[0:4] * np.array([width, height, width, height])).astype('int')
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)
                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    return boxes, confidences, class_ids

def draw_boxes(img, boxes, confidences, class_ids, classes):
    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
    font = cv2.FONT_HERSHEY_PLAIN
    colors = np.random.uniform(0, 255, size=(len(classes), 3))

    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])
            color = colors[class_ids[i]]
            cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
            cv2.putText(img, label, (x, y - 5), font, 1, color, 1)

    return img

def object_detection():
    net, classes = load_yolo()
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    detected_objects = []

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        boxes, confidences, class_ids = detect_objects(frame, net, classes)
        frame = draw_boxes(frame, boxes, confidences, class_ids, classes)
        cv2.imshow("Object Detection", frame)

        for i in range(len(boxes)):
            if i in cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4):
                detected_objects.append(classes[class_ids[i]])

        key = cv2.waitKey(1)
        if key == 27:  # Press 'Esc' to exit
            break

    cap.release()
    cv2.destroyAllWindows()
    return detected_objects

