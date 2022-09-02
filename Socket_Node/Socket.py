# 服务端server
import socket
import struct
import threading
import time
from loguru import logger

class Socket_Server():
    def __init__(self,port):
        self.data=None
        self._heart_data = bytes.fromhex("66")
        socket_ = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        self.socket_=socket_
        host = "0.0.0.0"
        socket_.bind((host, port))
        socket_.listen(1)
        self._client_socket, address = socket_.accept()
        logger.info(str(address) +self.class_name()+ '连接成功')
        self.socket_connect=True
        threading.Thread(target=self._heartbeat_threading).start()
        threading.Thread(target=self._reconnection_threading).start()
    @classmethod
    def class_name(cls):
        return str(cls.__name__)
    def _heartbeat_threading(self):
        while True:
            if self.socket_connect:
                try:
                    self._client_socket.send(self._heart_data)
                except BrokenPipeError :
                    logger.error(self.class_name()+"BrokenPipeError")
                    self.socket_connect=False
                except ConnectionResetError:
                    logger.error(self.class_name() + "ConnectionResetError")
                    self.socket_connect = False
                time.sleep(5)

    def _reconnection_threading(self):
        while True:
            if not self.socket_connect:
                logger.info(self.class_name()+"等待客户端重新连接")
                self._client_socket, address = self.socket_.accept()
                logger.info(self.class_name()+str(address)+'重新连接成功')
                self.socket_connect = True
class Car_Server(Socket_Server):
    def __init__(self, port):
        self.car_flag=False
        self._charge=100
        self.rfid=6
        super().__init__(port)
        self.__shake_data = bytes.fromhex("55 04 56")
        self.__open_led_data=bytes.fromhex("55 0a 56")
        self.__close_led_data = bytes.fromhex("55 07 56")
        self.__car_stop_data=bytes.fromhex("55 08 56")
        self.__car_run_data=bytes.fromhex("55 09 56")
        self.__blink_led_data=bytes.fromhex("55 06 56")
        threading.Thread(target=self.__threading_recv).start()
        threading.Thread(target=self.__threading_shake).start()
    def _car_open_led(self):
        self._client_socket.send(self.__open_led_data)
    def _car_close_led(self):
        self._client_socket.send(self.__close_led_data)
    def _car_blink_led(self):
        self._client_socket.send(self.__blink_led_data)
    def _car_stop(self):
        self._client_socket.send(self.__car_stop_data)
    def _car_run(self):
        self._client_socket.send(self.__car_run_data)
    def _heartbeat_threading(self):
        while True:
            if self.socket_connect:
                try:
                    self._client_socket.send(self._heart_data)
                except BrokenPipeError :
                    self.socket_connect=False
                    self.car_flag=False
                time.sleep(5)
    def _reconnection_threading(self):
        while True:
            if not self.socket_connect:
                logger.info("等待车辆客户端重新连接")
                self._client_socket, address = self.socket_.accept()

                logger.info(str(address)+'车辆连接成功')
                self.socket_connect = True
                threading.Thread(target=self.__threading_shake).start()
    def __threading_shake(self):
        while True:
            if self.socket_connect:
                if self.car_flag:
                    self._client_socket.send(bytes.fromhex("55 01 56"))
                    break
                try:
                    self._client_socket.send(self.__shake_data)
                except BrokenPipeError:
                    logger.error("BrokenPipeError")
                    pass
                time.sleep(1)
    def __threading_recv(self):
        while True:
            try:
                data=self._client_socket.recv(1024)
            except Exception :
                logger.error("Exception")
                data=None
            if data and data[0]==85 and data[-1]==86:
                hex_list=[i for i in data]
                logger.info('车辆接受数据'+str(hex_list))
                if hex_list[1]==0:
                    self.car_flag=True
                    logger.info("车辆握手完毕")
                if hex_list[1] == 2:
                    self.rfid = int(hex_list[3])
                if hex_list[1]==1:
                    self._charge=int(hex_list[2])-20
class Android_Server(Socket_Server):
    def __init__(self, port):
        super().__init__(port)
        self.Drama=0
        self.get_charge=False
        self.get_car = False
        threading.Thread(target=self.__threading_recv).start()
    def __threading_recv(self):
        while True:
            try:
                data = self._client_socket.recv(1024)
            except ConnectionResetError:
                logger.error("ConnectionResetError")
                data = None
            if data and data[0]==85 and data[-1]==86:
                hex_list=[i for i in data]
                logger.info('安卓接受数据'+str(hex_list))
                if hex_list[1]==10:
                    if self.Drama==0:
                        self.Drama=hex_list[2]
                    else:
                        logger.info("场景{}正在执行中".format(self.Drama))
                if hex_list[1] == 11:
                    self.get_charge=True
                if hex_list[1] == 12:
                    self.get_car=True
