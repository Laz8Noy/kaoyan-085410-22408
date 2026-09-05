# -*- coding: utf-8 -*-
"""分析模板剩余结构：O 数组、SRCS、考情明细区块 HTML、日期文本"""
import io, re

p = r'<SOURCE_DIR>\02_院校数据_原有\全国408_085410双非热度版_20260820.html'
html = io.open(p, encoding='utf-8').read()
scripts = re.findall(r'<script>(.*?)</script>', html, re.S)
s = scripts[0]

# O 数组
m = re.search(r'var O=\[(.*?)\];', s, re.S)
if m:
    objs = re.findall(r'\{[^{}]*\}', m.group(1))
    print(f'=== O 数组: {len(objs)} 对象 ===')
    for o in objs[:5]:
        print(' ', o[:250])
    print()

# SRCS
m = re.search(r'var SRCS=\[(.*?)\];', s, re.S)
if m:
    objs = re.findall(r'\{[^{}]*\}', m.group(1))
    print(f'=== SRCS: {len(objs)} 条 ===')
    for o in objs[:4]:
        print(' ', o[:200])
    print()

# 考情明细区块 id
for mid in re.findall(r'<section[^>]*id="([^"]+)"', html):
    print('section id:', mid)
for mid in re.findall(r'id="([^"]*kq[^"]*)"', html):
    print('kq id:', mid)

# 日期文本
for m in re.finditer(r'20(?:26|25)[\-\d]*', html):
    pass
dates = set(re.findall(r'20(?:25|26|27)[\-\/年][\d\-\/年]+|2026-\d{2}-\d{2}|2026\.\d{2}\.\d{2}', html))
print('\n日期出现:', sorted(dates)[:20])
