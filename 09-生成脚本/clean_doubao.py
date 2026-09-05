# -*- coding: utf-8 -*-
"""豆包记忆最终清理：过滤噪音行，按主题整理"""
import os, re, collections

src = r'<SOURCE_DIR>\_doubao_chat_extract.txt'
lines = open(src, encoding='utf-8').read().split('\n')

def noise_ratio(s):
    """统计行中'正常字符'比例：CJK + 全角 + ascii 可打印 + 空白"""
    good = 0
    for ch in s:
        o = ord(ch)
        if 0x4E00 <= o <= 0x9FFF or 0x3000 <= o <= 0x303F or 0xFF00 <= o <= 0xFFEF or 0x20 <= o <= 0x7E or ch in '\n\r\t':
            good += 1
    return good / max(1, len(s))

clean = []
for l in lines:
    l = l.strip()
    if not l:
        continue
    if noise_ratio(l) < 0.92:
        continue  # 噪音行（UTF-16反向解读的乱码）
    # 去掉行内残留的扩展 ASCII
    l2 = re.sub(r'[\x80-\u2FFF]', '', l)
    l2 = re.sub(r'[ \t]{2,}', ' ', l2)
    if len(l2) >= 6 and re.search(r'[\u4e00-\u9fff]{2,}', l2):
        clean.append(l2)

# 去重（保留顺序）
seen = set()
uniq = []
for l in clean:
    k = l[:60]
    if k not in seen:
        seen.add(k)
        uniq.append(l)

print('清理后有效行:', len(uniq))
out = r'<SOURCE_DIR>\_doubao_memories_clean.txt'
with open(out, 'w', encoding='utf-8') as f:
    f.write('\n'.join(uniq))
print('已写入:', out)

# 主题统计（关键词频次）
topics = {
    'ChatGPT/GPT': 0, 'API中转/Key': 0, 'DeepSeek': 0, 'Codex': 0, 'Cursor': 0,
    '考研/408': 0, '院校/085410': 0, '编程/代码': 0, '免费额度': 0, '精灵/绘图': 0,
}
for l in uniq:
    if re.search(r'ChatGPT|GPT-4|GPT-5|OpenAI', l): topics['ChatGPT/GPT'] += 1
    if re.search(r'中转|API|Key|sk-|token', l): topics['API中转/Key'] += 1
    if 'DeepSeek' in l: topics['DeepSeek'] += 1
    if 'Codex' in l: topics['Codex'] += 1
    if 'Cursor' in l: topics['Cursor'] += 1
    if re.search(r'考研|408|数学|英语|政治|数据结构|王道', l): topics['考研/408'] += 1
    if re.search(r'085410|院校|复试|调剂|人工智能专业', l): topics['院校/085410'] += 1
    if re.search(r'代码|编程|函数|脚本|报错|error|调试', l): topics['编程/代码'] += 1
    if re.search(r'免费|额度|试用|白嫖', l): topics['免费额度'] += 1
    if '精灵' in l or '绘图' in l: topics['精灵/绘图'] += 1
print('\n=== 主题分布 ===')
for k, v in sorted(topics.items(), key=lambda x: -x[1]):
    print(f'{k}: {v} 行')
