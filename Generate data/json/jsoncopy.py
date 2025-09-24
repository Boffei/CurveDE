import shutil

# JSON 文件所在的路径
json_file = "51.json"

# 执行复制和重命名文件的循环
for i in range(201, 701):
    # 构建新的文件名
    new_file_name = f"{i}.json"

    # 复制并重命名文件
    shutil.copy2(json_file, new_file_name)
