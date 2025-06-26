import requests
import json


class HttpsPostWithFormData:
    def __init__(self, num, psw):
        self.url = "https://pocketuni.net/index.php?app=api&mod=Sitelist&act=login"
        self.num = num
        self.psw = psw
        self.headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Host": "pocketuni.net",
            "Origin": "https://pc.pocketuni.net",
            "Pragma": "no-cache",
            "Referer": "https://pc.pocketuni.net/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "no-cors",
            "Sec-Fetch-Site": "same-site",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/117.0",
        }
        self.form_data = {
            "email": self.num + "@hhit.com",
            "type": "pc",
            "password": self.psw,
            "usernum": self.num,
            "sid": "",
            "school": "@hhit.com",
        }

        self.response_text = ""
        self.oauth_token = ""
        self.oauth_token_secret = ""
        self.uid = ""
        self.realname = ""

    def send_post_request(self):
        try:
            # 发送 HTTPS POST 请求
            response = requests.post(self.url, headers=self.headers, data=self.form_data)

            # 检查响应状态码
            if response.status_code == 200:
                self.response_text = response.text
                return response.text
            else:
                print(f"HTTP POST Request Failed with Status Code {response.status_code}")
                return None
        except Exception as e:
            print(f"An Error Occurred: {str(e)}")
            return None

    def analysis_json(self):
        try:
            parsed_data = json.loads(self.response_text)

            message = parsed_data["message"]
            if message == "success":
                # 提取所需的内容到变量中
                self.oauth_token = parsed_data["content"]["oauth_token"]
                self.oauth_token_secret = parsed_data["content"]["oauth_token_secret"]
                self.uid = parsed_data["content"]["user_info"]["uid"]
                self.realname = parsed_data["content"]["user_info"]["realname"]

                with open("Request_Get/cookie/ck.txt", "w", encoding="utf-8") as file:
                    file.write(f"OAuth Token={self.oauth_token}\n")
                    file.write(f"OAuth Token Secret={self.oauth_token_secret}\n")
                    file.write(f"UID={self.uid}\n")
                    file.write(f"RealName={self.realname}\n")

                # 打印提取的内容
                print("OAuth Token:", self.oauth_token)
                print("OAuth Token Secret:", self.oauth_token_secret)
                print(f"UID:", self.uid)
                # print(f"Real Name:", realname)
            else:
                print(message, ". Be SURE to enter them correctly")

        except json.JSONDecodeError as e:
            print(f"JSON Decoding Error: {str(e)}")


# 使用示例
if __name__ == "__main__":
    https_poster = HttpsPostWithFormData("2021122210", "@Xufeiran1")
    https_poster.send_post_request()
    https_poster.analysis_json()




