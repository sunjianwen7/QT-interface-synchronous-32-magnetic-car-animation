# 服务端server
import logging
import socket
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
        logger.info(str(address) + '连接成功')
        self.socket_connect=True
        threading.Thread(target=self._heartbeat_threading).start()
        threading.Thread(target=self._reconnection_threading).start()
    def _heartbeat_threading(self):
        while True:
            if self.socket_connect:
                try:
                    self._client_socket.send(self._heart_data)
                except BrokenPipeError :
                    logger.error("BrokenPipeError")
                    self.socket_connect=False
                time.sleep(5)
    def _reconnection_threading(self):
        while True:
            if not self.socket_connect:
                logger.info("等待客户端重新连接")
                self._client_socket, address = self.socket_.accept()
                logger.info(str(address)+'连接成功')
                self.socket_connect = True
class Car_Server(Socket_Server):
    def __init__(self, port):
        self.car_flag=False
        self._charge=100
        self.rfid=1
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
                logger.info("等待客户端重新连接")
                self._client_socket, address = self.socket_.accept()
                logger.info(str(address)+'连接成功')
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
                    self._charge=int(hex_list[2])
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
            if data and data[0] == 85 and data[-1] == 86:
                hex_list=[i for i in data]
                logger.info('OTA接受数据'+str(hex_list))
                if hex_list[1]==0:
                    self.car_control=hex_list[2]
                if hex_list[1]==1:
                    self.led_control=hex_list[2]
if __name__ == '__main__':
    Car_Server(1234)
