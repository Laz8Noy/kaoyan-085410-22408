# -*- coding: utf-8 -*-
"""交叉校验：trae记录关键数据 vs 终极版HTML数据"""
import io, json, re

HTML = r'<SOURCE_DIR>\02_院校数据_原有\全国408_085410双非热度版_终极版_20260824.html'
h = io.open(HTML, encoding='utf-8').read()
s = re.findall(r'<script>(.*?)</script>', h, re.S)[0]

def grab(name):
    m = re.search(r'var ' + name + r'=\[(.*?)\];', s, re.S)
    objs = []
    for o in re.finditer(r'\{[^{}]*\}', m.group(1)):
        try:
            objs.append(json.loads(o.group(0)))
        except: pass
    return objs

S = grab('S'); C = grab('C')
all_schools = {}
for d in S + C:
    all_schools.setdefault(d['n'], []).append(d)

# trae 记录中的关键数据点（从对话提取）
trae_checks = {
    '郑州大学': {'录取人数': '2024:68/2025:96', '均分': '2024:349/2025:357', '最低': 337},
    '南京信息工程大学': {'最低': 345, '最高': 421, '录取': '2025近160人', '科目': '22408确认'},
    '华中师范大学': {'统招': '约20人(两院系各10人)', '科目': '22408确认'},
    '广州大学': {'最低': 295, '最高': 385},
    '江苏大学': {'最低': 273, '最高': 333, '报录比': '官方公布'},
    '广西大学': {'最低': 277, '复试线2025': 277, '科目': '22408确认'},
    '云南大学': {'最低': 281, '科目': '22408(待确认)'},
    '福州大学': {'均分': '2024:328/2025:354', '人数': 51},
    '河南大学': {'最低': 338},
    '暨南大学': {'均分2025': 354, '人数2025': 42},
    '江南大学': {'均分2025': 373, '人数2025': 56},
    '苏州大学': {'均分2025': '369/364', '人数2025': '14+22'},
}

print('=== 交叉校验（trae vs 终极版）===')
for name, trae in trae_checks.items():
    hits = all_schools.get(name, [])
    if not hits:
        print(f'❌ [{name}] 终极版中未找到')
        continue
    for d in hits:
        print(f'\n[{name}] 学院:{d["c"]} | 2026线:{d["l"]} | plan:{d["plan"]} | 考情: rec={d.get("rec")} adm={d.get("adm")} min={d.get("min_s")} max={d.get("max_s")} avg={d.get("avg_s")}')
        print(f'   trae补充: {trae}')
