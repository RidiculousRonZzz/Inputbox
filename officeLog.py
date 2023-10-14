import win32evtlog

def get_app_start_events(app_names):
    server = 'localhost'  # 使用本地计算机
    log_type = 'Application'  # 指定事件日志类型
    events = []

    # 打开事件日志
    hand = win32evtlog.OpenEventLog(server, log_type)
    total = win32evtlog.GetNumberOfEventLogRecords(hand)

    flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ
    events_read = 0
    while events_read < total:
        # 读取事件
        results = win32evtlog.ReadEventLog(hand, flags, 0)
        if not results:
            break
        for event in results:
            for app_name in app_names:
                if app_name in str(event.StringInserts):  # 检查事件是否与指定的应用程序相关
                    events.append({
                        'AppName': app_name,
                        'EventID': event.EventID,
                        'TimeGenerated': event.TimeGenerated,
                        'StringInserts': event.StringInserts
                    })
        events_read += len(results)

    win32evtlog.CloseEventLog(hand)
    return events

# 获取与PowerPoint和Word相关的事件，看用户使用的频繁程度
events = get_app_start_events(["POWERPNT.EXE", "WINWORD.EXE"])
for event in events:
    print(event)
