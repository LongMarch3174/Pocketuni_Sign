import requests
from Request_Get import get_eventid, get_sign, get_time, get_uid


class HttpsPostWithFormData:
    def __init__(self, eventid, time, sign):
        self.eventid = eventid
        self.time = time
        self.sign = sign

        with open('Request_Get/cookie/ck.txt', 'r', encoding="utf-8") as file:
            # 逐行读取文件内容
            for line in file:
                # 查找包含特定关键字的行
                if 'OAuth Token=' in line:
                    ts_oauth_token = line.strip().split("=")[1]
                elif 'OAuth Token Secret=' in line:
                    ts_oauth_token_secret = line.strip().split("=")[1]
                elif 'UID=' in line:
                    uid = line.strip().split("=")[1]

        self.ts_oauth_token = ts_oauth_token
        self.ts_oauth_token_secret = ts_oauth_token_secret

        self.headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Host": "pocketuni.net",
            "Origin": "https://pc.pocketuni.net",
            "Pragma": "no-cache",
            "Referer": "https://pc.pocketuni.net/",
            "Sec-Ch-Ua": "\"Microsoft Edge\";v=\"117\", \"Not;A=Brand\";v=\"8\", \"Chromium\";v=\"117\"",
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": "\"Windows\"",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/117.0",
        }
        self.form_data = {
            "id": self.eventid,
            "time": self.time,
            "sign": self.sign,
            "oauth_token": self.ts_oauth_token,
            "oauth_token_secret": self.ts_oauth_token_secret,
            "version": "7.10.0",
            "from": "pc"
        }

    def send_post_request(self, url):
        try:
            # 发送 HTTPS POST 请求
            response = requests.post(url, headers=self.headers, data=self.form_data)

            # 检查响应状态码
            if response.status_code == 200:
                return response.text
            else:
                print(f"HTTP POST Request Failed with Status Code {response.status_code}")
                return None
        except Exception as e:
            print(f"An Error Occurred: {str(e)}")
            return None


# 使用示例
if __name__ == "__main__":
    uid = get_uid.get_uid()

    _Get_Eventid = get_eventid.GetEventID("https://pc.pocketuni.net/active/detail?id=5156083")
    eventid = _Get_Eventid.extract_number()

    _Get_Time = get_time.Get_Time
    time = str(_Get_Time.get_10_digit_timestamp())

    _Get_Sign = get_sign.Get_Sign(uid, eventid, time)
    sign = _Get_Sign.get_sign()

    https_poster = HttpsPostWithFormData(eventid, time, sign)
    response_text = https_poster.send_post_request("https://pocketuni.net/index.php?app=api&mod=Event&act=join2&")
    if response_text:
        print(f"Response Text:\n{response_text}")
