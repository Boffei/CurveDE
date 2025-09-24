import os
import json

folder_path = "./"  # 替换为实际的文件夹路径

# 遍历文件夹中的所有文件
for filename in os.listdir(folder_path):
    if filename.endswith(".json"):  # 仅处理JSON文件
        file_path = os.path.join(folder_path, filename)

        # 获取文件名的数字部分
        file_number = os.path.splitext(filename)[0]
        file_extension = os.path.splitext(filename)[1]

        # 读取JSON文件
        with open(file_path, "r") as file:
            data = json.load(file)

        # 更新name值
        data["info"]["name"] = file_number + ".jpg"

        # 将更新的数据写入JSON文件
        with open(file_path, "w") as file:
            json.dump(data, file, indent=4)
