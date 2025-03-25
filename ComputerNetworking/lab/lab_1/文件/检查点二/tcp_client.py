import socket

# 定义服务器的 IP 和端口
server_ip = '127.0.0.1'  # 如果在同一台机器上运行，可以使用本地回环地址
server_port = 12345

# 创建 TCP Socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 连接到服务器
client_socket.connect((server_ip, server_port))

# 获取用户输入并发送给服务器
message = input("请输入要发送给服务器的消息: ")
client_socket.sendall(message.encode())

# 关闭连接
client_socket.close()
print("客户端已关闭连接")
