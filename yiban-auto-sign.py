from bs4 import BeautifulSoup
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
import base64
import json
import os
import re
import requests
import time

def get_public_key(): # 获取登录用的 RSA 公钥和时间戳
    print('Attempting to get the RSA public key for login.')
    attempts = 1
    url = 'https://www.yiban.cn/login'
    while(attempts <= 3):
        print('Number of attempts:', attempts)
        response = session.get(url, headers = headers)
        if(response.status_code != 200):
            print('Failed to request the login page. Response status code:', response.status_code)
            attempts += 1
            continue
        loginPage = BeautifulSoup(response.text, 'html.parser')
        ul = loginPage.find('ul', attrs = {'class': 'login-pr clearfix'})
        if(ul == None):
            print('Public key is not found in the login page. Does Yiban get updated?')
            attempts += 1
            continue
        pubKey = ul.get('data-keys')
        keysTime = ul.get('data-keys-time')
        return pubKey, keysTime
    raise Exception('Failed to get RSA public key. Check the log for more information.')


def login(phone, password, pubKey, keysTime): # 登录
    print('Attempting to login.')
    attempts = 1
    url = 'https://www.yiban.cn/login/doLoginAjax'
    # 对密码进行加密
    rsa = RSA.importKey(pubKey)
    cipher = PKCS1_v1_5.new(rsa)
    encrypted = base64.b64encode(cipher.encrypt(password.encode('utf-8'))).decode('ascii')
    # 请求登录
    while(attempts <= 3):
        print('Number of attempts:', attempts)
        time.sleep(5) # 睡 5s，处理速度太快的话易班服务器会报错 711「pwd 长度必须在 6 至 20 之间」，有更好的处理方法的话欢迎 PR
        payload = {'account': str(phone), 'password': encrypted, 'keysTime': keysTime, 'captcha': None}
        response = session.post(url, data = payload, headers = headers)
        if(response.status_code != 200):
            print('Failed to request login. Response status code:', response.status_code)
            attempts += 1
            continue
        body = response.text.encode('utf-8').decode('unicode_escape')
        try:
            result = json.loads(body)
        except json.JSONDecodeError:
            print('There are something wrong with Yiban login response. Does Yiban get updated? Response body:', body)
            attempts += 1
            continue
        if(result['code'] == 200):
            print('Login successfully.')
            if(not actions):
                print('User ID:', result['data']['user_id'])
            return result['code'], result['data']['user_id']
        else:
            print('Failed to login. Response body:', body)
            attempts += 1
            continue
    raise Exception('Failed to login. Check the log for more information.')


def get_streak(): # 检查连续签到天数
    print('Attempting to get the streak.')
    url = 'https://www.yibanyun.cn/app/sign'
    regex = re.compile('var myday = (.*?);')
    response = session.get(url, headers = headers)
    if(response.status_code != 200):
        print('Failed to request the sign page. Response status code:', response.status_code)
        return
    signPage = BeautifulSoup(response.text, 'html.parser')
    js = signPage.find('script', attrs={'language': 'JavaScript'})
    if(js == None):
        print('Cannot get the streak. Does Yiban get updated?')
        return
    streak = regex.findall(js.text)[0]
    if(streak == None):
        print('Cannot get the streak. Does Yiban get updated?')
        return
    streak = int(streak.split('\'')[1])
    print('Streak:', streak, 'days.')
    return streak


def sign(): # 签到
    print('Attempting to sign in.')
    attempts = 1
    url = 'https://www.yibanyun.cn/app/sign/signin'
    while(attempts <= 3):
        print('Number of attempts:', attempts)
        response = session.post(url, headers = headers)
        if(response.status_code != 200):
            print('Failed to request sign in. Response code:', response.status_code)
            attempts += 1
            continue
        body = response.text.encode('utf-8').decode('unicode_escape')
        try:
            result = json.loads(body)
        except json.JSONDecodeError:
            print('There are something wrong with Yiban sign in response. Does Yiban get updated? Response body:', body)
            attempts += 1
            continue
        if(result['status'] == 1):
            print('Signed in successfully.')
            get_streak()
            return result['status'], result['info']
        elif(result['status'] == 0 and result['info'] == '今天已签到过了'):
            print('Already signed today.')
            return result['status'], result['info']
        else:
            print('Cannot make sure whether signed in successfully. Will try again. Response body:', body)
            attempts += 1
            continue
    raise Exception('Failed to sign in. Check the log for more information.')


if(__name__ == '__main__'):
    # 用户信息
    if(os.getenv('GITHUB_ACTIONS') == 'true'):
        actions = True
        phone = os.getenv('YIBAN_PHONE')
        password = os.getenv('YIBAN_PASSWORD')
    else:
        actions = False
        config = json.load(open('config.json', 'r'))
        phone = config['phone']
        password = config['password']

    # 杂项
    headers = {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 yiban_iOS/5.0.12'} # User-Agent 伪装成易班 iOS 客户端
    session = requests.session()

    pubKey, keysTime = get_public_key()
    login(phone, password, pubKey, keysTime)
    get_streak()
    sign()