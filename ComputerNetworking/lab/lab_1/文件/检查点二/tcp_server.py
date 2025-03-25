import socket

# 定义服务器的 IP 地址和端口
server_ip = '0.0.0.0'  # 监听所有可用网络接口
server_port = 12345
buffer_size = 1024

# 创建 TCP Socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((server_ip, server_port))

# 开始监听，最大连接数为 1
server_socket.listen(1)
print(f"服务器已启动，监听端口 {server_port}...")

# 接收客户端连接
client_socket, client_address = server_socket.accept()
print(f"已连接到客户端 {client_address}")

# 接收来自客户端的消息
data = client_socket.recv(buffer_size)
print(f"收到来自 {client_address} 的消息: {data.decode()}")

# 关闭连接
client_socket.close()
server_socket.close()
print("服务器已关闭连接")
