# -*- coding: utf-8 -*-
"""
v5：在 v4(20260820) 版基础上：
  1) 新增低分 211 对照：青海大学、海南大学（22408+AI+B区）
  2) 更新：贵州大学/华北电力大学 补历年线，新疆大学 补2026口径
  3) 主体 S 再补 11 所历史线（折线图扩至 26 所）
  4) 窄屏优化：表格更紧凑、折线图更小、横滑更友好
  5) 美化：报录比/复录比/历年线列高亮、行 hover、折线图渐变
"""
import io, re

SRC = r"<SOURCE_DIR>\02_院校数据_原有\全国408_085410双非热度版_20260820.html"
OUTS = [
    SRC,
    r"<MATERIAL_DIR>\02_院校数据_原有\全国408_085410双非热度版_20260820.html",
]

s = io.open(SRC, encoding="utf-8").read()

def rep(old, new):
    global s
    n = s.count(old)
    if n == 0:
        raise SystemExit("未找到锚点: " + old[:70])
    s = s.replace(old, new)

def inject_lh(name, arr, count=0):
    global s
    pat = re.compile(r'(\{"n":"' + re.escape(name) + r'"[^}]*?),\s*"note":')
    m = pat.search(s)
    if not m:
        raise SystemExit("未找到学校行: " + name)
    lh = ",".join("null" if v is None else str(v) for v in arr)
    s = pat.sub(r'\1,"lh":[' + lh + r'],"note":', s, count=count)

# ---------- 1) S 主体补历史线（折线图扩充） ----------
S_LH = {
    "浙江理工大学": [None, None, 290],   # 2025=290（官方复试线），2026=335
    "天津理工大学": [None, 286, 260],    # 2024=286，2025=260（A区国家线），2026=315
    "成都理工大学": [None, 299, 301],    # 2024=299，2025=301，2026=308
    "湖南科技大学": [None, None, 273],   # 2025=273（A类线），2026=338
    "广州大学": [None, 280, 296],        # 2024=280（首年），2025=296，2026=300/310
    "兰州理工大学": [None, None, 250],   # 2025=250（B区国家线），2026=254
    "桂林电子科技大学": [None, None, 250], # 2025=250（B区），2026=254
    "成都信息工程大学": [None, None, 260], # 2025=260，2026=264
    "东北石油大学": [None, None, 260],   # 2025=260，2026=302（改408）
    "齐鲁工业大学": [None, None, 260],   # 2025=260，2026=264
    "华南农业大学": [273, 273, 260],     # 2023/24=273，2025=260，2026=294
    "重庆邮电大学": [None, 273, 260],    # 2024=273，2025=260，2026=336（非408）
}
for name, arr in S_LH.items():
    inject_lh(name, arr)

# ---------- 2) C 对照：更新已有行 ----------
rep('{"n":"贵州大学","p":"贵州","r":"西南","t":"211","c":"计算机科学与技术学院","d":"不区分研究方向","l":303,"plan":"40","fc":"一志愿为主","ratio":null,"rr":null,"ai":"✅真AI方向","src":"官方","net":70,"note":"官方复试线303，拟招40，408"}',
    '{"n":"贵州大学","p":"贵州","r":"西南","t":"211","c":"计算机科学与技术学院","d":"不区分研究方向","l":303,"plan":"40","fc":"一志愿为主","ratio":null,"rr":null,"ai":"✅真AI方向","src":"官方","net":70,"note":"B区211；2024=330/2025=308/2026=303（启航）；拟招40，408；AI方向明确","lh":[null,330,308]}')
rep('{"n":"华北电力大学","p":"北京","r":"华北","t":"211","c":"控制与计算机工程学院","d":"不区分研究方向","l":264,"plan":"—","fc":"一志愿为主","ratio":null,"rr":null,"ai":"❓未注明","src":"官方","net":60,"note":"官方复试方案：085410按A区国家线264"}',
    '{"n":"华北电力大学","p":"北京","r":"华北","t":"211","c":"控制与计算机工程学院","d":"不区分研究方向","l":264,"plan":"—","fc":"一志愿为主","ratio":null,"rr":null,"ai":"❓未注明","src":"官方","net":60,"note":"2024年三个方向均273（国家线）；2026按A区国家线264；AI方向在控制与计算机工程学院，偏控制","lh":[null,273,null]}')
