import re


class GetEventID:
    def __init__(self, url):
        self.url = url

    def extract_number(self):
        try:
            # 使用正则表达式匹配 URL 中的数字参数
            match = re.search(r'id=(\d{7})', self.url)

            if match:
                # 提取匹配到的数字参数
                number = match.group(1)
                return number
            else:
                print("No 7-digit number found in the URL.")
                return None
        except Exception as e:
            print(f"An Error Occurred: {str(e)}")
            return None


# 使用示例
if __name__ == "__main__":
    url = "https://pc.pocketuni.net/active/detail?id=5148542"  # 替换为您要提取数字的网址
    extractor = GetEventID(url)
    extracted_number = extractor.extract_number()
    if extracted_number:
        print(f"Extracted Number: {extracted_number}")