class OTA_Server(Socket_Server):
    def __init__(self, port):
        super().__init__(port)
        self.car_control=-1
        self.led_control=-1
        threading.Thread(target=self.__threading_recv).start()
    def __threading_recv(self):
        while True:
            try:
                data = self._client_socket.recv(1024)
            except ConnectionResetError:
                logger.error("ConnectionResetError")
                data = None
            if data :
                print(data)
            if data and data[0] == 85 :
                hex_list=[i for i in data]
                logger.info('OTA接受数据' + str(hex_list))
                sum=0
                for i in hex_list:
                    sum+=i
                if sum%256==0:
                    if hex_list[1]==0:
                        self.car_control=hex_list[2]
                    if hex_list[1]==1:
                        self.led_control=hex_list[2]
class Zhaji_Client():
    def __init__(self):
        host = "192.168.1.200"
        port = 6001
        self.__socket_= socket.socket()
        self.__socket_.connect((host, port))
        self.__traffic_flag=False
        self.__traffic_led=0
        self.__msg_head = bytes.fromhex("BB FF 02 ")
        self.__msg_tail = bytes.fromhex("00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 02 FB")
    def _zhaji_open(self,zhaji_id):
        temp = self.__msg_head
        temp += struct.pack('b', zhaji_id)
        temp += struct.pack('b',1 )
        temp += self.__msg_tail
        print(temp)
        self.__socket_.send(temp)
    def _zhaji_close(self,zhaji_id):
        temp = self.__msg_head
        temp += struct.pack('b', zhaji_id)
        temp += struct.pack('b', 0)
        temp += self.__msg_tail
        self.__socket_.send(temp)
class Led_Client():
    def __init__(self):
        host = "192.168.1.110"
        port = 6000
        self.__socket_= socket.socket()
        self.__socket_.connect((host, port))
        self.__socket_.send(bytes.fromhex("55 01 33 FF FF FF FF 85"))
class Traffic_Client():
    def __init__(self):
        host = "192.168.1.200"
        port = 6000
        self.__socket_= socket.socket()
        self.__socket_.connect((host, port))
        self.__traffic_flag=False
        self.__traffic_led=0
        self.__msg_head = bytes.fromhex("BB FF 01 ")
        self.__msg_tail = bytes.fromhex("00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 02 FB")
        self.__traffic_group=([1,3],[2,4])
        threading.Thread(target=self.__threading_set_led).start()
        threading.Thread(target=self.__threading_listening_led).start()
    def close(self):
        self.__socket_.close()
    def __send_msg(self, index, color, waittime):
        temp = self.__msg_head
        temp += struct.pack('b', index)
        temp += struct.pack('b', color)
        temp += struct.pack('b', waittime)
        temp += self.__msg_tail
        self.__socket_.send(temp)
    def __threading_set_led(self):
        while True:
            self.__traffic_led = 1
            time.sleep(8)
            self.__traffic_led = 2
            time.sleep(2)
            self.__traffic_led = 3
            time.sleep(8)
            self.__traffic_led = 4
            time.sleep(2)
    def __set_led_from_group_color(self,group,color):
        # pr_group, pr_color=' ',' '
        # if group==0:
        #     pr_group="                           主控制"
        # elif group==1:
        #     pr_group = "从控制"
        # if color == 1:
        #     pr_color = 'red'
        # elif color == 2:
        #     pr_color = 'green'
        # elif color == 3:
        #     pr_color = 'yellow'
        # print('{0}设置了{1}'.format(pr_group, pr_color))
        if color==1:
            wait_time=10
        elif color==2:
            wait_time=8
        elif color==3:
            wait_time=2
        else:
            wait_time=0
        for i in self.__traffic_group[group]:
            self.__send_msg(index=i, color=color, waittime=wait_time)
            time.sleep(0.05)
    def __threading_listening_led(self):
        while True:
            if self.__traffic_led==0:
                continue
            elif self.__traffic_led == 1:
                self.__traffic_flag=False
                self.__set_led_from_group_color(0,1)
                time.sleep(0.05)
                self.__set_led_from_group_color(1,2)
                self.__traffic_led = 0
            elif self.__traffic_led == 2:
                self.__set_led_from_group_color(1,3)
                self.__traffic_led = 0
            elif self.__traffic_led == 3:
                self.__traffic_flag = True
                self.__set_led_from_group_color(0,2)
                time.sleep(0.05)
                self.__set_led_from_group_color(1,1)
                self.__traffic_led = 0
            elif self.__traffic_led == 4:
                self.__set_led_from_group_color(0,3)
                self.__traffic_led=0
    def get_traffic(self):
        return self.__traffic_flag
# def test():
#     host = "192.168.1.200"
#     port = 6000
#     socket_ = socket.socket()
#     socket_.connect((host, port))
#     msg_head = bytes.fromhex("BB FF 01 01 01 05 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 02 FB")
#     socket_.send(msg_head)
if __name__ == '__main__':
    Led_Client()
