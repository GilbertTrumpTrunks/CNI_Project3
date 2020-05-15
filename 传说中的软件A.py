import socket
import os


addr = ("localhost", 8887)
serialNumber = '0000000000'
status = 0

def writeSerialNumber():
    with open ('serialNumber.txt','wb') as f:
        f.write(serialNumber.encode('utf-8'))
def readSerialNumber():
    if(os.path.exists('serialNumber.txt')):
        with open ('serialNumber.txt','rb') as f:
            serialNumber = f.read().decode('utf-8')
def useLisence(client,addr,serialNumber):
    send_data(client,addr,'2')
    ####Status = 0:初次登入
    ####Status = 1:再次确认
    global status
    send_data(client,addr,str(serialNumber)+' '+str(status))
    dat, addr = client.recvfrom(1024)
    data=dat.decode('utf-8')
    if 'OK:' in data:
        print(data)
        status = 1
        return True
    elif 'Error:' in data:
        print(data)
        return False
        
def run():
    print('这是一个a+b问题:\n输入end退出,输入任意内容开始')
    s = input()
    if(s == 'end'):
        return False
    a = int(input('请输入加数:'))
    b = int(input('请输入加数:'))
    print('你得到了'+str(a+b))
    return True
def changeSerialNumber():
    inputok = False
    #while(inputok ==False):
    global serialNumber
    serialNumber = input('请输入十位序列号:')
            #try :
                #int(serialNumber)
            #except ValueError:
                #inputok = False
            #finally:
            #if(len(serialNumber)==10):

    inputok == True     
    writeSerialNumber()
    return None
def endOfProgramA():
        send_data(client,addr,'3')
        send_data(client,addr,str(serialNumber))
        exit(0)
        
def send_data(client,addr,data):
    client.sendto(data.encode('utf-8'), addr)
            
def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    global serialNumber
    changeSerialNumber()
    readSerialNumber()
    while True:
        opt = int(input('功能:\n1.修改授权\n2.开始程序\n3.退出\n'))
        if(opt ==1):
              changeSerialNumber()
        elif(opt == 2):
            if(useLisence(client,addr,serialNumber)   ==True):
                print('Program Running')
                while(run()==True):
                    int(1)##无效内容
            else:
                print('Please Try Again Later')
        elif(opt == 3):
            endOfProgramA()
        


    run()



main()
