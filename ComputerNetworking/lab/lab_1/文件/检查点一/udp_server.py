import socket

# 服务器地址和端口
server_ip = '0.0.0.0'  # 监听所有可用的网络接口
server_port = 12345
buffer_size = 1024

# 创建 UDP Socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((server_ip, server_port))

print(f"服务器已启动，监听端口 {server_port}...")

while True:
    # 接收来自客户端的消息
    data, client_address = server_socket.recvfrom(buffer_size)
    print(f"收到来自 {client_address} 的消息: {data.decode()}")

    # 发送响应消息回客户端
    message = "服务器已收到消息"
    server_socket.sendto(message.encode(), client_address)
    print(f"已向 {client_address} 发送确认信息")
