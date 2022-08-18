import os
import socket
import sys
import time

import numpy
from PyQt5.QtGui import QPixmap
import threading
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QMainWindow

from AMGraph_Node.amgraph_test import AMD_Map
from AMGraph_Node.model import get_node_rfid
from Drama.drama import Drama
from Socket_Node import socket_server
from UI_file.ui import Ui_MainWindow
from tools.tool import sengmsg_tostr, release_port, recode_bag, str2float

txt_list=[]
class MyWindow(QMainWindow,Ui_MainWindow):  #继承类
    m_singal = pyqtSignal(str)
    m_singal2 = pyqtSignal(str)
    def __init__(self):
        self.amd=AMD_Map()
        self.drama=Drama()
        super().__init__()
        self.car_flag=False
        self.rfid=6
        self.local_path=[1]
        self.record_flag=False
        self.next_rfid=6
        self.setMouseTracking(True)
        self.m_singal.connect(self.show_msg)
        self.m_singal2.connect(self.show_msg2)
        self.setupUi(self)   #执行类中的setupUi函数
        self.retranslateUi(self)
        self.status = self.statusBar()
        self.label_image.setPixmap(QPixmap("img_resource/1.jpg"))
        self.label_image.setScaledContents(True)
        # release_port(1234)
        threading.Thread(target=self.socker_thread).start()
        threading.Thread(target=self.Virtual_car_go).start()
    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        if event.buttons() == QtCore.Qt.LeftButton:
            event.ignore()
            if self.car_flag:
                self.Real_car_go(6,1)
            else :
                print('no')
            return
    # def mouseMoveEvent(self, event: QtGui.QMouseEvent) -> None:
    #     if self.record_flag:
    #         txt_list.append(str(event.x()) + '#' + str(event.y()) + "\n")
    #     self.label_car.move(event.x(), event.y())
    def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
        if (event.key() == QtCore.Qt.Key_1):
            self.print_log('事件1')
            self.drama.TODO1()
        if (event.key() == QtCore.Qt.Key_2):
            self.print_log('事件2')
            self.drama.TODO2()
        if (event.key() == QtCore.Qt.Key_3):
            self.print_log('事件3')
            self.drama.TODO3()
        if (event.key() == QtCore.Qt.Key_4):
            self.print_log('事件4')
            self.drama.TODO4()
        if (event.key() == QtCore.Qt.Key_5):
            self.print_log('事件5')
            self.drama.TODO5()
        if (event.key() == QtCore.Qt.Key_6):
            self.print_log('事件6')
            self.drama.TODO6()
        if (event.key() == QtCore.Qt.Key_7):
            self.print_log('事件7')
            self.drama.TODO7()
        if (event.key() == QtCore.Qt.Key_8):
            self.print_log('事件8')
            self.drama.TODO8()
        if (event.key() == QtCore.Qt.Key_9):
            self.print_log('事件9')
            self.drama.TODO9()
        if (event.key() == QtCore.Qt.Key_Control):
            self.record_flag=(self.record_flag==False)
            if self.record_flag:
                print("开启")
            else:
                print("关闭")
        if (event.key() == QtCore.Qt.Key_S):
            recode_bag(txt_list)
    def show_msg(self, msg):
        self.textBrowser_log.insertPlainText(msg)
    def show_msg2(self,msg):
        self.textBrowser_rece.insertPlainText(msg)
    def print_log(self, msg):
        self.m_singal.emit(str(msg) + "\n")
    def Virtual_car_go(self):
        while True:
            if self.car_flag:
                if self.rfid!=self.next_rfid:
                    txt_name="Drama/"+str(self.rfid)+'to'+str(self.next_rfid)+'.txt'
                    vir_run_plan_txt=open(txt_name,mode='r')
                    data=vir_run_plan_txt.readlines()
                    for i in data:
                        x = int(i[:-1].split('#')[0])
                        y = int(i[:-1].split('#')[1])
                        self.label_car.move(x, y)
                        time.sleep(0.1)
                    self.rfid=self.next_rfid
                else:
                    data=get_node_rfid(self.rfid)
                    self.label_car.move(data['qt_x'],data['qt_y'])
                time.sleep(1)
    def Real_car_go(self,start,end):
        if self.car_flag :
            data=self.Path_planning(start,end)
            self.server.client.send(data)
            self.print_log("发送数据"+str([hex(i) for i in data]))
        else:
            self.print_log("socket没有握手")

    def Path_planning(self, start, end):
        path = self.amd.Calculate_path(start,end)
        send_message = [55, 0, 2]
        index = 1
        temp_list=[]
        local_path=[]
        for i in path:
            temp_list.append(i)
            local_path.append(i[0])
            send_message.append(0)
            send_message.append(index)
            index += 1
            if i[0] < 10:
                send_message.append(0)
            send_message.append(i[0])
            if i[1]['choose'] < 10:
                send_message.append(0)
            send_message.append(i[1]['choose'])
            send_message.append(0)
            send_message.append(1)
        send_message.append(56)
        local_path.append(end)
        self.local_path=local_path
        return sengmsg_tostr(send_message)


    def print_recev(self, msg):
        self.m_singal2.emit(str(msg) + "\n")
    def socker_thread(self):
        Socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket=Socket_server
        host = "0.0.0.0"
        port = 1234
        # 绑定地址
        self.print_log("等待客户端连接")
        self.status.showMessage("等待客户端连接")
        Socket_server.bind((host, port))
        Socket_server.listen(1)
        self.client_socket, address = Socket_server.accept()
        self.status.showMessage("客户端已连接")
        self.print_log("客户端已连接")
        self.print_log(str(address))
        self.server= socket_server.Server(self)



if __name__=='__main__':
    app = QtWidgets.QApplication(sys.argv)
    window=MyWindow()
    window.show()
    sys.exit(app.exec_())