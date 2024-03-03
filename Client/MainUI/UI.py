from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QLabel
from getmac import get_mac_address as gma
from functools import partial
import sys
import os
import webbrowser, requests, hashlib, pyautogui

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))

# ACCESS INFO
mac = gma().replace(":","-")
mac_addr = hashlib.shake_256(mac.encode('utf-8')).hexdigest(10)
try:
    access = requests.get('http://localhost:5000/get_access/' + mac_addr)
    access_info = access.json()
    vm_id = access_info['VM_id']
    ip = access_info['ip_addr']
    username = access_info['username']
    password = access_info['password']
except:
    access = {}
    access_info = {}
    vm_id = ""
    ip = ""
    username = ""
    password = ""

# CONTAINER INFO
try:
    container_request = requests.get('http://localhost:5000/get_container/'+mac_addr)
    list_container = container_request.json()
    list_container_name = container_request.json()
except:
    list_container = {}
    list_container_name = {}
def show_alert(str):
    pyautogui.alert(str, "Thông báo")
def show_detail():
    try:
        res = requests.get('http://localhost:5000/get_detail/' + vm_id)
        data = res.json()
    except:
        state = -1
    pyautogui.alert("Tên máy ảo: " + data[0] + "\nCPU: " + str(data[1]) + "\nRam: " + str(data[2]) + "MB\nBộ nhớ trong: " + str(data[3]) + "GB", "Thông tin")
def open_url(url):
    ip = url[0]
    port = url[1]
    webbrowser.open("http:" + ip + ":" + port)

