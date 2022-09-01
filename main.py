from AMGraph_Node.amgraph_test import AMD_Map
from Drama import drama
from Socket_Node.Socket import Android_Server, Car_Server, OTA_Server,Zhaji_Client
from loguru import logger

class Densified_Sand_Table():
    def __init__(self):

        zhaji=Zhaji_Client()
        amd=AMD_Map()
        logger.info("等待socket连接")
        self.car = Car_Server(1234)
        logger.info("车辆初始完毕")
        self.android = Android_Server(1235)
        logger.info("安卓初始完毕")
        ota=OTA_Server(1236)
        logger.info("OTA初始完毕")
        self.drama=drama.Drama(self.car,self.android,ota,amd,zhaji)
        logger.info("场景初始完毕")
        self.AndroidEvent()
    def AndroidEvent(self) -> None:
        while True:
            drama=self.android.Drama
            if drama==0:
                continue
            print(drama,"+++++++++",self.car.rfid)
            if drama!=self.car.rfid:
                event=(self.car.rfid+1)%6
                if event==0:
                    event=6
                self.drama.event=event
            else:
                event=0
                self.drama.event = 0
                self.android.Drama=0
                self.android._client_socket.send(bytes.fromhex("55 0a 0{} 56".format(str(drama))))
            if event==1:
                logger.info('事件1')
                self.drama.TODO1()
            elif event==2:
                logger.info('事件2')
                self.drama.TODO2()
            elif event ==3:
                logger.info('事件3')
                self.drama.TODO3()
            elif event ==4:
                logger.info('事件4')
                self.drama.TODO4()
            elif event ==5:
                logger.info('事件5')
                self.drama.TODO5()
            elif event ==6:
                logger.info('事件6')
                self.drama.TODO6()

if __name__=='__main__':
    Densified_Sand_Table()
