import os
import subprocess

def close_server():
    with open('pid.txt', 'r') as file:
        pid = file.read()
    os.system(f"taskkill /F /PID {pid}")


# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':
    close_server()
