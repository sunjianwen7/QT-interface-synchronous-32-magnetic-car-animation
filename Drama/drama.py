import threading

from loguru import logger
from tools.tool import sengmsg_tostr
class Drama():
    def __init__(self,car,android,ota,amd):
        self.__car=car
        self.__amd=amd
        self.__ota=ota
        self.__android=android
        self.__listen_ota_flag=False
        self.__listen_android_flag = False
        threading.Thread(target=self.__listen_ota).start()
        threading.Thread(target=self.__listen_android).start()
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
        pass
    def TODO2(self):
        self.__Real_car_go(1,2)
        logger.info("事件2结束")
        self.__android._client_socket.send(bytes.fromhex("55 0a 02 56"))
    def TODO3(self):
        self.__Real_car_go(2,3)
        logger.info("事件3结束")
        self.__android._client_socket.send(bytes.fromhex("55 0a 03 56"))
        #TODO stop and run
    def TODO4(self):
        self.__Real_car_go(3,4)
        logger.info("事件4结束")
        self.__android._client_socket.send(bytes.fromhex("55 0a 04 56"))
    def TODO5(self):
        # while True:
        #     if self.red_green_led=="green":
        #         break
        self.__Real_car_go(4, 5)
        logger.info("事件5结束")
        self.__android._client_socket.send(bytes.fromhex("55 0a 05 56"))
    def TODO6(self):
        self.__Real_car_go(5, 6)
        logger.info("事件6结束")
        self.__android._client_socket.send(bytes.fromhex("55 0a 06 56"))
    def TODO7(self):
        self.__Real_car_go(6, 1)
        logger.info("事件7结束")
        self.__android._client_socket.send(bytes.fromhex("55 0a 07 56"))
    def TODO8(self):
        pass
    def TODO9(self):
        pass