rep('"note":"085400电子信息相关320/254；085410线待核"}',
    '"note":"2026电子信息[085400]（含人工智能方向）线254（B区国家线）；085410线待核"}')

# ---------- 3) C 新增低分 211 ----------
C_NEW = [
    '{"n":"青海大学","p":"青海","r":"西北","t":"211","c":"计算机技术与应用学院","d":"不区分研究方向","l":254,"plan":"25","fc":"一志愿为主(21/25)","ratio":null,"rr":null,"ai":"✅真AI方向","src":"官方+启航","net":48,"note":"B区211双一流；22408(英二数二408)；2023=263/2025=250/2026=254均按B区国家线未设院线；一志愿21/25调剂0；复试考程序设计","lh":[263,263,250]}',
    '{"n":"海南大学","p":"海南","r":"华南","t":"211","c":"信息与通信工程学院","d":"不区分研究方向","l":null,"plan":"—","fc":"一志愿为主","ratio":null,"rr":null,"ai":"✅真AI方向","src":"官方+启航","net":56,"note":"B区211双一流；2026起计算机相关专硕统一22408（启航2025-11）；2025信息与通信工程学院线250（B区国家线）；2026线待核","lh":[null,null,250]}',
]
rep('];\n// ===== 初试科目映射', ',\n' + ',\n'.join(C_NEW) + '\n];\n// ===== 初试科目映射')

rep('"上海大学":"22408"', '"上海大学":"22408","青海大学":"22408","海南大学":"22408"')

# ---------- 4) 窄屏优化 + 美化 CSS ----------
rep('''  .table-wrap{max-height:520px;-webkit-overflow-scrolling:touch;overscroll-behavior:contain;touch-action:pan-x pan-y}
  table{font-size:12px;min-width:1120px}
  th{padding:7px 5px;font-size:11px}
  td{padding:6px 5px;font-size:12px}''',
    '''  .table-wrap{max-height:520px;-webkit-overflow-scrolling:touch;overscroll-behavior:contain;touch-action:pan-x pan-y}
  table{font-size:11px;min-width:900px}
  th{padding:5px 4px;font-size:10px}
  td{padding:4px 3px;font-size:11px}''')
rep('table{font-size:11px;min-width:980px}', 'table{font-size:10.5px;min-width:860px}')
rep('.line-chart svg{display:block;width:100%;min-width:560px;height:auto}',
    '.line-chart svg{display:block;width:100%;min-width:430px;height:auto}')

BEAUTY = '''
.num-hl{background:#f0fdf4!important;font-weight:700;color:#15803d}
.num-warn{background:#fef2f2!important;font-weight:700;color:#b91c1c}
td.lh-col{background:#f8fafc;color:#334155}
#ov-tb tr:hover td,#ratio-tb tr:hover td,#heat-tb tr:hover td,#heat-e-tb tr:hover td,#heat-w-tb tr:hover td,#adjust-tb tr:hover td,#other-tb tr:hover td{background:#eef7f4!important}
.chart-figure figcaption{letter-spacing:.5px}
'''
rep('.lc-legend i{display:inline-block;width:22px;height:3px;border-radius:2px;margin-right:5px;vertical-align:middle}', '.lc-legend i{display:inline-block;width:22px;height:3px;border-radius:2px;margin-right:5px;vertical-align:middle}' + BEAUTY)

