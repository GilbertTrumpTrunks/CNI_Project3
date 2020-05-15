
# -*- coding = utf-8 -*-

import socket
####begin全局常量
operation={1:'申请许可证',2:'使用许可证',3:'退出程序',4:'保持在线'}
lisenceType = {1:'家庭版',2:'公司版',3:'个人版'}
maxUser={1:5,2:50,3:1}
####end全局常量

####begin全局变量
#管理员账户
Account={'admin':'admin'}
#在线用户数量
lisenceUser={'0300000001':0}
#每种账户的已发放的序列号数量
lisenceNum = [-1,0,0,1]
####end全局变量

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
    print('A new connection from '+str(addr))
    msg = data.decode('utf-8').split(' ',2)
    account = msg[0]
    password = msg[1]
    #关于lisenceType的输入错误在client处理了
    lisenceType = int(msg[2])
    #账号密码错误
    if(account not in Account.keys() or Account[account]!=password):
        send_data(client,addr,'Account or Password Error,Please Retry')
        return None
    else:
    #开始申请
        lisenceNum[lisenceType]=lisenceNum[lisenceType]+1
        serialNumber =  generateSerialNumber(lisenceType,lisenceNum[lisenceType])
        lisenceUser[str(serialNumber)]=0
        send_data(client,addr,'Apply Successfully!\nPlease Keep Your Serial Number:'+serialNumber+'\n')
        
        
            
    
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
        
main()
