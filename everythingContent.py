import ctypes

# 定义
EVERYTHING_REQUEST_CONTENT = 0x00004000

# dll 导入
everything_dll = ctypes.WinDLL("E:\\studyfxz\\ORIC\\inputbox\\Everything-SDK\\dll\\Everything64.dll")

# 设置搜索
search_query = "E:\\studyfxz\\ content:攻角"  # "content:您要搜索的中文内容"
everything_dll.Everything_SetSearchW(search_query)
everything_dll.Everything_SetRequestFlags(EVERYTHING_REQUEST_CONTENT)

# 执行查询
everything_dll.Everything_QueryW(1)

# 获取结果数量
num_results = everything_dll.Everything_GetNumResults()

# 创建缓冲区
filename = ctypes.create_unicode_buffer(260)

# 显示结果
for i in range(num_results):
    everything_dll.Everything_GetResultFullPathNameW(i, filename, 260)
    print("Filename with the content '{}': {}".format(search_query, ctypes.wstring_at(filename)))
