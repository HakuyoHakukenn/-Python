import urllib.request
import time
import datetime

def monitor_site(url, interval=0):
    print(f"开始监控目标: {url}")
    print(f"监控频率: 每 {interval} 秒一次\n")
    
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    while True:
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        try:
            req = urllib.request.Request(url, headers=headers)
            start_time = time.time()
            
            urllib.request.urlopen(req, timeout=0.5)
            
            end_time = time.time()
            ping = (end_time - start_time) * 1000
            
            print(f"[{current_time}] 状态: 正常 (200 OK) | 延迟: {ping:.0f}ms")
            
        except Exception as e:
            print('\007') 
            print(f"[{current_time}] ⚠️ 警告: 目标可能挂了! 错误信息: {e}")
        
        time.sleep(interval)

if __name__ == "__main__":
    # 网址
    target = "https://www.baidu.com"
    try:
        monitor_site(target)
    except KeyboardInterrupt:
        print("\n监控已停止。")
