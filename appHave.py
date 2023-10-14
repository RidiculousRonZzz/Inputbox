import winreg as reg

def get_installed_apps():
    apps = []
    reg_keys = [
        r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
        r"SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall"
    ]

    for reg_key in reg_keys:
        key = reg.OpenKey(reg.HKEY_LOCAL_MACHINE, reg_key)
        for i in range(0, reg.QueryInfoKey(key)[0]):
            try:
                skey_name = reg.EnumKey(key, i)
                skey = reg.OpenKey(key, skey_name)
                app_name = reg.QueryValueEx(skey, "DisplayName")[0]
                apps.append(app_name)
            except OSError as e:
                pass  # Skip if fails
            finally:
                skey.Close()

    return list(set(apps))  # Remove duplicates

if __name__ == "__main__":
    installed_apps = get_installed_apps()

    # Save to a TXT file
    with open("installed_apps.txt", "w") as f:
        for app in installed_apps:
            f.write(app + "\n")

    print("已安装的应用已保存到 installed_apps.txt 文件中。")