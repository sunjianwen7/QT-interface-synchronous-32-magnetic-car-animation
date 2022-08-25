import threading

from AMGraph_Node.amgraph_test import AMD_Map
from Drama.drama import Drama
from Socket_Node import Socket
from Socket_Node.Socket import Android_Server

class Densified_Sand_Table():
    def __init__(self):
        amd=AMD_Map()
        car = Socket.Car_Server(1233)
        print("车辆初始完毕")
        self.drama=Drama(car,amd)
        print("场景初始完毕")
        self.android = Android_Server(1238)
        print("安卓初始完毕")
        self.AndroidEvent()
    def AndroidEvent(self) -> None:
        while True:
            event=self.android.Drama
            if event==1:
                print('事件1')
                self.drama.TODO1()
                self.android.Drama=0
            elif event==2:
                print('事件2')
                self.drama.TODO2()
                self.android.Drama = 0
            elif event ==3:
                print('事件3')
                self.drama.TODO3()
                self.android.Drama = 0
            elif event ==4:
                print('事件4')
                self.drama.TODO4()
                self.android.Drama = 0
            elif event ==5:
                print('事件5')
                self.drama.TODO5()
                self.android.Drama = 0
            elif event ==6:
                print('事件6')
                self.drama.TODO6()
                self.android.Drama = 0
            elif event ==7:
                print('事件7')
                self.drama.TODO7()
                self.android.Drama = 0
            elif event ==8:
                print('事件8')
                self.drama.TODO8()
                self.android.Drama = 0
            elif event ==9:
                print('事件9')
                self.drama.TODO9()
                self.android.Drama = 0
if __name__=='__main__':
    Densified_Sand_Table()
