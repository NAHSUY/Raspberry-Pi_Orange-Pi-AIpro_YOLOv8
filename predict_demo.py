from ultralytics import YOLO
import cv2
from cv2 import getTickCount, getTickFrequency

yolo = YOLO('runs/detect/train/weights/best.pt')

# 摄像头实时检测

cap = cv2.VideoCapture(0)
while cap.isOpened():
    loop_start = getTickCount()  # 记录循环开始的时间，用于计算每一帧的处理时间
    success, frame = cap.read()  # 读取摄像头的一帧图像

    if success:
        results = yolo.predict(source=frame)  # 对当前帧进行目标检测并显示结果
    annotated_frame = results[0].plot()  # 将检测结果绘制在图像上，得到带有目标框的图像。

    # 显示程序
    loop_time = getTickCount() - loop_start  # 计算处理一帧图像所花费的时间。
    total_time = loop_time / (getTickFrequency())  # 将处理时间转换为秒数。
    FPS = int(1 / total_time)  # FPS计算
    # 在图像左上角添加FPS文本
    fps_text = f"FPS: {FPS:.2f}"  # 构造显示帧率的文本字符串
    font = cv2.FONT_HERSHEY_SIMPLEX  # 选择字体类型
    font_scale = 1  # 设置字体的缩放比例
    font_thickness = 2  # 设置字体的粗细
    text_color = (0, 0, 255)  # 红色
    text_position = (10, 30)  # 左上角位置

    cv2.putText(annotated_frame, fps_text, text_position, font, font_scale, text_color, font_thickness)
    cv2.imshow('Real-time detection', annotated_frame)
    # 通过按下 'q' 键退出循环
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()  # 释放摄像头资源
cv2.destroyAllWindows()  # 关闭OpenCV窗口