# -*- coding: utf-8 -*-
"""解析模板 HTML：提取 JS 数据结构与渲染逻辑骨架"""
import io, re

p = r'<SOURCE_DIR>\02_院校数据_原有\全国408_085410双非热度版_20260820.html'
html = io.open(p, encoding='utf-8').read()

# 提取所有 <script> 块
scripts = re.findall(r'<script>(.*?)</script>', html, re.S)
print('script 块数:', len(scripts))
for i, s in enumerate(scripts):
    print(f'\n--- script[{i}] 长度 {len(s)} ---')
    # 前 300 字符
    print(s[:300])
    # 关键声明
    for decl in re.findall(r'(var|let|const)\s+(\w+)\s*=', s):
        print('  声明:', decl[0], decl[1])
