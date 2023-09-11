import os
import time

def monitor_directory(directory):
    file_dict = {}  # 用于保存文件的修改时间戳
    while True:
        for file in os.listdir(directory):
            file_path = os.path.join(directory, file)
            if os.path.isfile(file_path):
                # 获取文件的最新修改时间戳
                modified_time = os.stat(file_path).st_mtime

                # 如果文件的最新修改时间戳与之前保存的不同，则说明文件发生了变化
                if file_path not in file_dict or modified_time != file_dict[file_path]:
                    print(f"文件 {file} 发生了变化")
                    file_dict[file_path] = modified_time

        time.sleep(1)  # 休眠1秒后再检查文件变化

# 监控目录下的文件变化
monitor_directory("E:\\11\\")