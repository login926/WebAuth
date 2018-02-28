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

def auth_read(filename):
    try:
        file = open(filename,'r')
    except IOError:
        error = []
        return error
    content = file.readlines()
    for i in range(len(content)):
        content[i] = content[i][:len(content[i])-1]
    file.close()
    return content

CurrentLogin = LoginStatus(0,'0.0.0.0','0','0','未登陆')
if(CurrentLogin.statusid == 1):
    print('当前已登陆')
    print('登陆IP：',CurrentLogin.ip)
    print('登陆位置：',CurrentLogin.location)
    print('登陆域：',CurrentLogin.domain)
    exit()

phone = {'user-agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Mobile Safari/537.36'}
pc = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'}

AuthInfo = auth_read('Auth.txt')
username = AuthInfo[0]
password = AuthInfo[1]
logindomainid = int(AuthInfo[2])
if(logindomainid == 1):
    logindomain = 'studentphone'
    headers = phone
else:
    logindomain = 'student'
    headers = pc

logining = requests.post('http://n.njcit.cn/index.php/index/login', data={'username': username, 'domain': logindomain, 'password': password, 'enablemacauth': '0'},headers=headers)
CurrentLogined = LoginStatus(0,'0.0.0.0','0','0','未登陆')
if(CurrentLogined.statusid == 1):
    print('当前已登陆')
    print('登陆IP：',CurrentLogined.ip)
    print('登陆位置：',CurrentLogined.location)
    print('登陆域：',CurrentLogined.domain)
else:
    print('登陆失败，请确认用户名密码正确或当前登陆位置有效')
