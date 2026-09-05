# -*- coding: utf-8 -*-
"""校验数据库 JSON 并出统计报告。"""
import json, os, glob, sys

SCH = r"<SOURCE_DIR>\deliverables\20260903-考研院校数据库AI版\data\schools"
rep = open(sys.argv[1] if len(sys.argv) > 1 else "db_report.txt", "w", encoding="utf-8")

def pr(*a):
    print(*a, file=rep)

pr("=== 数据库校验报告 2026-09-03 ===")
files = sorted(glob.glob(os.path.join(SCH, "*.json")))
pr("文件数:", len(files))
names = {}
errors = []
units_total = 0
conf_total = 0
nn_only = 0
for fp in files:
    try:
        with open(fp, "r", encoding="utf-8") as f:
            o = json.load(f)
    except Exception as e:
        errors.append((fp, f"JSON解析失败 {e}"))
        continue
    nm = o.get("name")
    if nm in names:
        errors.append((fp, f"重名 {nm} 与 {names[nm]}"))
    else:
        names[nm] = os.path.basename(fp)
    if not nm or "schema" not in o:
        errors.append((fp, "缺 name/schema"))
    u = o.get("units", [])
    units_total += len(u)
    conf_total += len(o.get("conflicts", []))
    if not u:
        nn_only += 1

pr("唯一校名数:", len(names), "| 总 units:", units_total, "| 冲突条数:", conf_total, "| 无主体行(仅候补/链接):", nn_only)
pr("错误数:", len(errors))
for e in errors[:40]:
    pr("  !", e)
pr("\n=== 样例：成都信息工程大学 ===")
for fp in files:
    with open(fp, "r", encoding="utf-8") as f:
        o = json.load(f)
    if o.get("name") == "成都信息工程大学":
        pr("file:", os.path.basename(fp))
        for un in o["units"]:
            pr(f"unit: 学院={un.get('college')} 科目分类={un.get('subjectClass')} 2026线={un.get('line2026')} 计划={un.get('plan2026')} "
               f"复试={un.get('retestCnt')} 录取={un.get('admitCnt')} 分={un.get('admitMin')}~{un.get('admitMax')}/均{un.get('admitAvg')} "
               f"AI={un.get('aiTag')} 标注={un.get('note')}")
            if un.get("subjectClaim2026"):
                pr("   科目claim:", un["subjectClaim2026"], "状态:", un.get("subjectStatus"))
        pr("conflicts:", json.dumps(o.get("conflicts"), ensure_ascii=False)[:1200])
        pr("deepRef:", o.get("deepRef"))
        pr("wdLinks:", len(o.get("wangdaoLinks", {})))
        pr("kqDetail条数:", len(o.get("kaoqingDetail2026", [])))
rep.close()
print("report written")
