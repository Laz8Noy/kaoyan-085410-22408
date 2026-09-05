# -*- coding: utf-8 -*-
"""轻量 Markdown -> HTML 转换器（针对豆包 408 资料的语法）"""
import re


def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def inline(s):
    """行内元素：去转义、粗体、行内代码。"""
    s = s.replace("\\", "")
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    return s


def table_to_html(lines):
    rows = []
    for ln in lines:
        cells = [c.strip() for c in ln.strip().strip("|").split("|")]
        rows.append(cells)
    if len(rows) < 2:
        return "<p>" + "<br>".join(inline(l) for l in lines) + "</p>"
    header = rows[0]
    # 第二行是分隔行 |---|---|
    body = rows[2:] if len(rows) >= 2 and all(re.fullmatch(r":?-{2,}:?", c) for c in rows[1]) else rows[1:]
    html = '<div class="table-scroll"><table><thead><tr>'
    html += "".join(f"<th>{inline(c)}</th>" for c in header)
    html += "</tr></thead><tbody>"
    for r in body:
        html += "<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>"
    html += "</tbody></table></div>"
    return html


def md_to_html(text):
    lines = text.split("\n")
    out = []
    i = 0
    in_code = False
    code_buf = []
    in_table = False
    table_buf = []
    n = len(lines)

    def flush_table():
        nonlocal in_table, table_buf
        if in_table:
            out.append(table_to_html(table_buf))
            table_buf = []
            in_table = False

    while i < n:
        line = lines[i].rstrip()
        if line.strip().startswith("```"):
            if in_code:
                out.append(f"<pre><code>{esc(chr(10).join(code_buf))}</code></pre>")
                code_buf = []
                in_code = False
            else:
                in_code = True
            i += 1
            continue
        if in_code:
            code_buf.append(line)
            i += 1
            continue

        if line.strip().startswith("|"):
            if not in_table:
                in_table = True
                table_buf = []
            table_buf.append(line)
            i += 1
            continue
        else:
            flush_table()

        m = re.match(r"^(#{1,6})\s+(.*)", line)
        if m:
            level = len(m.group(1))
            out.append(f"<h{level}>{inline(m.group(2))}</h{level}>")
            i += 1
            continue

        if line.strip() in ("---", "***", "___"):
            out.append("<hr>")
            i += 1
            continue

        if line.strip().startswith(">"):
            buf = []
            while i < n and lines[i].strip().startswith(">"):
                buf.append(lines[i].strip().lstrip(">").strip())
                i += 1
            out.append("<blockquote>" + "<br>".join(inline(b) for b in buf if b) + "</blockquote>")
            continue

        if re.match(r"^\s*[-*+]\s+", line):
            buf = []
            while i < n and re.match(r"^\s*[-*+]\s+", lines[i]):
                buf.append(re.sub(r"^\s*[-*+]\s+", "", lines[i]).strip())
                i += 1
            out.append("<ul>" + "".join(f"<li>{inline(b)}</li>" for b in buf) + "</ul>")
            continue

        if re.match(r"^\s*\d+[.)]\s+", line):
            buf = []
            while i < n and re.match(r"^\s*\d+[.)]\s+", lines[i]):
                buf.append(re.sub(r"^\s*\d+[.)]\s+", "", lines[i]).strip())
                i += 1
            out.append("<ol>" + "".join(f"<li>{inline(b)}</li>" for b in buf) + "</ol>")
            continue

        if not line.strip():
            i += 1
            continue

        buf = []
        while i < n and lines[i].strip() and not lines[i].strip().startswith(("|", "#", ">", "- ", "* ", "```", "---")) and not re.match(r"^\s*\d+[.)]\s+", lines[i]):
            buf.append(lines[i].strip())
            i += 1
        out.append("<p>" + "<br>".join(inline(b) for b in buf) + "</p>")

    flush_table()
    return "\n".join(out)


if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding="utf-8")
    path = r"<DOWNLOADS_DIR>\408考研全套资料·院校大全+复习指南+核心笔记.md"
    with open(path, encoding="utf-8") as f:
        content = f.read()
    html = md_to_html(content)
    # 只打印前 40 行验证
    print("\n".join(html.split("\n")[:40]))
