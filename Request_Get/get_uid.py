def get_uid():
    with open('Request_Get/cookie/ck.txt', 'r', encoding="utf-8") as file:
        # 逐行读取文件内容
        for line in file:
            # 查找包含特定关键字的行
            if 'OAuth Token' in line:
                ts_oauth_token = line.strip().split("=")[1]
            elif 'OAuth Token Secret' in line:
                ts_oauth_token_secret = line.strip().split("=")[1]
            elif 'UID' in line:
                uid = line.strip().split("=")[1]

    return uid


if __name__ == "__main__":
    UID = get_uid()

    if UID:
        print(UID)
    else:
        print("UID not found or request failed.")
