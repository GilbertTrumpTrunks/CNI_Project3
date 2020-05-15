
# -*- coding = utf-8 -*-
import os
import socket
import csv
####begin全局常量
operation={1:'申请许可证',2:'使用许可证',3:'退出程序',4:'保持在线'}
lisenceType = {1:'家庭版',2:'公司版',3:'个人版'}
maxUser={1:5,2:50,3:1}
####end全局常量

####begin全局变量
#管理员账户
Account={'admin':'admin'}
Acc_Ser={'admin':'0300000001'}
#在线用户数量
lisenceUser={'0300000001':0}
#每种账户的已发放的序列号数量
lisenceNum = [-1,0,0,1]
####end全局变量
info=[]
def setUp():
    if(os.path.exists('account.csv')):
        lisenceNum = []
        for i in range(4):
            lisenceNum[i]=0
        Account = {}
        Acc_ser = {}
        lisenceUser = {}
        
        with open('account.csv','rb') as f:
            #更新所有的全局变量
            f_csv = csv.reader(f)
            for r in f_csv:
                msg = r
                serialNumber = msg[0]
                serialKind = msg[0][0:2]
                account = msg[1]
                password = msg[2]
                Account[account]=password
                Acc_ser[account]=serialNumber
                lisenceUser[serialNumber]=0;
                lisenceNum[int(serialKind)]=lisenceNum[int(serialKind)]+1
            

####end全局变量
def useLisence(client,addr):
    dat, addr = client.recvfrom(1024)
    data = []
    print(dat)
    data = dat.decode('utf-8').split(' ',1)
    serialNumber = data[0]
    serialKind = int(data[0][0:2])
    status = data[1]
    if(serialNumber not in lisenceUser.keys()):
        send_data(client,addr,'Error: You\'ve entered a WRONG Serial Number')
    elif(status == 1):
        send_data(client,addr,'OK: Continue To Connect')
    elif(status == 0 and lisenceUser[serialNumber]==maxUser[serialKind]):
        send_data(client,addr,'Error: Full Of Visitors')
    else:
        lisenceUser[serialNumber]=lisenceUser[serialNumber]+1
        send_data(client,addr,'OK: Connect successfully')
    return None

def generateSerialNumber(lisenceType,lisenceNum):
    top = str(lisenceType)
    while(len(top)<2):
        top='0'+top
    bott = str(lisenceNum)
    while(len(bott)<8):
        bott='0'+bott
    return top+bott

def applyForALicense(client,addr):
    data, addr = client.recvfrom(1024)
    print('OK: A new connection from '+str(addr))
    msg = data.decode('utf-8').split(' ',2)
    account = msg[0]
    password = msg[1]
    #关于lisenceType的输入错误在client处理了
    lisenceType = int(msg[2])
    #账号密码错误
    if(account in Account.keys()):
        send_data(client,addr,'Error: The Account Has Been Registered,Please Retry')
        return None
    else:
    #开始申请
        lisenceNum[lisenceType]=lisenceNum[lisenceType]+1
        Account[account]=password
        serialNumber =  generateSerialNumber(lisenceType,lisenceNum[lisenceType])
        Acc_Ser[account]=serialNumber
        lisenceUser[str(serialNumber)]=0
        send_data(client,addr,'OK: Apply Successfully!\nPlease Keep Your Serial Number:'+serialNumber+'\n')
        info.append((serialNumber,account,password,lisenceType))
        with open('account.csv','a+',newline = '') as f:
            f_csv = csv.writer(f)
            row = []
            row.append(serialNumber)
            row.append(account)
            row.append(password)
            row.append(serialNumber[0:2])
            f_csv.writerow(row)
        
            
    
def send_data(client,addr,data):
    client.sendto(data.encode('utf-8'), addr) 
    
    

def run():     
    while True:
        # 接收数据
        # u_server.recvfrom() 接收UDP数据，返回值是（data,address）
        data, addr = u_server.recvfrom(1024)
        print("接收信息的来源： %s:%s" %addr)
        print("接收信息的数据： %s" %data.decode('utf-8'))
             
        # 发送原地址数据
        send_data = ("接收到数据："+data.decode('utf-8')+" --Thanks").encode('utf-8')
        u_server.sendto(send_data, addr)
     
        # 退出系统操作
        # if(data.decode('utf-8') == 'exit'):
            # break
    u_server.close()

def main():
    # 绑定端口
    u_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    u_server.bind(('localhost', 8887))
     
    print("%s:%s 开始工作" %u_server.getsockname())
    while True:
        # 接收数据
        # u_server.recvfrom() 接收UDP数据，返回值是（data,address）
        data, addr = u_server.recvfrom(1024)
        print("接收信息的来源： %s:%s" %addr)
        print("接收信息的数据： %s" %data.decode('utf-8'))
        opt = data.decode('utf-8')
        if(opt=='1'):
            applyForALicense(u_server,addr)
        if(opt=='2'):
            useLisence(u_server,addr)
        
main()
