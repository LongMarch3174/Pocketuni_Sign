import time


class Get_Time:
    @staticmethod
    def get_13_digit_timestamp():
        # 获取当前的 13 位时间戳（精确到毫秒）
        timestamp = int(time.time() * 1000)
        return timestamp

    @staticmethod
    def get_10_digit_timestamp():
        # 获取当前的 10 位时间戳（精确到秒）
        timestamp = int(time.time())
        return timestamp


# 使用示例
if __name__ == "__main__":
    timestamp_generator = Get_Time()

    # 获取 13 位时间戳
    timestamp_13 = timestamp_generator.get_13_digit_timestamp()
    print(f"13-Digit Timestamp: {timestamp_13}")

    # 获取 10 位时间戳
    timestamp_10 = timestamp_generator.get_10_digit_timestamp()
    print(f"10-Digit Timestamp: {timestamp_10}")
