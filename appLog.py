import win32evtlog
import winreg
import json

def get_installed_apps():
    apps = []
    reg_path = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall'

    with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path) as key:
        for i in range(0, winreg.QueryInfoKey(key)[0]):
            skey_name = winreg.EnumKey(key, i)
            with winreg.OpenKey(key, skey_name) as skey:
                try:
                    app_name = winreg.QueryValueEx(skey, 'DisplayName')[0]
                    apps.append(app_name)
                except OSError as e:
                    pass

    return apps

def get_app_event_logs(app_names):
    server = 'localhost'  # 使用本地计算机
    log_type = 'Application'  # 指定事件日志类型
    events = []

    hand = win32evtlog.OpenEventLog(server, log_type)
    total = win32evtlog.GetNumberOfEventLogRecords(hand)

    flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ
    events_read = 0
    while events_read < total:
        results = win32evtlog.ReadEventLog(hand, flags, 0)
        if not results:
            break
        for event in results:
            for app_name in app_names:
                if app_name in str(event.StringInserts):
                    events.append({
                        'AppName': app_name,
                        'EventID': event.EventID,
                        'TimeGenerated': event.TimeGenerated.strftime("%Y-%m-%d %H:%M:%S"),
                        'StringInserts': event.StringInserts
                    })
        events_read += len(results)

    win32evtlog.CloseEventLog(hand)
    return events

installed_apps = get_installed_apps()
events = get_app_event_logs(installed_apps)

# 保存到txt文件
with open('events.txt', 'w') as file:
    for event in events:
        file.write(json.dumps(event))
        file.write('\n')  # 每个JSON对象后面添加一个换行符，以便于阅读