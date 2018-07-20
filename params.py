# -*- coding:utf8 -*-
"""参数加密部分"""
import sys
import random
import hashlib


reload(sys)
sys.setdefaultencoding("utf8")


def get_nonce():
    """
    js是for i in range(500),没卵用，直接range(9)取数
    随机选择9个数
    """
    varchar_list = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']
    after_choice = []
    for i in range(9):
        choice_number = int(16*random.random())
        after_choice.append(varchar_list[choice_number])
    final_result = "".join(map(str, after_choice))
    return final_result


def get_xyz(login_url, nonce, params):
    """
    :param login_url: 请求接口路径 "/xdnphb/list/day/rank"
    :param params: 请求时附带参数 {"end":"2017-04-28","rank_name":"时事","rank_name_group":"资讯","start":"2017-05-16"}
    :param nonce: 上一步得到的nonce
            app_key = "joker" 固定
            md5(接口路径+App_key+请求参数.sort()+nonce)
    :return:
    """
    uri = login_url.replace("http://www.newrank.cn", "")
    has_bool_key = [k for k, v in params.items() if v is False or v is True]
    has_bool_key = has_bool_key[0] if len(has_bool_key) != 0 else None
    if has_bool_key is not None:
        params[has_bool_key] = "false" if params[has_bool_key] is False else "true"
    key_list = [i for i in params.keys()]
    key_list.sort()
    middle_params = ["&"+i+"="+params[i] for i in key_list]
    middle_params = uri + "?AppKey=joker" + "".join(map(str, middle_params)) + "&nonce=%s" % nonce
    xyz = hashlib.md5()
    xyz.update(middle_params)
    xyz = xyz.hexdigest()
    return xyz
