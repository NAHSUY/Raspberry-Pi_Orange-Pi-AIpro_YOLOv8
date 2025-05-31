import os
import random
import shutil

# 设置数据集路径
image_dir = "datasets/images"
label_dir = "datasets/labels"

# 设置划分比例
train_ratio = 0.7  # 训练集占70%
val_ratio = 0.2  # 验证集占20%
test_ratio = 0.1  # 测试集占10%

# 确保所有目标文件夹存在
for split in ["train", "val", "test"]:
    os.makedirs(os.path.join(image_dir, split), exist_ok=True)
    os.makedirs(os.path.join(label_dir, split), exist_ok=True)

# 获取所有图片文件（假设图片是 .jpg 格式）
image_files = [f for f in os.listdir(image_dir) if f.endswith(".jpg")]

# 打乱数据集
random.shuffle(image_files)

# 计算划分数量
num_train = int(len(image_files) * train_ratio)
num_val = int(len(image_files) * val_ratio)

train_files = image_files[:num_train]
val_files = image_files[num_train:num_train + num_val]
test_files = image_files[num_train + num_val:]


# 定义一个函数来移动图片和对应的标签
def move_files(file_list, split):
    for file in file_list:
        # 移动图片
        shutil.move(os.path.join(image_dir, file), os.path.join(image_dir, split, file))

        # 移动标签（.txt文件）
        label_file = file.replace(".jpg", ".txt")
        if os.path.exists(os.path.join(label_dir, label_file)):
            shutil.move(os.path.join(label_dir, label_file), os.path.join(label_dir, split, label_file))


# 开始移动文件
move_files(train_files, "train")
move_files(val_files, "val")
move_files(test_files, "test")

print("数据集划分完成！")