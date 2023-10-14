import datetime


now = datetime.datetime.now()
start = now - datetime.timedelta(days=5, hours=now.hour, minutes=now.minute, seconds=now.second, microseconds=now.microsecond)
end = start + datetime.timedelta(days=4, hours=23, minutes=59, seconds=59)


print(start)
print(end)
