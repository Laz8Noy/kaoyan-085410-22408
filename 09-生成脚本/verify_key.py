# -*- coding: utf-8 -*-
"""核对模板关键院校数据 vs 主表20260820 md 最新数据"""
import io, re, json

T = r'<SOURCE_DIR>\02_院校数据_原有\全国408_085410双非热度版_20260820.html'
html = io.open(T, encoding='utf-8').read()
s = re.findall(r'<script>(.*?)</script>', html, re.S)[0]

def grab(name):
    m = re.search(r'var ' + name + r'=\[(.*?)\];', s, re.S)
    objs = []
    for o in re.finditer(r'\{[^{}]*\}', m.group(1)):
        try:
            objs.append(json.loads(o.group(0)))
        except: pass
    return objs

all_objs = grab('S') + grab('C')

# 关键院校：主表最新线 vs 模板线
checks = {
    '郑州大学': 335, '华中师范大学': 264, '上海大学': '计科院305/未来334',
    '暨南大学': 331, '云南大学': 339, '北京交通大学': 326,
    '河南大学': 264, '成都理工大学': 308, '广州大学': '网安300/AI310',
    '浙江理工大学': 335, '天津理工大学': 315, '湖南科技大学': 338,
    '青岛大学': 264, '成都信息工程大学': 264, '重庆科技大学': 264,
    '河南工业大学': 264, '兰州理工大学': 254, '宁夏大学': 254,
    '桂林电子科技大学': 254, '中国民用航空飞行学院': 264,
    '安庆师范大学': 264, '中北大学': 319, '青海大学': 254,
    '海南大学': 254, '贵州大学': 303, '陕西师范大学': 264,
    '华南农业大学': 294, '西南交通大学': 310, '辽宁大学': 311,
}
print('=== 模板中关键院校线 ===')
for name, expect in checks.items():
    hits = [o for o in all_objs if o['n'] == name]
    for o in hits:
        print(f"{name}: 模板线={o.get('l')} (主表期望 {expect}) | plan={o.get('plan')} | K科目见映射")
