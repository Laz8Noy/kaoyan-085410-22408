# -*- coding: utf-8 -*-
"""排查：注入位置是否在正确 HTML 区域，JS 是否被破坏"""
import io, re

p = r'<SOURCE_DIR>\02_院校数据_原有\全国408_085410双非热度版_终极版_20260824.html'
html = io.open(p, encoding='utf-8').read()

# kq 锚点第一次出现位置
i_kq = html.find('<section id="kq">')
print('kq 锚点 idx:', i_kq)
print('kq 前 200 字符:', repr(html[i_kq-200:i_kq]))

# script 块边界
i_script_end = html.find('</script>')
print('\n首个 </script> idx:', i_script_end)
print('kq 在 script 内?', i_kq < i_script_end)

# gaikao 注入位置
i_gk = html.find('id="gaikao"')
print('\ngaikao idx:', i_gk, '| 在 kq 之前?', i_gk < i_kq)

# 检查 gaikao/mentors 区块是否完整闭合
i_mt = html.find('id="mentors"')
print('mentors idx:', i_mt)

# 检查 table 行数（新改考表）
sec = html[html.find('<section id="gaikao"'):html.find('<section id="mentors"')]
trs = sec.count('<tr')
print('\n改考区块 <tr> 数:', trs)
sec2 = html[html.find('<section id="mentors"'):html.find('<section id="kq"')]
dc = sec2.count('detail-card')
print('导师区块 detail-card 数:', dc)
