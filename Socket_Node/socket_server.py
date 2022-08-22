# 服务端server
import threading
import time


class Server():
    def __init__(self,main):
        self.print_log=main.print_log
        self.print_rece=main.print_recev
        self.client=main.client_socket
        self.shake_data = bytes.fromhex("55 04 56")
        self.main=main
        threading.Thread(target=self.__threading_recv).start()
        self.__threading_shake()

    def __threading_shake(self):
        while True:
            if self.main.car_flag:
                self.print_log("握手成功")
                break
            self.client.send(self.shake_data)
            time.sleep(1)
    def __threading_recv(self):
        while True:
            data=self.client.recv(1024)
            if data:
                hex_list=[i for i in data]
                if hex_list[1]==0 or hex_list[1]==1 or hex_list[1]==2 :
                    self.print_rece([hex(i) for i in data])
                    if hex_list[1]==0:
                        self.main.car_flag=True
                    if hex_list[1]==1:
                        rfid=int(hex_list[2])
                        self.main.print_log('rfid is '+str(rfid))
                        if self.main.local_path[-1] == rfid:
                            self.main.rfid = rfid
                            self.main.next_rfid = rfid
                        else:
                            for i in range(len(self.main.local_path)):
                                # print(self.main.local_path[i],' ',rfid)
                                if self.main.local_path[i] == rfid:
                                    self.main.next_rfid=self.main.local_path[i+1]
                                    self.main.rfid=rfid
                                    # print(self.main.next_rfid,self.main.rfid)
                                    break
                else:
                    self.main.print_log('未知数据')
                    print([hex(i) for i in data])
if __name__ == '__main__':
    server=Server()