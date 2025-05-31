from yolo_detect import detect_items
from inventory_manager import load_inventory, save_inventory, log_detection

def main(image_path="test_photo.jpg"):
    detected_items = detect_items(image_path)
    print("识别结果:", detected_items)

    inventory = load_inventory()
    for item in detected_items:
        inventory[item] += 1
    save_inventory(inventory)

    log_detection(detected_items)
    print("库存已更新，记录已保存")

if __name__ == "__main__":
    main()
