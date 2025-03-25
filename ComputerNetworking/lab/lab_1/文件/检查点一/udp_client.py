import socket

# 服务器地址和端口（根据实际服务器的 IP 和端口设置）
server_ip = '127.0.0.1'  # 如果在同一台机器上运行，可以使用本地回环地址
server_port = 12345
buffer_size = 1024

# 创建 UDP Socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

try:
    # 获取用户输入并发送给服务器
    message = input("请输入要发送给服务器的消息: ")
    client_socket.sendto(message.encode(), (server_ip, server_port))

    # 接收服务器的响应
    data, server = client_socket.recvfrom(buffer_size)
    print(f"收到来自服务器 {server} 的响应: {data.decode()}")

finally:
    client_socket.close()
    print("客户端已关闭连接")
