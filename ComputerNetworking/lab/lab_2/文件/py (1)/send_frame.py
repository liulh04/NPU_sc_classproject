from scapy.all import Ether, sendp, get_if_hwaddr, get_if_list
import os
file_path = "test_file.txt5"  # 要发送的文件路径

def send_file(interface, file_path, dest_mac):
    """
    发送文件的函数，将文件分割成多个以太网帧进行传输。
    """
    # 获取源 MAC 地址
    src_mac = get_if_hwaddr(interface)

    # 打开文件
    with open(file_path, "rb") as file:
        file_data = file.read()
    
    # 文件大小
    file_size = len(file_data)
    print(f"文件大小: {file_size} bytes")

    # 设置每个数据帧的最大有效负载
    max_payload_size = 1400  # 以太网帧有效载荷的最大大小（1400 字节）

    # 将文件数据按最大负载拆分成多个数据帧
    for i in range(0, file_size, max_payload_size):
        payload = file_data[i:i + max_payload_size]
        # 构造以太网帧
        eth_frame = Ether(dst=dest_mac, src=src_mac, type=0x0800)  # IPv4 类型
        eth_frame = eth_frame / payload  # 添加数据负载
        
        # 发送帧
        sendp(eth_frame, iface=interface, verbose=True)
        print(f"发送数据帧 {i // max_payload_size + 1}，大小: {len(payload)} bytes")

def main():
    # 设置文件路径
    file_path = "test_file.txt"  # 要发送的文件
    dest_mac = "ff:ff:ff:ff:ff:ff"  # 广播地址，或者接收端的 MAC 地址
    
    # 获取可用网络接口列表
    interfaces = get_if_list()
    print("可用的网络接口列表:")
    for idx, iface in enumerate(interfaces, start=1):
        print(f"{idx}: {iface}")

    # 选择网络接口
    choice = int(input("请选择一个网络接口（输入编号）: "))
    if choice < 1 or choice > len(interfaces):
        print("无效的选择")
        return
    interface = interfaces[choice - 1]

    # 发送文件
    send_file(interface, file_path, dest_mac)

if __name__ == "__main__":
    main()
5