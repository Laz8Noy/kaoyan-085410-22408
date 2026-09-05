# -*- coding: utf-8 -*-
"""定位 O/SRCS 实际定义与考情明细区块渲染"""
import io, re

p = r'<SOURCE_DIR>\02_院校数据_原有\全国408_085410双非热度版_20260820.html'
html = io.open(p, encoding='utf-8').read()
scripts = re.findall(r'<script>(.*?)</script>', html, re.S)
s = scripts[0]

# O 和 SRCS 用不同定义方式
for name in ['O', 'SRCS', 'ov', 'KQ']:
    for pat in [r'var ' + name + r'=(\[.*?\]);', r'var ' + name + r'=(\{.*?\});', r'const ' + name + r'=(\[.*?\]);']:
        m = re.search(pat, s, re.S)
        if m:
            print(f'=== {name} 定义({len(m.group(1))}字符) ===')
            print(m.group(1)[:600])
            print()
            break

# 考情明细渲染函数
for fn in re.finditer(r'function\s+(\w+)\s*\(', s):
    pass
fns = set(re.findall(r'function\s+(\w+)', s))
print('函数名:', sorted(fns))

# 找 kq 相关渲染
for seg in re.finditer(r'kq[\w]*\s*=\s*[\[{\(]', s):
    pass
print('\n=== kq 区块 HTML 定位 ===')
idx = html.find('id="kq"')
print(html[idx-100:idx+400] if idx>=0 else 'not found')
