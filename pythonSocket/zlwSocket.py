import socket
import subprocess
import time

from flask import jsonify

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 1))
        locale_ip = s.getsockname()[0]
    except:
        locale_ip = ''
    finally:
        s.close()
    return locale_ip

# 服务端，执行命令端
def start_server(IP):
    # 创建socket对象
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 设置socket绑定地址和端口号
    server_address = (IP, 6565)
    # 将socket绑定到指定的地址和端口号
    server_socket.bind(server_address)
    # 监听客户端链接操作
    server_socket.listen(1)
    print('Server is waiting for connection...')

    # 使用accept()方法获取与客户端通信的socket对象
    while True:
        client_socket, client_address = server_socket.accept()
        print('Client {} is connected'.format(client_address))
        try:
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break
                command = data.decode()
                result = subprocess.run(command,
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE,
                                        shell=True)
                client_socket.sendall(result.stdout)
        except ConnectionResetError as cre:
            print(cre)
        finally:
            print('Client {} is disconnected'.format(client_address))
            break
    server_socket.close()


def start_client(IP,command,q):
    # 创建socket对象
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 设置socket链接地址和端口号
    server_address = (IP, 6565)
    # 将socket链接到指定的地址和端口号
    client_socket.connect(server_address)

    # 发送需要执行的命令给服务端
    # command = input('Please input your command:')
    client_socket.sendall(command.encode())
    data = client_socket.recv(1024)
    # 编码根据实际情况改变data.decode('gbk')
    print('{}\n{}'.format(command, data.decode('gbk')))

    client_socket.close()
    q.put('{}\n{}'.format(command, data.decode()))
    return jsonify('{}\n{}'.format(command, data.decode()))




# start_server("192.168.3.131")
#
# time.sleep(3)
# start_client("192.168.3.85","adb devices","1")
