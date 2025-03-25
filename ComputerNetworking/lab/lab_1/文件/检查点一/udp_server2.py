import socket

# 定义服务器的 IP 和端口
server_ip = '0.0.0.0'  # 监听所有可用网络接口
server_port = 12345
buffer_size = 1024

# 创建 UDP Socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((server_ip, server_port))

print(f"服务器已启动，监听端口 {server_port}...")

while True:
    # 接收客户端发送的数据
    data, client_address = server_socket.recvfrom(buffer_size)
    print(f"收到来自 {client_address} 的消息: {data.decode()}")

    # 将接收到的数据回传给客户端
    server_socket.sendto(data, client_address)
    print(f"已将数据回传给客户端 {client_address}")
