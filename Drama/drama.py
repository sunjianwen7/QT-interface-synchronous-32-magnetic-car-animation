import threading
import time

from loguru import logger

from Socket_Node.Socket import Traffic_Client
from tools.tool import sengmsg_tostr
class Drama():
    def __init__(self,car,android,ota,amd,zhaji):
        self.event = 0
        self.__car=car
        self.__amd=amd
        self.__ota=ota
        self.__android=android
        self.__zhaji=zhaji
        self.__traffic=Traffic_Client()
        self.__listen_ota_flag=False
        self.__listen_android_flag = False
        threading.Thread(target=self.__listen_ota).start()
        threading.Thread(target=self.__listen_android).start()
        threading.Thread(target=self.__zhaji_led_range).start()
    def __listen_android(self):
        while True:
            if self.__listen_android_flag:
                break
            if self.__android.get_car:
                self.__android.get_car=False
                if self.__car.car_flag:
                    self.__android._client_socket.send(bytes.fromhex("55 0c 00 56"))
                else:
                    self.__android._client_socket.send(bytes.fromhex("55 0c 01 56"))
            if self.__android.get_charge:
                self.__android.get_charge=False
                seng_data="55 0b {} 56".format(str(hex(self.__car._charge))[2:])
                self.__android._client_socket.send(bytes.fromhex(seng_data))
    def __listen_ota(self):
        while True:
            if self.__listen_ota_flag:
                break
            if self.__ota.car_control!=-1:

                if self.__ota.car_control==0:
                    self.__car._car_run()
                    logger.info("车辆运动")
                elif self.__ota.car_control == 1:
                    self.__car._car_stop()
                    logger.info("车辆停止")
                else:
                    logger.error("ota车辆控制数据错误")
                self.__ota.car_control=-1
            if self.__ota.led_control!=-1:
                if self.__ota.led_control==0:
                    self.__car._car_open_led()
                    logger.info("车灯常亮")
                elif self.__ota.led_control==1:
                    self.__car._car_close_led()
                    logger.info("车灯关闭")
                elif self.__ota.led_control==2:
                    self.__car._car_blink_led()
                    logger.info("车灯闪烁")
                else:
                    logger.error("ota车灯控制数据错误")
                self.__ota.led_control=-1

    def __zhaji_led_range(self):
        while True:
            if self.__car.rfid == 7 and self.event==4:
                pass
            if self.__car.rfid == 16 and self.event !=0:
                print("炸鸡开")
                self.__zhaji._zhaji_open(1)
                time.sleep(1.5)
                self.__zhaji._zhaji_close(1)
                self.event=0
            if self.__car.rfid == 1 and self.event == 2:
                print("轧机开")
                self.__zhaji._zhaji_open(2)
                time.sleep(1.5)
                self.__zhaji._zhaji_close(2)
                self.event=0
            #TODO 7触发红绿灯
    def __Real_car_go(self,start,end):
        if self.__car.car_flag :
            data=self.__Path_planning(start,end)
            self.__car._client_socket.send(data)
            logger.info("发送数据"+str([hex(i) for i in data]))
            while True:
                if self.__car.rfid==end:
                    break
        else:
            logger.warning("socket没有握手")
    def __Path_planning(self, start, end):
        path,last_node = self.__amd.Calculate_path(start,end)
        send_message = [55, 0, 2]
        index = 1
        for i in path:
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
        send_message.append(0)
        send_message.append(index)
        send_message.append(0)
        send_message.append(last_node)
        send_message.append(0)
        send_message.append(3)
        send_message.append(0)
        send_message.append(1)
        send_message.append(56)
        return sengmsg_tostr(send_message)
    def TODO1(self):
        self.__Real_car_go(6, 1)
        logger.info("到达点1")
        self.__android._client_socket.send(bytes.fromhex("55 0e 01 56"))
    def TODO2(self):
        self.__Real_car_go(1,2)
        logger.info("到达点2")
        self.__android._client_socket.send(bytes.fromhex("55 0e 02 56"))
    def TODO3(self):
        self.__Real_car_go(2,3)
        logger.info("到达点3")
        self.__android._client_socket.send(bytes.fromhex("55 0e 03 56"))
    def TODO4(self):
        self.__Real_car_go(3, 8)
        while True:
            if self.__traffic.get_traffic():
                break
        self.__Real_car_go(8, 4)
        logger.info("到达点4")
        self.__android._client_socket.send(bytes.fromhex("55 0e 04 56"))
    def TODO5(self):

        self.__Real_car_go(4, 9)
        time.sleep(2)
        self.__Real_car_go(9, 5)
        logger.info("到达点5")
        self.__android._client_socket.send(bytes.fromhex("55 0e 05 56"))
    def TODO6(self):
        self.__Real_car_go(5, 6)
        logger.info("到达点6")
        self.__android._client_socket.send(bytes.fromhex("55 0e 06 56"))