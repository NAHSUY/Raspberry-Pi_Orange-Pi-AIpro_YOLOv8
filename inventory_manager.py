import csv
import json
from collections import defaultdict
from datetime import datetime

inventory_file = "data/inventory.csv"
log_file = "data/detect_log.json"

def load_inventory():
    inventory = defaultdict(int)
    try:
        with open(inventory_file, newline='') as f:
            reader = csv.reader(f)
            for row in reader:
                name, qty = row
                inventory[name] = int(qty)
    except FileNotFoundError:
        pass
    return inventory

def save_inventory(inventory):
    with open(inventory_file, 'w', newline='') as f:
        writer = csv.writer(f)
        for name, qty in inventory.items():
            writer.writerow([name, qty])

def log_detection(detected_items):
    log = {"timestamp": datetime.now().isoformat(), "items": detected_items}
    try:
        with open(log_file, 'r') as f:
            data = json.load(f)
    except:
        data = []
    data.append(log)
    with open(log_file, 'w') as f:
        json.dump(data, f, indent=2)
