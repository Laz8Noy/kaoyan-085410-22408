# -*- coding: utf-8 -*-
"""导出模板 S/C 数组的完整 JSON（含考情字段），供合并参考"""
import io, re, json

p = r'<SOURCE_DIR>\02_院校数据_原有\全国408_085410双非热度版_20260820.html'
html = io.open(p, encoding='utf-8').read()
scripts = re.findall(r'<script>(.*?)</script>', html, re.S)
s = scripts[0]

def grab(name):
    m = re.search(r'var ' + name + r'=\[(.*?)\];', s, re.S)
    if not m:
        return None
    txt = m.group(1)
    # 逐对象解析
    objs = []
    for o in re.finditer(r'\{[^{}]*\}', txt):
        try:
            objs.append(json.loads(o.group(0)))
        except Exception as e:
            objs.append({'RAW': o.group(0)[:200]})
    return objs

for name in ['S', 'C']:
    objs = grab(name)
    print(f'=== {name}: {len(objs)} 条 ===')
    # 输出字段集合
    keys = set()
    for o in objs:
        keys.update(o.keys())
    print('字段:', sorted(keys))
    # 有考情字段的条目
    kq = [o for o in objs if o.get('rec') is not None or o.get('adm') is not None or o.get('max_s') is not None or o.get('lh')]
    print(f'含考情字段(lh/rec/adm)条目: {len(kq)}')
    for o in kq:
        print('  ', o.get('n'), '| lh:', o.get('lh'), '| rec:', o.get('rec'), '| adm:', o.get('adm'), '| max/min/avg:', o.get('max_s'), o.get('min_s'), o.get('avg_s'), '| scope:', (o.get('scope') or '')[:40])
