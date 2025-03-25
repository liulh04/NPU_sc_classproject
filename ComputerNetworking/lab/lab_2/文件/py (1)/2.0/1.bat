echo 启动 UDP 服务器...
start cmd /k "python receiver2.0.py"

REM 等待服务器启动
timeout /t 2 >nul

echo 启动 UDP 客户端...
start cmd /k "python send_frame.py"

