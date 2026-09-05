# -*- coding: utf-8 -*-
"""读取示例：查某校（默认成信工）主体行 + 冲突。"""
import json, glob, sys

SCH = r"..\data\schools"
kw = sys.argv[1] if len(sys.argv) > 1 else "成都信息工程大学"
for fp in glob.glob(SCH + r"\*.json"):
    with open(fp, "r", encoding="utf-8") as f:
        o = json.load(f)
    if kw in o["name"]:
        print("== 校名:", o["name"], "==")
        for u in o.get("units", []):
            print("-", u.get("college"), "| 科目分类:", u.get("subjectClass"),
                  "| 2026线:", u.get("line2026"), "| 计划:", u.get("plan2026"),
                  "| 复试/录取:", u.get("retestCnt"), "/", u.get("admitCnt"),
                  "| NN408均分:", u.get("nn408avg"), "| 录取率:", u.get("nnRate"))
        print("== conflicts ==")
        for c in o.get("conflicts", []):
            print(" *", c.get("field"), "|", c.get("status"), "|", c.get("action"))
