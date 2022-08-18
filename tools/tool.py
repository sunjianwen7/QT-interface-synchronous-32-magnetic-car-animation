import os
from functools import reduce


def sengmsg_tostr(msg_list):
    msg_str = ''
    for i in msg_list:
        msg_str += str(i)
        if str(i) != '0':
            msg_str += ' '
    data = bytes.fromhex(msg_str)
    return data
def release_port(port):
    "释放指定端口"
    # 查找端口对应的pid
    cmd_find = 'netstat -apn |grep %s' % port
    # 返回命令执行结果
    a=os.popen(cmd_find).read()
    print(a)
    result = a.split(' ')
    if result and result[0] != '':
        result0 = result[24]
        cmd_kill = 'kill -9 %s' % result0
        os.popen(cmd_kill)
    else:
        print('no port')
def recode_bag(data_list):
    txt = open('temp.txt', mode='w')
    txt.writelines(data_list)
    txt.close()


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