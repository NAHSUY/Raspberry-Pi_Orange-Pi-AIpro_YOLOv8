import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import matplotlib
import os

# 设置中文字体（适用于大多数系统）
def set_chinese_font():
    # 尝试几种常见的中文字体（Windows, macOS, Linux）
    font_candidates = [
        "SimHei",          # 黑体（Windows常见）
        "Microsoft YaHei", # 微软雅黑
        "STHeiti",         # macOS 中文字体
        "Arial Unicode MS",
        "sans-serif"       # 保底方案
    ]
    for font in font_candidates:
        try:
            plt.rcParams["font.sans-serif"] = [font]
            plt.rcParams["axes.unicode_minus"] = False  # 正常显示负号
            break
        except:
            continue


# 设置字体
set_chinese_font()

INVENTORY_FILE = "data/inventory.csv"
LOG_FILE = "data/detect_log.json"


def analyze_inventory():
    df = pd.read_csv(INVENTORY_FILE, names=["item", "count"])
    print("📦 当前库存统计：\n")
    print(df.sort_values("count", ascending=False))


def plot_inventory_bar():
    df = pd.read_csv(INVENTORY_FILE, names=["item", "count"])
    df = df.sort_values("count", ascending=False)
    plt.figure(figsize=(10, 6))
    plt.bar(df["item"], df["count"], color="skyblue")
    plt.title("当前库存柱状图")
    plt.xlabel("商品")
    plt.ylabel("数量")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("data/inventory_bar.png")
    print("✅ 柱状图已保存至 data/inventory_bar.png")
    plt.close()


def analyze_detection_history():
    try:
        data = pd.read_json(LOG_FILE)
    except ValueError:
        print("⚠️ 检测日志为空或格式错误")
        return

    records = []
    for row in data.itertuples():
        ts = pd.to_datetime(row.timestamp)
        for item in row.items:
            records.append((ts, item))
    df = pd.DataFrame(records, columns=["timestamp", "item"])
    df["date"] = df["timestamp"].dt.date

    trend = df.groupby(["date", "item"]).size().unstack(fill_value=0)
    print("📈 每日识别趋势：\n")
    print(trend)

    trend.plot(kind="line", marker="o", figsize=(10, 6))
    plt.title("商品识别数量趋势图")
    plt.xlabel("日期")
    plt.ylabel("识别数量")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("data/detection_trend.png")
    print("✅ 趋势图已保存至 data/detection_trend.png")
    plt.close()


if __name__ == "__main__":
    analyze_inventory()
    plot_inventory_bar()
    analyze_detection_history()
