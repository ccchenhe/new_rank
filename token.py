# -*- coding:utf8 -*-
"""登录部分"""
import sys
import time
import requests
from params import get_nonce, get_xyz

reload(sys)
sys.setdefaultencoding("utf8")


MAX_TIMEOUT = 12
MAX_RETRY = 5


def code_login_rank(usr, pwd, retry_num=MAX_RETRY):
    """
    代码登录
    :param usr:  账号
    :param pwd: 加密后密码，固定,未找到加密方式，抓包后获取
    :param retry_num: 重试次数
    :return: token
    """
    login_url = 'http://www.newrank.cn/xdnphb/login/new/usernameLogin'
    login_headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Host": "www.newrank.cn",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/67.0.3396.99 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
    }
    params = {
        "flag": "%.16f" % (int(time.time())*1000),
        "identifyCode": "",
        "password": pwd,
        "username": usr,

    }
    nonce = get_nonce()
    xyz = get_xyz(login_url=login_url, nonce=nonce, params=params)
    params['nonce'] = nonce
    params['xyz'] = xyz
    try:
        r = requests.post(url=login_url, headers=login_headers, data=params, timeout=MAX_TIMEOUT)
        total = r.json()
        token = total['value']['token']
    except Exception, e:
        print "account {usr} login error with {error}".format(usr=usr, error=e)
        token = ''
        if retry_num > 0:
            code_login_rank(usr=usr, pwd=pwd, retry_num=retry_num-1)
    return token
