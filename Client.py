# -*- coding = utf-8 -*-
import socket

operation={1:'申请许可证',2:'使用许可证',3:'退出程序',4:'保持在线'}
lisenceType = {1:'家庭版',2:'公司版',3:'个人版'}
addr = ("localhost", 8887)
def showOperation():
    s = ''
    for key,value in operation.items():
        s+=(str(key)+'.'+value+'\n')
    return s

def applyForALicense(client,addr):
    account=input('账号:')
    password=input('密码:')
    lisenceType=input('类型:')
    ok = False
    while(ok == False):
        try:
            int(lisenceType)
        except ValueError:
            lisenceType=input('类型')
        else:
            ok = True
    data = account + ' ' + password + ' '+lisenceType
    send_data   (client,addr,data)
    data, addr = client.recvfrom(1024)
    print(data.decode('utf-8'))
    return
def send_data(client,addr,data):
    client.sendto(data.encode('utf-8'), addr) 

def main():
    u_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # s.getsockname()  返回套接字自己的地址。
    #print("%s:%s 开始工作" %u_client.getsockname())
     
    while True:
      # 发送数据
        inputok = False
        inp = input('请输入操作数:\n'+showOperation()+'input>>>')
        while(inputok == False):
            try:
                opt = int (inp)
                if(opt>=0 and opt<=4):
                    inputok = True
            except TypeError:
                continue
            finally:
                print('执行操作:'+str(operation[opt]))
        if(opt==1):
                send_data(u_client,addr,'1')
                applyForALicense(u_client,addr)
                

def comment(u_client):
        u_client.sendto(data.encode('utf-8'), ("localhost", 8887)) 
         
     
        # 接收数据
        data, addr = u_client.recvfrom(1024)
        print("客户端接收信息的来源： %s:%s" %addr)
        print("客户端接收信息的数据： %s" %data.decode('utf-8'))


main()
