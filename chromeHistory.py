import sqlite3
import os
import json

def get_chrome_history():
    # 默认Chrome历史数据库路径，可能需要针对你的系统进行修改
    data_path = os.path.expanduser('~') + r"\AppData\Local\Google\Chrome\User Data\Default\History"
    
    # 连接到SQLite数据库
    connection = sqlite3.connect(data_path)
    cursor = connection.cursor()

    # 查询所有历史记录
    cursor.execute("SELECT url, title, last_visit_time FROM urls ORDER BY last_visit_time DESC")
    
    return cursor.fetchall()

def save_to_txt_file(data, filename):
    with open(filename, 'w') as f:
        for record in data:
            # 转换每条记录为JSON格式并写入TXT文件
            json_str = json.dumps({
                "url": record[0],
                "title": record[1],
                "last_visit_time": record[2]
            })
            f.write(json_str + '\n')

history = get_chrome_history()
save_to_txt_file(history, "browser_history.txt")