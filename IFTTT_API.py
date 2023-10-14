import requests

def trigger_ifttt(event_name, key, value1=None, value2=None, value3=None):
    url = f"https://maker.ifttt.com/trigger/{event_name}/with/key/{key}"
    payload = {"value1": value1, "value2": value2, "value3": value3}
    response = requests.post(url, data=payload)
    return response.status_code

# 使用你的事件名和 Webhooks 密钥调用函数
event_name = "InputBox"
your_key = "Hgdx-fQfn7cUPOruwaGCPwew0hJ3b1x-0_eFZFFVRieDk_rhhdIaOsFTRwpBm1cW"
trigger_ifttt(event_name, your_key, "Value1", "Value2", "Value3")
