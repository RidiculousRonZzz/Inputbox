import win32evtlog
import winreg
import json

def get_installed_apps_from_regkey(regkey):
    apps = []
    reg_path = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall'

    with winreg.OpenKey(regkey, reg_path) as key:
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
    server = 'localhost'  # Use the local computer
    log_type = 'Application'  # Specify the event log type
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
            if any(app_name in str(event.StringInserts) for app_name in app_names):
                events.append({
                    'AppName': next((app for app in app_names if app in str(event.StringInserts)), 'Unknown'),
                    'EventID': event.EventID,
                    'TimeGenerated': event.TimeGenerated.strftime("%Y-%m-%d %H:%M:%S"),
                    'StringInserts': event.StringInserts
                })
        events_read += len(results)

    win32evtlog.CloseEventLog(hand)
    return events

# Retrieve installed apps from both HKEY_LOCAL_MACHINE and HKEY_CURRENT_USER
installed_apps = list(set(get_installed_apps_from_regkey(winreg.HKEY_LOCAL_MACHINE) + 
                          get_installed_apps_from_regkey(winreg.HKEY_CURRENT_USER)))
events = get_app_event_logs(installed_apps)

# Save to txt file
with open('events.txt', 'w') as file:
    for event in events:
        file.write(json.dumps(event))
        file.write('\n')
