# -*- coding: utf-8 -*-
"""尝试解析 trae 分享页，找聊天内容 API"""
import urllib.request, re, json

url = 'https://share.traecontent.cn/share/E-9457Z4G26D62'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
data = urllib.request.urlopen(req, timeout=15).read().decode('utf-8', 'ignore')

# 查找可能的 API 端点模式
patterns = [
    (r'["\'](/[a-zA-Z0-9_\-/]*(?:share|conversation|chat|message|session)[a-zA-Z0-9_\-/]*)["\']', 'API路径'),
    (r'window\.__[A-Z_]+__\s*=\s*(\{.*?\});', '全局状态'),
]
for pat, name in patterns:
    ms = re.findall(pat, data)
    print(f'[{name}] 命中 {len(ms)} 个')
    for m in ms[:10]:
        print('  ', m if isinstance(m, str) else str(m)[:120])

# 尝试常见 API
for ep in [
    'https://share.traecontent.cn/api/share/E-9457Z4G26D62',
    'https://share.traecontent.cn/api/v1/share/E-9457Z4G26D62',
    'https://work.trae.cn/api/share/E-9457Z4G26D62',
]:
    try:
        r2 = urllib.request.urlopen(urllib.request.Request(ep, headers={'User-Agent': 'Mozilla/5.0'}), timeout=10)
        body = r2.read().decode('utf-8', 'ignore')
        print(f'\n[API {ep}] HTTP {r2.status} len {len(body)}')
        print(body[:800])
    except Exception as e:
        print(f'\n[API {ep}] ERR {e}')
