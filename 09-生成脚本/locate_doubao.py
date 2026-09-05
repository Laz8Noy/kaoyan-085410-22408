# -*- coding: utf-8 -*-
"""在 UTF-16LE 全文中精确定位关键词及其上下文"""
import os, re

base = os.path.expandvars(r'%LOCALAPPDATA%\Doubao\User Data\Default\IndexedDB\chrome_doubao-chat_0.indexeddb.leveldb')
data = b''
for fn in ['000137.log', '000139.ldb']:
    p = os.path.join(base, fn)
    if os.path.exists(p):
        data += open(p, 'rb').read()

t = data.decode('utf-16-le', errors='ignore')
print('全文长度(字符):', len(t))

for kw in ['人工智能', '豆包', '<DIR>', 'deepseek', '考研', '408']:
    idx = t.find(kw)
    if idx >= 0:
        ctx = t[max(0, idx-60): idx+120]
        print(f'\n=== 命中[{kw}] @ {idx} ===')
        print(repr(ctx))
    else:
        print(f'\n未命中 [{kw}]')

# 打印几个大段连续文本，看看结构
print('\n=== 前5000字符概览(前300可打印) ===')
print(repr(t[:300]))
