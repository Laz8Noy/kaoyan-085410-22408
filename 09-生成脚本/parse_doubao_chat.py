# -*- coding: utf-8 -*-
"""解析豆包 IndexedDB LevelDB 日志，尝试解压提取聊天内容"""
import os, re, sys, zlib, struct
sys.path.insert(0, r'<SOURCE_DIR>\_pylibs')
import cramjam

base = os.path.expandvars(r'%LOCALAPPDATA%\Doubao\User Data\Default\IndexedDB\chrome_doubao-chat_0.indexeddb.leveldb')
out_lines = []

def parse_log(path, tag):
    """LevelDB .log 文件：32KB 块，记录 = [crc32c 4B][len 2B][type 1B] + data"""
    data = open(path, 'rb').read()
    pos = 0
    block = 0
    total = 0
    while pos + 7 <= len(data):
        # 每 32768 字节一个块
        block_start = (pos // 32768) * 32768
        if pos - block_start + 7 > 32768:
            pos = block_start + 32768
            continue
        crc, ln, typ = data[pos], int.from_bytes(data[pos+4:pos+6], 'little'), data[pos+6]
        if ln == 0 or ln > 32768:
            pos += 7
            continue
        payload = data[pos+7:pos+7+ln]
        pos += 7 + ln
        total += 1
        if len(payload) < 4:
            continue
        # 尝试 snappy 解压
        for comp in (False, True):
            try:
                if comp:
                    raw = bytes(cramjam.snappy.decompress_raw(payload))
                else:
                    raw = payload
                # 找中文
                for m in re.finditer(rb'[\xe4-\xe9][\x80-\xbf][\x80-\xbf]', raw):
                    pass
                zh = re.findall(r'[\u4e00-\u9fff]{2,}', raw.decode('utf-8', 'ignore'))
                if zh and len(''.join(zh)) >= 6:
                    out_lines.append(f"[{tag} rec#{total} comp={comp}] " + ' '.join(zh))
                    break
            except Exception:
                continue

for fn in ['000137.log', '000139.ldb']:
    p = os.path.join(base, fn)
    if os.path.exists(p):
        parse_log(p, fn)

print("解压提取到含中文记录:", len(out_lines))
for l in out_lines[:80]:
    print(l[:300])
