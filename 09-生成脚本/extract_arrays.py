# -*- coding: utf-8 -*-
"""提取模板 JS 数组定义（S/C/K/O/SRCS）的原始文本到临时文件，供分析字段格式"""
import io, re

p = r'<SOURCE_DIR>\02_院校数据_原有\全国408_085410双非热度版_20260820.html'
html = io.open(p, encoding='utf-8').read()
scripts = re.findall(r'<script>(.*?)</script>', html, re.S)
s = scripts[0]

for name in ['S', 'C', 'K', 'O', 'SRCS']:
    m = re.search(r'var ' + name + r'=\[(.*?)\];', s, re.S)
    if m:
        print(f'=== {name}: {len(m.group(1))} 字符 ===')
        txt = m.group(1)
        # 打印前 3 条完整对象
        objs = re.findall(r'\{[^{}]*\}', txt)
        print(f'对象数(粗略): {len(objs)}')
        for o in objs[:3]:
            print(' ', o[:400])
        print()
    else:
        m2 = re.search(r'var ' + name + r'=(\{.*?\});', s, re.S)
        if m2:
            print(f'=== {name}: 对象形式 {len(m2.group(1))} 字符 ===')
            print(m2.group(1)[:800])
        else:
            print(f'=== {name}: 未找到 ===')
        print()
