import sqlite3
import os
import json

def get_edge_history():
    # 默认Microsoft Edge历史数据库路径
    data_path = os.path.expanduser('~') + r"\AppData\Local\Microsoft\Edge\User Data\Default\History"
    
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

def get_edge_bookmarks():
    bookmarks_path = os.path.expanduser('~') + r"\AppData\Local\Microsoft\Edge\User Data\Default\Bookmarks"
    with open(bookmarks_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def save_bookmarks_to_json(data, filename):
    root = data.get("roots", {}).get("bookmark_bar", {})
    bookmarks = extract_bookmarks_as_json(root)
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(bookmarks, f, ensure_ascii=False, indent=4)

def extract_bookmarks_as_json(bookmark_node):
    extracted = []
    if 'children' in bookmark_node:
        for child in bookmark_node['children']:
            extracted.extend(extract_bookmarks_as_json(child))
    else:
        if 'url' in bookmark_node:
            bookmark = {
                "title": bookmark_node.get('name', ''),
                "url": bookmark_node['url']
            }
            extracted.append(bookmark)
    return extracted

# 使用新函数保存书签为JSON格式
bookmarks_data = get_edge_bookmarks()
save_bookmarks_to_json(bookmarks_data, "edge_bookmarks.json")

history = get_edge_history()
save_to_txt_file(history, "edge_history.txt")
# 不过不能设置自动删除历史记录
# 查询历史记录的时候，必须关闭浏览器