# ---------- 5) 总览表单元格美化 ----------
rep('''    '<td class="num">'+numOrNa(d.ratio==null?null:d.ratio)+"</td>"+
    '<td class="num">'+numOrNa(d.rr==null?null:d.rr)+"</td>"+''',
    '''    '<td class="num '+(d.ratio!=null?"num-hl":"")+'">'+numOrNa(d.ratio==null?null:d.ratio)+"</td>"+
    '<td class="num '+(d.rr!=null?"num-warn":"")+'">'+numOrNa(d.rr==null?null:d.rr)+"</td>"+''')
rep('    "<td>"+lhCell(d)+"</td>"+', '    \'<td class="lh-col">\'+lhCell(d)+"</td>"+')

# ---------- 6) 折线图渐变美化 ----------
rep('''  var html='<svg viewBox="0 0 '+W+' '+H+'" preserveAspectRatio="xMidYMid meet">';''',
    '''  var html='<svg viewBox="0 0 '+W+' '+H+'" preserveAspectRatio="xMidYMid meet"><defs><linearGradient id="lcg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0f766e" stop-opacity=".28"/><stop offset="1" stop-color="#0f766e" stop-opacity=".03"/></linearGradient></defs>';''')
rep('''  if(pts.length>=2){
    var pth=pts.map(function(t,j){return (j?"L":"M")+t;}).join(" ");
    html+='<path d="'+pth+'" fill="none" stroke="#0f766e" stroke-width="2.6" stroke-linejoin="round"/>';
  }''',
    '''  if(pts.length>=2){
    var pth=pts.map(function(t,j){return (j?"L":"M")+t;}).join(" ");
    var fx=parseFloat(pts[0].split(" ")[0]),lx=parseFloat(pts[pts.length-1].split(" ")[0]);
    html+='<path d="'+pth+' L'+lx+' '+(H-PB)+' L'+fx+' '+(H-PB)+' Z" fill="url(#lcg)"/>';
    html+='<path d="'+pth+'" fill="none" stroke="#0f766e" stroke-width="2.6" stroke-linejoin="round"/>';
  }''')

# ---------- 7) SRCS 补来源 + footer 说明 ----------
rep('["历年线·黑眼圈院校库（河北大学/苏大/华北理工）","https://www.heiyanquan.fun/"],',
    '["历年线·黑眼圈院校库（河北大学/苏大/华北理工）","https://www.heiyanquan.fun/"],\n'
    '["青海大学085410考情（B区211低分）","https://m-jixun.iqihang.com/zixun/fenshuxian/2026714871.html#1"],\n'
    '["海南大学计算机考情（2026专硕22408）","https://jixun.iqihang.com/zixun/changshi/2025701402.html"],\n'
    '["贵州大学历年线（2024/25/26）","https://m-jixun.iqihang.com/zixun/changshi/2025701407.html"],\n'
    '["浙江理工大学2025复试线（官方）","https://gradadmission.zstu.edu.cn/info/1011/3206.htm#1"],\n'
    '["天津理工/成都理工/广州大学/华南农大历年线","https://m.dxsbb.com/news/45394.html"],\n'
    '["重邮历年线（路灯考研）","https://www.ludengkaoyan.com/school322/qrz/zsml/28349.html"],')

rep('数据截止 2026-08-20（本轮新增天津工业/吉首大学，211/双一流对照新增华中师范/中国矿业/郑大/上大/苏大/暨南/福大/西南大学/河南大学，并修正重庆科技/湖南科技/江苏海洋/安庆师范/新疆农大初试科目；报录比/复录比均来自官方公示或机构交叉核实，未编造），报考请以官方 2027 招生简章为准。',
    '数据截止 2026-08-20（8-21 再更新：新增青海大学/海南大学低分211对照，主体与对照累计 26 所可画历年线，窄屏阅读优化，报录比/复录比均来自官方公示或机构交叉核实，未编造），报考请以官方 2027 招生简章为准。')

for out in OUTS:
    with io.open(out, "w", encoding="utf-8") as f:
        f.write(s)
    print("已写入:", out, len(s))
print("S_lh:", len(S_LH), "| C新增:", len(C_NEW))
