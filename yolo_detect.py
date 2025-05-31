from ultralytics import YOLO
import cv2

model = YOLO("runs/detect/train/weights/best.onnx")  # 使用轻量模型，或换成自训练模型

def detect_items(image_path):
    results = model(image_path)
    items = []
    for box in results[0].boxes:
        cls_id = int(box.cls)
        name = results[0].names[cls_id]
        items.append(name)
    return items
