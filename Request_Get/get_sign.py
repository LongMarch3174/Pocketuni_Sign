from Request_Get import get_eventid, get_uid, get_time, md5


MD5 = md5.MD5Encryptor()


class Get_Sign:
    def __init__(self, uid, event_id, time):
        self.uid = uid
        self.event_id = event_id
        self.time = time
        self.keys = "s25ycjfxcehwzs60yookgq8fx1es05af"
        self.s = ""
        self.sign = ""

    def get_sign(self):
        self.s = self.uid + self.event_id + self.time + self.keys
        self.sign = MD5.encrypt(self.s)
        return self.sign


if __name__ == "__main__":
    uid = get_uid.get_uid()

    _get_eventid = get_eventid.GetEventID("https://pc.pocketuni.net/active/detail?id=5148542")
    eventid = _get_eventid.extract_number()

    _get_time = get_time.Get_Time
    time = str(_get_time.get_10_digit_timestamp())

    get_sign = Get_Sign(uid, eventid, time)
    sign = get_sign.get_sign()
    print(sign)
