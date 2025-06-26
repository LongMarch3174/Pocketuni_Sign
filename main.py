import sys
from PyQt5 import QtWidgets
from PyQt5.QtGui import QTextCursor
from PyQt5.QtCore import QTimer, QDateTime

from RG import Ui_Form
from PyQt5.QtCore import QThread, pyqtSignal

from Request_Get import get_eventid, get_sign, get_time, get_uid, request_acti, request_cookie

import time
from apscheduler.schedulers.background import BackgroundScheduler
import json
import datetime


class MyJob(QThread):
    update_signal = pyqtSignal(str)

    def __init__(self, req_time, event_url, num, psw):
        super().__init__()
        self.req_time = req_time
        self.event_url = event_url
        self.num = num
        self.psw = psw

    def run(self):
        self.trigger()

    def request_get(self):
        start_time = time.time()

        uid = get_uid.get_uid()
        eventId = get_eventid.GetEventID(self.event_url).extract_number()
        time_10 = str(get_time.Get_Time.get_10_digit_timestamp())
        sign = get_sign.Get_Sign(uid, eventId, time_10).get_sign()

        acti_post = request_acti.HttpsPostWithFormData(eventId, time_10, sign)
        # time.sleep(0.005)
        i = 0

        end_time = time.time()
        execution_time_ms = (end_time - start_time) * 1000

        print(f"程序运行时间：{execution_time_ms:.2f} 毫秒")
        self.update_signal.emit("Time-Prepare Data: "+str(execution_time_ms)+"\n")
        time.sleep(0.8)

        while True:
            # 获取当前时间
            current_time = datetime.datetime.now()
            formatted_time = current_time.strftime('%Y-%m-%d %H:%M:%S.%f')
            self.update_signal.emit("Request of Sign up: " + formatted_time)
            print(formatted_time)

            response_text = acti_post.send_post_request("https://pocketuni.net/index.php?app=api&mod=Event&act=join2&")
            if response_text:
                data = json.loads(response_text)
                msg = data["msg"]
                status = int(data["status"])

                self.update_signal.emit("message:" + msg + "status:" + str(status)+"\n")
                print("message:", msg, "status:", status)

                if status:
                    break
                else:
                    i += 1
                    if i == 3:
                        break
                    else:
                        time.sleep(2.75)
            else:
                self.update_signal.emit("No response\n")
                # self.textEdit.setText("No response")
                print("No response")
                break

    def trigger(self):
        # 创建一个触发器
        # 创建一个后台调度器
        scheduler = BackgroundScheduler()

        # 添加触发器，使用 date 选项触发任务
        # 触发获取cookie
        cookie_time = self.req_time - datetime.timedelta(seconds=5)
        scheduler.add_job(lambda: self.cookie(), 'date', run_date=cookie_time)
        # 触发报名请求
        scheduler.add_job(lambda: self.request_get(), 'date', run_date=self.req_time)

        # 启动调度器
        scheduler.start()

        # 让程序运行，等待任务触发
        try:
            while True:
                pass
        except KeyboardInterrupt:
            # 捕获 Ctrl+C 退出程序
            scheduler.shutdown()

    def cookie(self):
        cookie_post = request_cookie.HttpsPostWithFormData(self.num, self.psw)
        cookie_status = cookie_post.send_post_request()
        if cookie_status:
            cookie_post.analysis_json()
            self.update_signal.emit("Get name: "+cookie_post.realname)
        else:
            self.update_signal.emit("Close Proxy!")

        current_time = datetime.datetime.now()
        formatted_time = current_time.strftime('%Y-%m-%d %H:%M:%S.%f')
        self.update_signal.emit("Time-Get cookie: "+formatted_time+"\n")
        print(formatted_time)


class CountdownThread(QThread):
    update_signal = pyqtSignal(str)  # 用于发送更新信号

    def __init__(self, req_time):
        super().__init__()
        self.time_left = 0
        self.request_time = req_time

    def run(self):
        current_time = QDateTime.currentDateTime()
        target_time = QDateTime.fromString(self.request_time, "yyyy-MM-dd hh:mm:ss")
        self.time_left = current_time.secsTo(target_time)

        while self.time_left > 0:
            hours, remainder = divmod(self.time_left, 3600)
            minutes, seconds = divmod(remainder, 60)
            time_str = "{:02d}:{:02d}:{:02d}".format(hours, minutes, seconds)
            self.update_signal.emit(time_str)
            self.time_left -= 1
            self.sleep(1)


class MyPyQT_Form(QtWidgets.QWidget, Ui_Form):
    def __init__(self):
        super(MyPyQT_Form, self).__init__()
        self.setupUi(self)

        self.thread = None  # 用于存储线程实例

        self.countdown_thread = None  # 倒计时线程

    # 实现pushButton_click()函数，textEdit是我们放上去的文本框的id
    def get_all_data(self):
        print(self.lineEdit.text())
        print(self.lineEdit_2.text())
        print(self.lineEdit_3.text())
        print(self.dateTimeEdit.text())

        if not self.lineEdit.text().startswith("https://pc.pocketuni.net/"):
            self.textEdit.setText("Check the URL!\n")
        else:
            e_u = self.lineEdit.text()
            number = self.lineEdit_2.text()
            password = self.lineEdit_3.text()

            request_time = self.dateTimeEdit.text()
            tar_time = datetime.datetime.strptime(request_time, "%Y-%m-%d %H:%M:%S")

            self.thread = MyJob(tar_time, e_u, number, password)
            self.thread.update_signal.connect(self.update_text)
            self.thread.start()

            self.countdown_thread = CountdownThread(request_time)
            self.countdown_thread.update_signal.connect(self.updateCountdown)
            if not self.countdown_thread.isRunning():
                self.countdown_thread.start()

    def update_text(self, data):
        cursor = self.textEdit.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.insertText(data+"\n")

    def updateCountdown(self, time_str):
        self.lcdNumber.display(time_str)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    my_pyqt_form = MyPyQT_Form()
    my_pyqt_form.show()
    sys.exit(app.exec_())
