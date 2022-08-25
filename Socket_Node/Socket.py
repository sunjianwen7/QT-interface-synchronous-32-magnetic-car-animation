# 服务端server
import socket
import threading
import time
class Socket_Server():
    def __init__(self,port):
        self.data=None
        self.heart_data = bytes.fromhex("00")
        socket_ = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_=socket_
        host = "0.0.0.0"
        socket_.bind((host, port))
        socket_.listen(1)
        self.client_socket, address = socket_.accept()
        print(str(address) + '连接成功')
        self.socket_connect=True
        threading.Thread(target=self._heartbeat_threading).start()
        threading.Thread(target=self._reconnection_threading).start()
    def _heartbeat_threading(self):
        while True:
            if self.socket_connect:
                try:
                    self.client_socket.send(self.heart_data)
                except BrokenPipeError :
                    self.socket_connect=False
                time.sleep(5)
    def _reconnection_threading(self):
        while True:
            if not self.socket_connect:
                print("等待客户端重新连接")
                self.client_socket, address = self.socket_.accept()
                print(str(address)+'连接成功')
                self.socket_connect = True
class Car_Server(Socket_Server):
    def __init__(self, port):
        super().__init__(port)
        self.shake_data = bytes.fromhex("55 04 56")
        self.car_flag=False
        threading.Thread(target=self.__threading_recv).start()
        threading.Thread(target=self.__threading_shake).start()
    def _heartbeat_threading(self):
        while True:
            if self.socket_connect:
                try:
                    self.client_socket.send(self.heart_data)
                except BrokenPipeError :
                    self.socket_connect=False
                    self.car_flag=False
                time.sleep(5)
    def _reconnection_threading(self):
        while True:
            if not self.socket_connect:
                print("等待客户端重新连接")
                self.client_socket, address = self.socket_.accept()
                print(str(address)+'连接成功')
                self.socket_connect = True
                threading.Thread(target=self.__threading_shake).start()
    def __threading_shake(self):
        while True:
            if self.car_flag:
                break
            self.client_socket.send(self.shake_data)
            time.sleep(1)
    def __threading_recv(self):
        while True:
            data=self.client_socket.recv(1024)
            if data:
                hex_list=[i for i in data]
                print(hex_list)
                if hex_list[1]==0:
                    self.car_flag=True
                    print("车辆握手完毕")
                if hex_list[1]==2:
                    self.rfid=int(hex_list[3])
class Android_Server(Socket_Server):
    def __init__(self, port):
        super().__init__(port)
        self.Drama=0
        threading.Thread(target=self.__threading_recv).start()
    def __threading_recv(self):
        while True:
            data=self.client_socket.recv(1024)
            if data:
                hex_list=[i for i in data]
                print(hex_list)
                if hex_list[1]==10:
                    self.Drama=hex_list[2]
class OTA_Server(Socket_Server):
    def __init__(self, port):
        super().__init__(port)
        self.Drama=0
    def __threading_recv(self):
        while True:
            data=self.client_socket.recv(1024)
            if data:
                hex_list=[i for i in data]
                print(hex_list)
                if hex_list[1]==1:
                    self.car_flag=True
                if hex_list[1]==2:
                    self.rfid=int(hex_list[3])
if __name__ == '__main__':
    Car_Server(1234)
