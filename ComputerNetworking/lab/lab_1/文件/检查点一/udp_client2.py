import socket

# 定义服务器的 IP 和端口（请根据实际服务器的 IP 地址修改）
server_ip = '127.0.0.1'  # 如果客户端和服务器在同一台电脑上运行，可用本地回环地址
server_port = 12345
buffer_size = 1024

# 创建 UDP Socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

try:
    # 输入要发送的消息
    message = input("请输入要发送给服务器的消息: ")
    # 将消息发送到服务器
    client_socket.sendto(message.encode(), (server_ip, server_port))

    # 接收来自服务器的响应
    data, server = client_socket.recvfrom(buffer_size)
    print(f"收到来自服务器 {server} 的响应: {data.decode()}")

finally:
    client_socket.close()
    print("客户端已关闭连接")
