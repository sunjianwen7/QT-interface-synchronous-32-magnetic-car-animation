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
        host = "192.168.0.50"
        port = 6000
        self.__socket_= socket.socket()
        self.__socket_.connect((host, port))
        self.__traffic_flag=False
        self.__traffic_led=0
        self.__msg_head = bytes.fromhex("BB FF 01 ")
        self.__msg_tail = bytes.fromhex("00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 02 FB")
        self.__traffic_group = ([1, 3], [2, 4])
        self.set_init_value()
        # self.traffic_range()
        RepeatingTimer(0.849, self.traffic_range).start()

    def set_init_value(self):
        self.a1=[1,10]
        self.a2 = [2, 8]
    def __send_msg(self, group, color, waittime):
        temp = self.__msg_head
        msg_group = struct.pack('b', self.__traffic_group[group][0])
        temp += msg_group
        msg_color = struct.pack('b', color)
        temp += msg_color
        msg_waittime = struct.pack('b', waittime)
        temp += msg_waittime
        temp += self.__msg_tail
        self.__socket_.send(temp)
        print(self.__traffic_group[group][0],msg_group.hex(),color,msg_color.hex(),waittime,msg_waittime.hex())
        print(time.time(),temp)
        time.sleep(0.05)
        temp = self.__msg_head
        temp += struct.pack('b', self.__traffic_group[group][1])
        temp += struct.pack('b', color)
        temp += struct.pack('b', waittime)
        temp += self.__msg_tail
        self.__socket_.send(temp)
        print(time.time(),temp)
    def get_traffic(self):
        return self.__traffic_flag
    def traffic_range(self):
        self.__send_msg(0,self.a1[0],self.a1[1])
        time.sleep(0.05)
        self.__send_msg(1, self.a2[0], self.a2[1])
        if self.a1[1]==1 :
            if self.a1[0]==1:
                self.a1[0]=2
                self.a1[1]=8
            elif self.a1[0] == 2:
                self.a1[0] = 3
                self.a1[1]=2
            elif self.a1[0] ==3 :
                self.a1[0] = 1
                self.a1[1] = 10
        else:
            self.a1[1]=self.a1[1]-1
        if self.a2[1]==1 :
            if self.a2[0]==1:
                self.a2[0]=2
                self.a2[1]=8
            elif self.a2[0] == 2:
                self.a2[0] = 3
                self.a2[1]=2
            elif self.a2[0] ==3 :
                self.a2[0] = 1
                self.a2[1] = 10
        else:
            self.a2[1]=self.a2[1]-1


class _Timer(threading.Thread):
    def __init__(self, interval, function, args=[], kwargs={}):
        threading.Thread.__init__(self)
        self.interval = interval
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.finished = threading.Event()
    def run(self):
        self.finished.wait(self.interval)
        if not self.finished.is_set():
            self.function(*self.args, **self.kwargs)
        self.finished.set()
class RepeatingTimer(_Timer):
    def run(self):
        while not self.finished.is_set():
            self.function(*self.args, **self.kwargs)
            self.finished.wait(self.interval)
a=Traffic_Client()
input()
a.set_init_value()