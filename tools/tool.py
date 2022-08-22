import os
from functools import reduce


def sengmsg_tostr(msg_list):
    msg_str = ''
    for i in msg_list:
        msg_str += str(i)
        if str(i) != '0':
            msg_str += ' '
    data = bytes.fromhex(msg_str)
    print('发送数据',data)
    return data
def release_port(port):
    "释放指定端口"
    # 查找端口对应的pid
    cmd_find = 'netstat -antup |grep %s' % port
    # 返回命令执行结果
    a=os.popen(cmd_find).read()
    result0 = a.split(' ')
    result=[]
    for i in result0:
        if i !='':
            result.append(i)
    pid=0
    for i in result:
        if i =='0.0.0.0:1234':
            pid=int(result[result.index(i)+3].split('/')[0])
            break
    if pid!=0:
        cmd_kill = 'kill -9 %s' % pid
        os.popen(cmd_kill)
def recode_bag(data_list):
    txt = open('Drama/temp.txt', mode='w')
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
if __name__ == '__main__':
    release_port(1234)