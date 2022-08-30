from AMGraph_Node.amgraph_test import AMD_Map
from Drama import drama
from Socket_Node.Socket import Android_Server, Car_Server, OTA_Server
from loguru import logger

class Densified_Sand_Table():
    def __init__(self):
        amd=AMD_Map()
        logger.info("等待socket连接")
        car = Car_Server(1234)
        logger.info("车辆初始完毕")
        self.android = Android_Server(1235)
        logger.info("安卓初始完毕")
        ota=OTA_Server(1236)
        logger.info("OTA初始完毕")
        self.drama=drama.Drama(car,self.android,ota,amd)
        logger.info("场景初始完毕")
        self.AndroidEvent()
    def AndroidEvent(self) -> None:
        while True:
            event=self.android.Drama
            if event==1:
                logger.info('事件1')
                self.drama.TODO1()
                self.android.Drama=0
            elif event==2:
                logger.info('事件2')
                self.drama.TODO2()
                self.android.Drama = 0
            elif event ==3:
                logger.info('事件3')
                self.drama.TODO3()
                self.android.Drama = 0
            elif event ==4:
                logger.info('事件4')
                self.drama.TODO4()
                self.android.Drama = 0
            elif event ==5:
                logger.info('事件5')
                self.drama.TODO5()
                self.android.Drama = 0
            elif event ==6:
                logger.info('事件6')
                self.drama.TODO6()
                self.android.Drama = 0

if __name__=='__main__':
    Densified_Sand_Table()
