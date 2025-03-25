import socket

# 创建UDP套接字
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

# 广播的目标地址和端口
broadcast_address = "192.168.213.255"  # 广播地址
port = 9999  # 广播的端口号

# 广播内容
message = b"This is a test broadcast from 192.168.213.192"
sock.sendto(message, (broadcast_address, port))

print(f"Broadcast message sent to {broadcast_address}:{port}")