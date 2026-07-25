import os
import sys
import time
import webbrowser
import threading
from monitor_service import start_server

def open_browser():
    time.sleep(1.5)
    print(">>> 自动为您在默认浏览器中打开 Robinhood 官方币股监控面板: http://localhost:8080")
    webbrowser.open("http://localhost:8080")

def main():
    print("=" * 70)
    print("   Robinhood 链 Uniswap 官方币股 (Stock Tokens) 流动性监控系统   ")
    print("   全量覆盖 20 个官方认证币股 | 30分钟费用激增告警 | 自动 10 分钟定时更新  ")
    print("=" * 70)
    
    # Auto open browser
    b_thread = threading.Thread(target=open_browser, daemon=True)
    b_thread.start()
    
    # Start web server
    try:
        start_server()
    except KeyboardInterrupt:
        print("\n服务已停止。")
        sys.exit(0)

if __name__ == "__main__":
    main()
