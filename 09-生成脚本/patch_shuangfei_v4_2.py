# -*- coding: utf-8 -*-
"""v4.2 小修正：footer 27 所 + header/banner 日期统一 2026-08-21"""
import io

SRC = r"<SOURCE_DIR>\02_院校数据_原有\全国408_085410双非热度版_20260820.html"
OUTS = [
    SRC,
    r"<MATERIAL_DIR>\02_院校数据_原有\全国408_085410双非热度版_20260820.html",
]

s = io.open(SRC, encoding="utf-8").read()

def rep(old, new, expect=1):
    global s
    n = s.count(old)
    if n != expect:
        raise SystemExit("锚点数量不符 (%d/%d): %s" % (n, expect, old[:60]))
    s = s.replace(old, new)

rep('主体与对照累计 26 所可画历年线', '主体与对照累计 27 所可画历年线')
rep('<div class="stat"><b>2026-08-20</b><span>数据截止</span></div>',
    '<div class="stat"><b>2026-08-21</b><span>数据截止</span></div>')
rep('截至 2026-08-20，研招网 2027 硕士专业目录尚未发布', '截至 2026-08-21，研招网 2027 硕士专业目录尚未发布')

for out in OUTS:
    with io.open(out, "w", encoding="utf-8") as f:
        f.write(s)
    print("已写入:", out, len(s))
