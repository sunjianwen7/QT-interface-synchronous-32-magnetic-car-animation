import os
import datetime
from functools import reduce
from loguru import logger
class Logings:
    __instance = None
    # 文件名称，按天创建
    DATE = datetime.datetime.now().strftime('%Y-%m-%d')
    # 项目路径下创建log目录保存日志文件
    logpath = os.path.join(os.getcwd(), "logs")  # 拼接指定路径
    if not os.path.isdir(logpath):
        os.makedirs(logpath)
    logger.add('%s/%s.log' % (logpath, DATE),  # 指定文件
               format="{time:YYYY-MM-DD HH:mm:ss}  | {level}> {elapsed}  | {message}",
               encoding='utf-8',
               retention='1 days',  # 设置历史保留时长
               backtrace=True,  # 回溯
               diagnose=True,  # 诊断
               enqueue=True,  # 异步写入
               # rotation="5kb",  # 切割，设置文件大小，rotation="12:00"，rotation="1 week"
               # filter="my_module"  # 过滤模块
               # compression="zip"   # 文件压缩
               )

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super(Logings, cls).__new__(cls, *args, **kwargs)
        return cls.__instance
def sengmsg_tostr(msg_list):
    msg_str = ''
    for i in msg_list:
        msg_str += str(i)
        if str(i) != '0' :
            msg_str += ' '
    msg_str=msg_str[:-1]
    data = bytes.fromhex(msg_str)
    return data
def release_port(port):
    "释放指定端口"
    # 查找端口对应的pid
    cmd_find = 'lsof -i -P -n |grep %s' % port
    # 返回命令执行结果
    a=os.popen(cmd_find).read()
    result0 = a.split(' ')
    result=[]
    for i in result0:
        if i !='':
            result.append(i)
    if result:
        pid=result[1]
        cmd_kill = 'kill -9 %s' % pid
        os.popen(cmd_kill)
def chars2num(s):
    chars_num = {"0":0,"1":1,"2":2,"3":3,"4":4,"5":5,"6":6,"7":7,"8":8,"9":9}
    return chars_num[s]
def point_left(x,y):
    return x*10 + y
def point_right(x,y):
    return x*0.1 + y
def str2float(s):
    chars = s
    chars = chars.split(".")
    num = reduce(point_left,map(chars2num,chars[0])) + reduce(point_right,list(map(chars2num,chars[1]))[::-1])*0.1
    return num
logs=Logings()
if __name__ == '__main__':
    release_port(1234)