def run_VM(ip, username, password):
    try:
        res = requests.get('http://localhost:5000/get_vm_detail/' + vm_id)
        state = res.json()["OS-EXT-STS:power_state"]
    except:
        state = -1
    if state == -1:
        show_alert("Không thể kết nối đến máy chủ!")
    elif state == 7:
        show_alert("Đang khởi động máy ảo! Hãy thử lại")
        res = requests.get('http://localhost:5000/reboot_vm/' + vm_id)
    elif state != 1:
        show_alert("Đang khởi động máy ảo! Hãy thử lại")
        res = requests.get('http://localhost:5000/power_on/' + vm_id)
    else:
        os.system('cmd /c "cmdkey /generic:"%s" /user:"%s" /pass:"%s"' % (ip, username, password))
        os.system('cmd /c "mstsc /v:%s /admin /f"' % (ip))
        os.system('cmd /c "cmdkey /delete:%s"' % (ip))
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowModality(QtCore.Qt.NonModal)
        MainWindow.resize(800, 600)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        MainWindow.setFont(font)
        MainWindow.setMouseTracking(False)
        MainWindow.setAcceptDrops(True)
        MainWindow.setAutoFillBackground(False)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        background_label = QLabel(self.centralwidget)
        background_label.setGeometry(
        QtCore.QRect(0, 0, 800, 600))
        background_pixmap = QPixmap(os.path.join(CURRENT_DIR, 'background.jpg'))
        background_label.setPixmap(background_pixmap)
        background_label.setScaledContents(True)

        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(20, 80, 183, 471))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.main_list = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.main_list.setContentsMargins(0, 0, 0, 0)
        self.main_list.setObjectName("main_list")

        self.run_VM = QtWidgets.QPushButton(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.run_VM.sizePolicy().hasHeightForWidth())
        self.run_VM.setSizePolicy(sizePolicy)
        self.run_VM.setMinimumSize(QtCore.QSize(150, 50))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.run_VM.setFont(font)
        self.run_VM.setIconSize(QtCore.QSize(16, 16))
        self.run_VM.setObjectName("run_VM")
        self.run_VM.clicked.connect(partial(run_VM, ip,username,password))
        self.main_list.addWidget(self.run_VM)

        self.show_detail = QtWidgets.QPushButton(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.show_detail.sizePolicy().hasHeightForWidth())
        self.show_detail.setSizePolicy(sizePolicy)
        self.show_detail.setMinimumSize(QtCore.QSize(150, 50))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.show_detail.setFont(font)
        self.show_detail.setIconSize(QtCore.QSize(16, 16))
        self.show_detail.setObjectName("show_detail")
        self.show_detail.clicked.connect(show_detail)
        self.main_list.addWidget(self.show_detail)

        self.group_Containers = QtWidgets.QGroupBox(self.centralwidget)
        self.group_Containers.setGeometry(QtCore.QRect(210, 90, 571, 441))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.group_Containers.setFont(font)
        self.group_Containers.setAlignment(QtCore.Qt.AlignCenter)
        self.group_Containers.setFlat(False)
        self.group_Containers.setObjectName("group_Containers")

        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.group_Containers)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(10, 20, 160, 411))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.containers_list_1 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.containers_list_1.setContentsMargins(0, 0, 0, 0)
        self.containers_list_1.setObjectName("containers_list_1")

        self.verticalLayoutWidget_3 = QtWidgets.QWidget(self.group_Containers)
        self.verticalLayoutWidget_3.setGeometry(QtCore.QRect(200, 20, 161, 411))
        self.verticalLayoutWidget_3.setObjectName("verticalLayoutWidget_3")
        self.containers_list_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_3)
        self.containers_list_2.setContentsMargins(0, 0, 0, 0)
        self.containers_list_2.setObjectName("containers_list_2")

        self.verticalLayoutWidget_4 = QtWidgets.QWidget(self.group_Containers)
        self.verticalLayoutWidget_4.setGeometry(QtCore.QRect(390, 20, 160, 411))
        self.verticalLayoutWidget_4.setObjectName("verticalLayoutWidget_4")
        self.containers_list_3 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_4)
        self.containers_list_3.setContentsMargins(0, 0, 0, 0)
        self.containers_list_3.setObjectName("containers_list_3")


        if len(list_container) <= 4:
            for i in range(len(list_container)):
                objname = f"{list_container[i]['tenanh']}"
                list_container[i]['tenanh'] = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
                list_container[i]['tenanh'].setMinimumSize(QtCore.QSize(100, 50))
                list_container[i]['tenanh'].setObjectName(objname)
                list_container[i]['tenanh'].clicked.connect(partial(open_url, (list_container[i]['ip'],list_container[i]['port'])))
                self.containers_list_1.addWidget(list_container[i]['tenanh'])
        elif len(list_container) <= 8 and len(list_container) > 4:
            for i in range(4):
                objname = f"{list_container[i]['tenanh']}"
                list_container[i]['tenanh'] = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
                list_container[i]['tenanh'].setMinimumSize(QtCore.QSize(100, 50))
                list_container[i]['tenanh'].setObjectName(objname)
                list_container[i]['tenanh'].clicked.connect(partial(open_url, (list_container[i]['ip'],list_container[i]['port'])))
                self.containers_list_1.addWidget(list_container[i]['tenanh'])
            for i in range(4, len(list_container)):
                objname = f"{list_container[i]['tenanh']}"
                list_container[i]['tenanh'] = QtWidgets.QPushButton(self.verticalLayoutWidget_3)
                list_container[i]['tenanh'].setMinimumSize(QtCore.QSize(100, 50))
                list_container[i]['tenanh'].setObjectName(objname)
                list_container[i]['tenanh'].clicked.connect(partial(open_url, (list_container[i]['ip'], list_container[i]['port'])))
                self.containers_list_2.addWidget(list_container[i]['tenanh'])
        elif len(list_container) <= 12 and len(list_container) > 8:
            for i in range(4):
                objname = f"{list_container[i]['tenanh']}"
                list_container[i]['tenanh'] = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
                list_container[i]['tenanh'].setMinimumSize(QtCore.QSize(100, 50))
                list_container[i]['tenanh'].setObjectName(objname)
                list_container[i]['tenanh'].clicked.connect(partial(open_url, (list_container[i]['ip'],list_container[i]['port'])))
                self.containers_list_1.addWidget(list_container[i]['tenanh'])
            for i in range(4, 8):
                objname = f"{list_container[i]['tenanh']}"
                list_container[i]['tenanh'] = QtWidgets.QPushButton(self.verticalLayoutWidget_3)
                list_container[i]['tenanh'].setMinimumSize(QtCore.QSize(100, 50))
                list_container[i]['tenanh'].setObjectName(objname)
                list_container[i]['tenanh'].clicked.connect(partial(open_url, (list_container[i]['ip'], list_container[i]['port'])))
                self.containers_list_2.addWidget(list_container[i]['tenanh'])
            for i in range(8, len(list_container)):
                objname = f"{list_container[i]['tenanh']}"
                list_container[i]['tenanh'] = QtWidgets.QPushButton(self.verticalLayoutWidget_4)
                list_container[i]['tenanh'].setMinimumSize(QtCore.QSize(100, 50))
                list_container[i]['tenanh'].setObjectName(objname)
                list_container[i]['tenanh'].clicked.connect(partial(open_url, (list_container[i]['ip'], list_container[i]['port'])))
                self.containers_list_3.addWidget(list_container[i]['tenanh'])

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "ỨNG DỤNG CHẠY MÁY ẢO"))
        self.run_VM.setText(_translate("MainWindow", "CHẠY MÁY ẢO"))
        self.show_detail.setText(_translate("MainWindow", "THÔNG TIN MÁY ẢO"))
        self.group_Containers.setTitle(_translate("MainWindow", "DANH SÁCH DỊCH VỤ"))
        for i in range(len(list_container)):
            name = f"{list_container_name[i]['tenanh']}"
            list_container[i]['tenanh'].setText(_translate("MainWindow", name))


def run():
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    app_icon = QIcon(os.path.join(CURRENT_DIR, 'icon.png'))
    app.setWindowIcon(app_icon)
    MainWindow.show()
    sys.exit(app.exec_())
