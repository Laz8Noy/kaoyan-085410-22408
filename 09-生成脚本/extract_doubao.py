# -*- coding: utf-8 -*-
"""豆包聊天记录提取：UTF-16LE 解码 + 文本分段"""
import os, re

base = os.path.expandvars(r'%LOCALAPPDATA%\Doubao\User Data\Default\IndexedDB\chrome_doubao-chat_0.indexeddb.leveldb')
data = b''
for fn in ['000137.log', '000139.ldb']:
    p = os.path.join(base, fn)
    if os.path.exists(p):
        data += open(p, 'rb').read()

t = data.decode('utf-16-le', errors='ignore')

# 提取连续可读文本段
pat = re.compile(r'[\u4e00-\u9fff\u3000-\u303f\uff00-\uffefA-Za-z0-9，。！？、；：“”‘’（）《》\s\.\,\-—…%#@/]{6,}')
segs = pat.findall(t)
print('文本段数:', len(segs))

out = []
for s in segs:
    s = s.strip()
    if len(s) >= 6 and re.search(r'[\u4e00-\u9fff]', s):
        out.append(s)
print('有效中文段:', len(out))

# 按首段去重打印
seen = set()
with open(r'<SOURCE_DIR>\_doubao_chat_extract.txt', 'w', encoding='utf-8') as f:
    for s in out:
        key = s[:40]
        if key not in seen:
            seen.add(key)
            f.write(s + '\n---\n')
            print(repr(s[:160]))
print('已写入 _doubao_chat_extract.txt, 去重后段数:', len(seen))
