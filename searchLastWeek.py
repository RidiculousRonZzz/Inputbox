import os
import datetime

def search_all_files():
    """
    Search for all files in the specified directories.

    :return: List of file paths.
    """
    directories = ["E:\\studyfxz", "C:\\Users\\fanxianzhe\\Desktop"]
    all_files = []

    for directory in directories:
        for foldername, subfolders, filenames in os.walk(directory):
            for filename in filenames:
                filepath = os.path.join(foldername, filename)
                all_files.append(filepath)
    
    fileString = ""
    for idx, file in enumerate(all_files):
        file = file.replace("\\", "/")
        if idx == 0:
            fileString += file
        else:
            fileString += "\n" + file
    print(fileString)
    with open("fileString.txt", "w", encoding='utf-8') as f:
        f.write(fileString)
        f.write("\n")
    print("fileString.txt Saved")
    return all_files

def search_files_in_time_range(time_range):
    """
    Search for files in the specified directories that were modified within the given time range.

    :param directories: List of directories to search in.
    :param time_range: A tuple containing the start and end dates as (start_date, end_date).
    :return: List of file paths.
    """
    directories = ["E:\\studyfxz", "C:\\Users\\fanxianzhe\\Desktop"]
    start_date, end_date = time_range
    modified_files = []

    for directory in directories:
        for foldername, subfolders, filenames in os.walk(directory):
            for filename in filenames:
                filepath = os.path.join(foldername, filename)
                file_time = datetime.datetime.fromtimestamp(os.path.getmtime(filepath))
                if start_date <= file_time <= end_date:
                    modified_files.append(filepath)

    return modified_files

# now = datetime.datetime.now()
# start = now - datetime.timedelta(days=now.weekday(), hours=now.hour, minutes=now.minute, seconds=now.second, microseconds=now.microsecond)
# end = now