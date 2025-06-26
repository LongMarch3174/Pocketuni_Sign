import hashlib


class MD5Encryptor:
    @staticmethod
    def encrypt(text):
        try:
            # 创建 MD5 加密对象
            md5 = hashlib.md5()

            # 更新对象以加密文本
            md5.update(text.encode('utf-8'))

            # 返回 MD5 加密结果
            encrypted_text = md5.hexdigest()
            return encrypted_text
        except Exception as e:
            print(f"An Error Occurred: {str(e)}")
            return None


# 使用示例
if __name__ == "__main__":
    encryptor = MD5Encryptor()

    # 加密字符串
    original_text = "1524770651491531695123647s25ycjfxcehwzs60yookgq8fx1es05af"
    encrypted_text = encryptor.encrypt(original_text)
    if encrypted_text:
        print(f"Original Text: {original_text}")
        print(f"MD5 Encrypted Text: {encrypted_text}")
