echo 启动 UDP 服务器...
start cmd /k "python udp_server.py"

REM 等待服务器启动
timeout /t 2 >nul

echo 启动 UDP 客户端...
start cmd /k "python udp_client.py"

