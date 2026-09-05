# -*- coding: utf-8 -*-
"""定位真正的 HTML 静态 kq 区块（避开 JS 字符串内的 kq）"""
import io, re

p = r'<SOURCE_DIR>\02_院校数据_原有\全国408_085410双非热度版_20260820.html'
html = io.open(p, encoding='utf-8').read()

# 所有出现位置
idxs = [m.start() for m in re.finditer(r'<section id="kq">', html)]
print('所有 <section id="kq"> 位置:', idxs)

# script 边界
sm = re.search(r'<script>', html)
se = html.find('</script>')
print('script 范围:', sm.start(), '-', se)

for i in idxs:
    print(f'  idx {i}: 在 script 内? {sm.start() < i < se} | 前后文: {html[i-60:i+30]!r}')

# HTML 静态区块的 kq（script 之后）
html_idxs = [i for i in idxs if i > se]
print('\nHTML 静态 kq 位置:', html_idxs)
if html_idxs:
    i = html_idxs[0]
    print('静态 kq 前后文:', repr(html[i-100:i+50]))
