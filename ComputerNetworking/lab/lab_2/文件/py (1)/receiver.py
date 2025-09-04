from scapy.all import sniff, Ether
import os

def packet_handler(packet):
    """
    处理接收到的以太网帧，提取数据并保存到文件。
    """
    if Ether in packet:
        payload = bytes(packet[Ether].payload)
        if payload:
            # 将接收到的有效载荷写入文件
            with open("received_file.txt", "ab") as file:
                file.write(payload)
            print(f"接收到数据帧，大小: {len(payload)} bytes")

def main():
    # 获取可用网络接口列表
    from scapy.all import get_if_list
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
    
    # 开始捕获数据包
    print("开始接收数据包...")
    sniff(iface=interface, prn=packet_handler, store=False)

if __name__ == "__main__":
    main()
