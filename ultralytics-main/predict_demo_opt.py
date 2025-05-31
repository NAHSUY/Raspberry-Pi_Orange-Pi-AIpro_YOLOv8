from ultralytics import YOLO
import cv2
from cv2 import getTickCount, getTickFrequency

# 加载模型
yolo = YOLO('runs/detect/train/weights/best.onnx')

cap = cv2.VideoCapture(1)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

while cap.isOpened():
    loop_start = getTickCount()
    success, frame = cap.read()
    if not success:
        break

    # 保持 BGR 图像输入
    results = yolo.predict(
        source=frame,
        conf=0.4,
        iou=0.5,
        verbose=False
    )

    annotated_frame = results[0].plot()

    # 输出调试信息：类别 + 置信度 + 位置
    boxes = results[0].boxes
    if boxes is not None and boxes.xyxy.shape[0] > 0:
        for i in range(len(boxes.cls)):
            cls_id = int(boxes.cls[i].item())  # 类别索引
            conf = boxes.conf[i].item()        # 置信度
            xyxy = boxes.xyxy[i].tolist()      # 边框坐标

            print(f"Detected class {cls_id} with confidence {conf:.2f} at {xyxy}")

            # 可选：在图像上添加文字标注（与plot叠加显示）
            label = f"{cls_id}: {conf:.2f}"
            x1, y1 = int(xyxy[0]), int(xyxy[1])
            cv2.putText(
                annotated_frame, label, (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2
            )

    # FPS 计算
    loop_time = getTickCount() - loop_start
    total_time = loop_time / getTickFrequency()
    FPS = 1.0 / total_time if total_time > 0 else 0

    cv2.putText(
        annotated_frame, f"FPS: {FPS:.2f}", (10, 30),
        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2
    )

    cv2.imshow('Real-time detection', annotated_frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
