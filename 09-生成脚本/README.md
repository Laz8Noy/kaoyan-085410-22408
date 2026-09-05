# 09 生成脚本

这里是当初从 Excel / 网页模板生成择校表的脚本，**日常备考可以不管**。

若你要改数据再出一版 HTML/XLSX：

- 规划文档相关：`build_plan_v2.py`
- 终极版 / 双非热度：`build_final.py`、`build_final_html.py`、`integrate_three_sources.py` 等

大量 `debug_*` / `dump_*` / `try_*` 是排查脚本，公开仅为了复现整理过程，不是稳定 CLI。运行前请读脚本头部，不要把 API Key 写进仓库。
