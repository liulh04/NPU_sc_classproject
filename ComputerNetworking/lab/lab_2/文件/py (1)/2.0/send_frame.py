from scapy.all import Ether, sendp, get_if_list

def send_file():
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

    # 发送文件的数据
    filename = "example_file.txt"  # 替换为你的文件
    with open(filename, "rb") as file:
        data = file.read()

    # 自定义以太网帧，附加唯一标识符
    identifier = b"MyUniqueTag"  # 唯一标记
    frame = Ether(dst="FF:FF:FF:FF:FF:FF") / (identifier + data)

    # 发送帧
    print(f"开始通过网络接口 {interface} 发送数据...")
    sendp(frame, iface=interface, verbose=True)

if __name__ == "__main__":
    send_file()
