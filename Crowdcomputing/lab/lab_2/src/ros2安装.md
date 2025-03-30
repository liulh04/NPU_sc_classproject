 
# ROS 2 Humble Hawksbill 安装指南 (Ubuntu 22.04)

## 1. 设置软件源

### 1.1 启用 Universe 仓库
```bash
sudo apt install software-properties-common
sudo add-apt-repository universe
```

### 1.2 添加 ROS 2 GPG 密钥
```bash
sudo apt update && sudo apt install curl -y
sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg
```

#### 常见问题解决
若出现 `Failed to connect to raw.githubusercontent.com` 错误，需手动添加域名解析：
1. 访问 [IPAddress.com](https://www.ipaddress.com/) 查询 `raw.githubusercontent.com` 的 IP（如 `185.199.108.133`）。
2. 修改 `/etc/hosts`：
   ```bash
   sudo gedit /etc/hosts
   ```
   添加行：
   ```
   185.199.108.133 raw.githubusercontent.com
   ```

### 1.3 添加 ROS 2 软件源
```bash
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null
```

---

## 2. 安装 ROS 2 软件包

### 2.1 更新系统及软件包
```bash
sudo apt update
sudo apt upgrade
```

### 2.2 选择安装版本
- **完整桌面版** (推荐，含 GUI 工具如 RViz)：
  ```bash
  sudo apt install ros-humble-desktop
  ```
- **最小基础版** (仅核心功能)：
  ```bash
  sudo apt install ros-humble-ros-base
  ```

### 2.3 安装开发工具（可选）
```bash
sudo apt install ros-dev-tools
```

---

## 3. 配置环境变量

### 临时生效（当前终端）
```bash
source /opt/ros/humble/setup.bash
```

### 永久生效（写入 `~/.bashrc`）
```bash
echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
```

---

## 4. 测试安装

### 4.1 运行 C++ Talker
```bash
source /opt/ros/humble/setup.bash
ros2 run demo_nodes_cpp talker
```

### 4.2 运行 Python Listener
```bash
source /opt/ros/humble/setup.bash
ros2 run demo_nodes_py listener
```

#### 预期结果
- `talker` 终端会持续发布消息。
- `listener` 终端会接收并打印这些消息。

---

## 附：关键命令速查
| 功能               | 命令                                                                 |
|--------------------|----------------------------------------------------------------------|
| 启用 Universe      | `sudo add-apt-repository universe`                                   |
| 添加 GPG 密钥      | `sudo curl -sSL https://raw.githubusercontent.com/...`               |
| 安装桌面版         | `sudo apt install ros-humble-desktop`                                |
| 永久配置环境       | `echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc`              |
| 测试 C++ Talker    | `ros2 run demo_nodes_cpp talker`                                     |
| 测试 Python Listener | `ros2 run demo_nodes_py listener`                                   |
 