from tools.tool import sengmsg_tostr
class Drama():
    def __init__(self,car,amd):
        self.car=car
        self.amd=amd
    def __Real_car_go(self,start,end):
        if self.car.car_flag :
            data=self.__Path_planning(start,end)
            self.car.client_socket.send(data)
            print("发送数据"+str([hex(i) for i in data]))
        else:
            print("socket没有握手")
    def __Path_planning(self, start, end):
        path,last_node = self.amd.Calculate_path(start,end)
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
        #TODO 灯光控制
    def TODO2(self):
        self.__Real_car_go(1,2)
    def TODO3(self):
        self.__Real_car_go(2,3)
        #TODO stop and run
    def TODO4(self):
        self.__Real_car_go(3,4)
    def TODO5(self):
        # while True:
        #     if self.red_green_led=="green":
        #         break
        self.__Real_car_go(4, 5)
    def TODO6(self):
        self.__Real_car_go(5, 6)
    def TODO7(self):
        self.__Real_car_go(6, 1)
    def TODO8(self):
        pass
    def TODO9(self):
        pass