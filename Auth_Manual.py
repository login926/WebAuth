import base64
import requests
import re
import getpass

class LoginStatus():
    def __init__(self,statusid,ip,location,domain,status):
        r = requests.post('http://n.njcit.cn/index.php/index/init')
        if(r.json()['status'] == 1 ):
            self.statusid = r.json()['status']
            self.ip = r.json()['logout_ip']
            self.location = r.json()['logout_location']
            self.domain = r.json()['logout_domain']
            self.status = '已登陆'
        else:
            r = requests.post('http://n.njcit.cn/')
            self.statusid = statusid
            self.ip = re.findall("(?<=登录IP:).*?(?=<\/span)",r.text)[0]
            self.location = location
            self.domain = domain
            self.status = '未登陆'

CurrentLogin = LoginStatus(0,'0.0.0.0','0','0','未登陆')
if(CurrentLogin.statusid == 1):
    print('当前已登陆')
    print('登陆IP：',CurrentLogin.ip)
    print('登陆位置：',CurrentLogin.location)
    print('登陆域：',CurrentLogin.domain)
    while True:
        try:
            print('输入数字选择操作 1.退出登陆并退出程序 2.退出程序 3.退出登陆并重新登陆:')
            SelectNum = int(input())
        except:
            print('无效输入')
            continue
        if (SelectNum < 1 or SelectNum > 3):
            print('无效输入')
            continue
        else:
            break
    if (SelectNum == 1):
        r = requests.post('http://n.njcit.cn/index.php/index/logout')
        CurrentLoginOut = LoginStatus(0,'0.0.0.0','0','0','未登陆')
        if (CurrentLoginOut.statusid == 0 ):
            print('已退出登陆，886')
            exit()
        else:
            print('未能退出登陆，请重试')
            exit()
    elif(SelectNum == 3):
        r = requests.post('http://n.njcit.cn/index.php/index/logout')
        CurrentLoginOut = LoginStatus(0,'0.0.0.0','0','0','未登陆')
        if (CurrentLoginOut.statusid == 0 ):
            print('已退出登陆，请重新登陆')
        else:
            print('未能退出登陆，请重试')
            exit()
    else:
        print('886')
        exit()
else:
    print('当前未登陆')
    print('当前IP：',CurrentLogin.ip)

username = input('登陆名：')
pwd = getpass.getpass('密码（输入时不会显示）：')
password = base64.b64encode(pwd.encode(encoding="utf-8")).decode()

phone = {'user-agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Mobile Safari/537.36'}
pc = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'}

while True:
    try:
        print('输入数字选择登陆域')
        logindomainid = int(input('1.电脑 ￥0.4/h  2.手机 ￥6/m ：'))
    except:
        print('无效输入')
        continue
    if (logindomainid < 1 or logindomainid > 2):
        print('无效输入')
        continue
    else:
        break
if (logindomainid == 1):
    headers = pc
    logindomain = 'student'
else:
    headers = phone
    logindomain = 'studentphone'
print('正在登陆')
logining = requests.post('http://n.njcit.cn/index.php/index/login', data={'username': username, 'domain': logindomain, 'password': password, 'enablemacauth': '0'},headers=headers)
CurrentLogined = LoginStatus(0,'0.0.0.0','0','0','未登陆')
if(CurrentLogined.statusid == 1):
    print('当前已登陆')
    print('登陆IP：',CurrentLogined.ip)
    print('登陆位置：',CurrentLogined.location)
    print('登陆域：',CurrentLogined.domain)
else:
    print('登陆失败，请确认用户名密码正确或当前登陆位置有效')
