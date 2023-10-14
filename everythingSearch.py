import ctypes
import datetime
import struct

def combine_strings(keyword, filetypes):
    filetypes_list = filetypes.split(" | ")
    combined_list = [keyword + " " + filetype for filetype in filetypes_list]
    combined_string = " | ".join(combined_list)
    return combined_string

def search_everything_results(search_term, filetypes, start="", end=""):
    search_term = combine_strings(search_term, filetypes)
    if start != "" and end != "":
        search_term = f"{search_term} dm:{start}-{end}"
        print(f"search_term: {search_term}")
    EVERYTHING_REQUEST_FILE_NAME = 0x00000001
    EVERYTHING_REQUEST_PATH = 0x00000002
    EVERYTHING_REQUEST_SIZE = 0x00000010
    EVERYTHING_REQUEST_DATE_MODIFIED = 0x00000040
    EVERYTHING_REQUEST_FOLDER_NAME = 0x00000004  # 包括文件夹

    everything_dll = ctypes.WinDLL("E:\\studyfxz\\ORIC\\inputbox\\Everything-SDK\\dll\\Everything64.dll")
    everything_dll.Everything_GetResultDateModified.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_ulonglong)]
    everything_dll.Everything_GetResultSize.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_ulonglong)]
    everything_dll.Everything_GetResultFileNameW.argtypes = [ctypes.c_int]
    everything_dll.Everything_GetResultFileNameW.restype = ctypes.c_wchar_p

    # 设置搜索条件
    everything_dll.Everything_SetSearchW(search_term)
    everything_dll.Everything_SetRequestFlags(EVERYTHING_REQUEST_FILE_NAME | EVERYTHING_REQUEST_PATH | EVERYTHING_REQUEST_SIZE | EVERYTHING_REQUEST_DATE_MODIFIED | EVERYTHING_REQUEST_FOLDER_NAME)

    # 执行查询
    everything_dll.Everything_QueryW(1)

    # 获取结果数量
    num_results = everything_dll.Everything_GetNumResults()

    # 显示结果数量
    print("Result Count: {}".format(num_results))

    # 将 Windows FILETIME 转换为 python datetime
    WINDOWS_TICKS = int(1/10**-7)  # 10,000,000 (100纳秒或0.1微秒)
    WINDOWS_EPOCH = datetime.datetime.strptime('1601-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')
    POSIX_EPOCH = datetime.datetime.strptime('1970-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')
    EPOCH_DIFF = (POSIX_EPOCH - WINDOWS_EPOCH).total_seconds()  # 11644473600.0
    WINDOWS_TICKS_TO_POSIX_EPOCH = EPOCH_DIFF * WINDOWS_TICKS  # 116444736000000000.0

    def get_time(filetime):
        """将 windows filetime winticks 转换为 python datetime.datetime."""
        winticks = struct.unpack('<Q', filetime)[0]
        microsecs = (winticks - WINDOWS_TICKS_TO_POSIX_EPOCH) / WINDOWS_TICKS
        return datetime.datetime.fromtimestamp(microsecs)

    # 创建缓冲区
    filename = ctypes.create_unicode_buffer(260)
    date_modified_filetime = ctypes.c_ulonglong(1)
    file_size = ctypes.c_ulonglong(1)

    results_dict = {} 
    # 显示结果
    for i in range(num_results):
        everything_dll.Everything_GetResultFullPathNameW(i, filename, 260)
        everything_dll.Everything_GetResultDateModified(i, date_modified_filetime)
        everything_dll.Everything_GetResultSize(i, file_size)
        print("Filename: {}\nDate Modified: {}\nSize: {} bytes\n".format(ctypes.wstring_at(filename), get_time(date_modified_filetime), file_size.value))
        file_name = everything_dll.Everything_GetResultFileNameW(i)  # 获取文件名
        file_path = ctypes.wstring_at(filename)  # 获取文件路径
        results_dict[file_name] = file_path  # 将文件名和路径添加到字典中

    return results_dict

# results = search_everything_results("*.pptx")
# print(results["v1顶边4-3.pptx"])
# search_everything_results("*.docx | *.pptx")