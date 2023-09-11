import socket
import subprocess


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
    servers = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 设置超时
    servers.settimeout(10)
    # 将socket绑定到指定的地址和端口号
    servers.bind((IP, 6565))
    # 监听客户端链接操作
    servers.listen(1)
    print('Server is waiting for connection...')
    while 1:
        try:
            # 使用accept()方法获取与客户端通信的socket对象
            client_socket, client_address = servers.accept()
            print('Client {} is connected'.format(client_address))
            data = client_socket.recv(1024)
            # 没有数据返回
            if not data:
                print("客户端连接已关闭")
                servers.close()
            result = subprocess.run(data.decode().split(),stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
            print(result.args)
            print(result.stdout.decode('utf-8'))
            client_socket.sendall(result.stdout)
        except socket.timeout:
            print("接收数据超时")
        except:
            print("异常退出，请重启重试！！")
            servers.close()
            break

# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':
    # 获取当前进程的进程ID
    # pid = os.getpid()
    # with open("pid.txt", "w") as file:
    #     file.write(str(pid))
    #     file.close()
    start_server(get_local_ip())
