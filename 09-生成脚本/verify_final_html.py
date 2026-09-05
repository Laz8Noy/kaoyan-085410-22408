# -*- coding: utf-8 -*-
"""终极版 HTML 完整性验证"""
import io, re

p = r'<SOURCE_DIR>\02_院校数据_原有\全国408_085410双非热度版_终极版_20260824.html'
h = io.open(p, encoding='utf-8').read()
print('总长:', len(h))
s = h.find('<script>')
e = h.find('</script>')
print('script 区间:', s, '-', e)
gk = h.find('id="gaikao"')
mt = h.find('id="mentors"')
kq = h.find('id="kq"')
print('gaikao:', gk, '| mentors:', mt, '| kq:', kq)
print('新区块在 script 前?', gk < s and mt < s and kq < s)
sec_gk = h[h.find('<section id="gaikao"'):h.find('<section id="mentors"')]
sec_mt = h[h.find('<section id="mentors"'):h.find('<section id="kq"')]
print('改考表格 <tr> 数:', sec_gk.count('<tr'))
print('导师卡片数:', sec_mt.count('detail-card'))
t = re.search(r'<title>(.*?)</title>', h)
print('标题:', t.group(1) if t else None)
h1 = re.search(r'<h1[^>]*>(.*?)</h1>', h)
print('h1:', h1.group(1) if h1 else None)
# 各主要 section 是否都在
for sid in ['overview', 'ratio', 'heat', 'viz', 'kq', 'recommender', 'timeline', 'career', 'detail', 'other408']:
    print(f'  section#{sid}:', h.find(f'id="{sid}"'))
