# -*- coding: utf-8 -*-
"""检查模板是否含：2027改考动态、导师研究方向、避坑提醒"""
import io, re

T = r'<SOURCE_DIR>\02_院校数据_原有\全国408_085410双非热度版_20260820.html'
html = io.open(T, encoding='utf-8').read()

checks = {
    '2027改考': ['2027 改考', '改考动态', '改考', '反向改考', '南信大', '上海电力', '长春工业'],
    '导师': ['导师', '研究方向', '杨云', '高源', '段书凯', '李进'],
    '避坑': ['避坑', '11408', '勿报', '⚠️'],
    '时间轴': ['时间轴', '预报名', '初试', '12/19', '12月19'],
    '就业': ['就业', '学费', '奖助'],
}
for grp, kws in checks.items():
    found = {k: html.count(k) for k in kws if k in html}
    print(f'=== {grp} ===')
    for k, c in found.items():
        print(f'  {k}: {c}次')
    if not found:
        print('  无')

# 其他408附表内容
print('\n=== O 附表前几行 ===')
s = re.findall(r'<script>(.*?)</script>', html, re.S)[0]
m = re.search(r'var O=\[(.*?)\];', s, re.S)
print(m.group(1)[:500] if m else '无')
