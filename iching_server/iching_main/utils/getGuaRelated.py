# coding=utf8
import random

gua_dict = {
    '阳阳阳': '乾',
    '阴阴阴': '坤',
    '阴阳阳': '兑',
    '阳阴阳': '震',
    '阳阳阴': '巽',
    '阴阳阴': '坎',
    '阳阴阴': '艮',
    '阴阴阳': '离'
}

number_dict = {
    0: '初爻',
    1: '二爻',
    2: '三爻',
    3: '四爻',
    4: '五爻',
    5: '六爻',
}

def get_3_coins():
    return [random.randint(0, 1) for _ in range(3)]

def get_yin_yang(coin_result):
    return "阳" if sum(coin_result) > 1.5 else "阴"

def get_gua_xiang(yinyang_res):
    return gua_dict[''.join(yinyang_res)]

def format_coin_result(coin_result,i):
    return f'{number_dict[i]}为' + ''.join([f'{"背" if i>0.5 else "字"}' for i in coin_result]) + '为' + get_yin_yang(coin_result)
