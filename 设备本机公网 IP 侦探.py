import urllib.request
import json

def get_ip_info():
    print("正在追踪网络信号...")
    api = "http://ip-api.com/json/?lang=zh-CN"
    
    try:
        req = urllib.request.Request(api, headers={'User-Agent': 'Mozilla/5.0'})
        res = urllib.request.urlopen(req)
        data = json.loads(res.read().decode('utf-8'))
        
        if data['status'] == 'success':
            print("-" * 30)
            print(f"IP 地址 : {data['query']}")
            print(f"国家/地区: {data['country']}")
            print(f"省份/区域: {data['regionName']}")
            print(f"城市     : {data['city']}")
            print(f"运营商   : {data['isp']}")
            print(f"经纬度   : {data['lat']}, {data['lon']}")
            print("-" * 30)
        else:
            print("查询失败")
            
    except Exception as e:
        print(f"网络错误: {e}")

if __name__ == "__main__":
    get_ip_info()
    input("\n按回车退出...")
