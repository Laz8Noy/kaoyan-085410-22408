# -*- coding: utf-8 -*-
"""
终极版生成：以 全国408_085410双非热度版_20260820.html 为基底
1) 复制模板全部样式/数据/交互
2) 注入「2027改考动态」+「导师研究方向」两个新区块（插在考情明细前）
3) 更新标题日期为 2026-08-24 终极版
输出：全国408_085410双非热度版_终极版_20260824.html
"""
import io, re, json

BASE = r'<SOURCE_DIR>\02_院校数据_原有\全国408_085410双非热度版_20260820.html'
OUT = r'<SOURCE_DIR>\02_院校数据_原有\全国408_085410双非热度版_终极版_20260824.html'
MAIN_MD = r'<SOURCE_DIR>\01_择校与规划\085410_22408_择校与规划_20260820.md'

html = io.open(BASE, encoding='utf-8').read()

# ---------- 1. 提取改考动态 38 条 ----------
md = io.open(MAIN_MD, encoding='utf-8').read()
lines = md.split('\n')
gk_rows = []
in_gk = False
for l in lines:
    if l.startswith('##') and '2027改考动态' in l:
        in_gk = True
        continue
    if in_gk:
        if l.startswith('##'):
            break
        if l.startswith('|') and not l.startswith('|---'):
            cells = [c.strip() for c in l.strip('|').split('|')]
            if cells and cells[0] not in ('院校', ''):
                gk_rows.append(cells)

# ---------- 2. 提取导师 ----------
ds_rows = []
in_ds = False
for l in lines:
    if l.startswith('##') and '导师研究方向' in l:
        in_ds = True
        continue
    if in_ds:
        if l.startswith('##'):
            break
        m = re.match(r'- \*\*(.+?)\*\*：(.+)', l)
        if m:
            ds_rows.append((m.group(1), m.group(2)))

# ---------- 3. 生成新区块 HTML ----------
gk_html_rows = ""
for r in gk_rows:
    name, tier, scope, old, new, yr, src, note = (r + [''] * 8)[:8]
    cls = 'warn' if ('⚠️' in note or '勿' in note or '非408' in note) else ''
    gk_html_rows += f'<tr class="{cls}"><td>{name}</td><td>{tier}</td><td>{scope}</td><td>{old}</td><td>{new}</td><td>{yr}</td><td>{src}</td><td>{note}</td></tr>\n'

ds_html = ""
for name, info in ds_rows:
    ds_html += f'<div class="detail-card"><h4>{name}</h4><div class="meta">{info}</div></div>\n'

new_block = f'''
<section id="gaikao" class="card-stack">
  <div class="card">
    <h3>📢 2027 改考动态（38条）<span class="hint">新增/改考408 · 反向改考避坑 · 以官方公告为准</span></h3>
    <div class="cardsub">汇总自 2026-08-24 各校研究生院/研招网/新东方/启航公告。⚠️ 红行=与 22408 相关或需避坑（非408/反向改考/公共课不符）。9月简章发布后须逐条复核。</div>
    <div class="table-wrap" style="max-height:480px">
      <table style="min-width:1200px">
        <thead><tr><th>院校</th><th>层次</th><th>专业/范围</th><th>原科目</th><th>新科目</th><th>生效</th><th>来源</th><th>备注</th></tr></thead>
        <tbody>{gk_html_rows}</tbody>
      </table>
    </div>
  </div>
</section>

<section id="mentors" class="card-stack">
  <div class="card">
    <h3>🧑‍🏫 导师研究方向（49位 · 16所）<span class="hint">优先标注 Agent / 大模型 / 具身智能 / 多模态 相关课题</span></h3>
    <div class="cardsub">摘自各校教师主页/学院招生目录（2026-08 核实）。报考前建议邮件联系导师确认 2027 招生名额与课题。</div>
    <div class="detail-grid">{ds_html}</div>
  </div>
</section>
'''

# ---------- 4. 插入位置：考情明细 <section id="kq"> 之前 ----------
anchor = '<section id="kq">'
idx = html.find(anchor)
if idx < 0:
    raise SystemExit('未找到 kq 锚点')
html = html[:idx] + new_block + '\n' + html[idx:]

# ---------- 5. 更新标题/日期 ----------
html = html.replace('全国408·085410人工智能专硕双非热度版（2026-2027）',
                    '全国408·085410人工智能专硕·终极版（2026-08-24汇总）')
html = html.replace('<title>全国408·085410人工智能专硕双非热度版（2026-2027）</title>',
                    '<title>全国408·085410人工智能专硕·终极版（2026-2027）</title>')
html = html.replace('<h1>全国 408「085410 人工智能专硕」双非热度版</h1>',
                    '<h1>全国 408「085410 人工智能专硕」终极版</h1>')

io.open(OUT, 'w', encoding='utf-8').write(html)
print('输出:', OUT, '大小:', len(html))
print('改考区块注入:', 'id="gaikao"' in html, '| 导师区块:', 'id="mentors"' in html)
print('改考条数:', len(gk_rows), '| 导师院校:', len(ds_rows))
