# -*- coding: utf-8 -*-
"""从主表 md 提取：2027改考动态38条 + 导师49位"""
import io, re

M = r'<SOURCE_DIR>\01_择校与规划\085410_22408_择校与规划_20260820.md'
md = io.open(M, encoding='utf-8').read()
lines = md.split('\n')

# 提取改考动态表格（第四节）
print('=== 2027改考动态（表格行）===')
in_gk = False
gk_rows = []
for l in lines:
    if '2027改考动态' in l and l.startswith('##'):
        in_gk = True
        continue
    if in_gk:
        if l.startswith('##'):
            break
        if l.startswith('|') and not l.startswith('|---'):
            cells = [c.strip() for c in l.strip('|').split('|')]
            if cells and cells[0] not in ('院校', ''):
                gk_rows.append(cells)
print(f'共 {len(gk_rows)} 条')
for r in gk_rows[:8]:
    print(' ', r)

# 提取导师（第五节）
print('\n=== 导师研究方向 ===')
in_ds = False
ds_rows = []
for l in lines:
    if '导师研究方向' in l and l.startswith('##'):
        in_ds = True
        continue
    if in_ds:
        if l.startswith('##'):
            break
        if l.startswith('- **'):
            m = re.match(r'- \*\*(.+?)\*\*：(.+)', l)
            if m:
                ds_rows.append((m.group(1), m.group(2)))
print(f'共 {len(ds_rows)} 所院校的导师')
for r in ds_rows:
    print(' ', r[0], '->', r[1][:60])
