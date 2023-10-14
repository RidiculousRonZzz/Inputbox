import requests

# Zotero API设置
ZOTERO_API_KEY = 'YOUR_ZOTERO_API_KEY'
ZOTERO_USER_ID = 'YOUR_ZOTERO_USER_ID'
ZOTERO_COLLECTION_ID = 'YOUR_ZOTERO_COLLECTION_ID'  # 如果有的话

# 要提取的网址
URL = 'https://example.com'

headers = {
    'Authorization': f'Bearer {ZOTERO_API_KEY}',
    'User-Agent': 'Mozilla/5.0'
}

# 使用Zotero的Web Translators提取文献信息
response = requests.post(f'https://api.zotero.org/users/{ZOTERO_USER_ID}/items?key={ZOTERO_API_KEY}', headers=headers, json={
    "url": URL,
    "sessionid": "unique_session_id"  # 为每个会话提供一个唯一的ID
})

if response.status_code == 200:
    print("文献信息已成功提取并添加到Zotero!")
else:
    print("提取失败:", response.text)
