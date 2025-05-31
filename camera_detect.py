from yolo_detect import model
from inventory_manager import load_inventory, save_inventory, log_detection
import cv2


# 打开摄像头实时识别（按 s 保存识别，q 退出）：
def main():
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        results = model(frame)
        items = []
        for box in results[0].boxes:
            cls_id = int(box.cls)
            name = results[0].names[cls_id]
            items.append(name)

        # 显示画面
        annotated_frame = results[0].plot()
        cv2.imshow("YOLOv8 Inventory Camera", annotated_frame)

        # 按键识别
        key = cv2.waitKey(1)
        if key == ord('s'):  # 按 s 保存识别
            inventory = load_inventory()
            for item in items:
                inventory[item] += 1
            save_inventory(inventory)
            log_detection(items)
            print("识别并保存:", items)
        elif key == ord('q'):  # 按 q 退出
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
