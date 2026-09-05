# -*- coding: utf-8 -*-
"""豆包聊天记忆提取 v2：UTF-16LE 解码 + 噪音过滤 + 写 UTF-8 文件"""
import os, re

base = os.path.expandvars(r'%LOCALAPPDATA%\Doubao\User Data\Default\IndexedDB\chrome_doubao-chat_0.indexeddb.leveldb')
data = b''
for fn in ['000137.log', '000139.ldb']:
    p = os.path.join(base, fn)
    if os.path.exists(p):
        data += open(p, 'rb').read()

t = data.decode('utf-16-le', errors='ignore')

# 清理：替换掉明显是二进制噪音的字符
# 保留：CJK、全角标点、ASCII 可打印、常见换行/空格
clean_chars = []
for ch in t:
    o = ord(ch)
    if ch == '\n' or ch == '\r' or ch == '\t':
        clean_chars.append(ch)
    elif 0x4E00 <= o <= 0x9FFF or 0x3000 <= o <= 0x303F or 0xFF00 <= o <= 0xFFEF:
        clean_chars.append(ch)
    elif 0x20 <= o <= 0x7E:
        clean_chars.append(ch)
    else:
        clean_chars.append(' ')  # 噪音变空格
clean = ''.join(clean_chars)

# 压缩多余空白
clean = re.sub(r'[ \t]+', ' ', clean)
clean = re.sub(r'\n{3,}', '\n\n', clean)

# 拆行：每行至少 8 个字符且含中文才算有效文本
lines = []
for line in clean.split('\n'):
    line = line.strip()
    if len(line) >= 8 and re.search(r'[\u4e00-\u9fff]{2,}', line):
        lines.append(line)

print('有效行数:', len(lines))
out_path = r'<SOURCE_DIR>\_doubao_chat_extract.txt'
with open(out_path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))
print('已写入:', out_path)
# 打印前 40 行预览
for l in lines[:40]:
    print(l[:160])
