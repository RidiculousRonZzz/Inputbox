import win32evtlog
import datetime
import pywintypes

def get_last_week_events():
    # 获取当前时间和上周时间范围
    now = datetime.datetime.now()
    last_week = now - datetime.timedelta(days=7)

    server = 'localhost'
    logtype = 'Application'
    logtype = 'System'
    begin_time = pywintypes.Time(last_week)
    flags = win32evtlog.EVENTLOG_BACKWARDS_READ|win32evtlog.EVENTLOG_SEQUENTIAL_READ

    hand = win32evtlog.OpenEventLog(server, logtype)
    events = win32evtlog.ReadEventLog(hand, flags, 0)


    # 存储运行的程序
    programs = []

    for event in events:
        print(event.StringInserts)

        # if event.TimeGenerated < begin_time:
        #     continue
        if event.StringInserts and 'Application Name' in event.StringInserts:
            program_name = event.StringInserts[event.StringInserts.index('Application Name') + 1]
            if program_name not in programs:
                programs.append(program_name)

    return programs

if __name__ == "__main__":
    last_week_programs = get_last_week_events()
    print("Programs run last week:")
    for program in last_week_programs:
        print(program)
