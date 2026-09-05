# -*- coding: utf-8 -*-
"""2026 考情精细数据整合：考情明细区块 + SRCS + CSS + 章节重编号（第 3 步）"""
import io, json, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

HTML = r"<SOURCE_DIR>\02_院校数据_原有\全国408_085410双非热度版_20260820.html"
s = io.open(HTML, encoding="utf-8").read()

# ---------- 考情明细区块 HTML ----------
KQ_SECTION = (
'<section id="kq">\n'
'  <h2>五、2026 复试 / 录取考情明细（目标院校）<span class="hint">复试人数 · 录取人数 · 初试最高/最低/平均 · 口径与来源</span></h2>\n'
'  <div class="banner tip" style="margin:10px 0">\n'
'    <b>读法：</b>「复试人数/录取人数」以各校 2026 年官方复试结果、拟录取名单公示为准；「录取初试最高/最低/平均」取自拟录取名单中的初试成绩（一志愿/含调剂口径见卡片「口径」）。机构数据一律标🔍，官方公示标✅，查不到的标「查无」，绝不编造。报录比因报考人数官方普遍不公布，多数院校查无公开数据。\n'
'  </div>\n'
'  <div class="filters">\n'
'    <div class="grp" id="kq-tier">\n'
'      <button class="active" data-v="全部">全部</button>\n'
'      <button data-v="川渝">川渝</button>\n'
'      <button data-v="外地">外地</button>\n'
'    </div>\n'
'    <input type="search" id="kq-kw" placeholder="搜学校 / 学院">\n'
'  </div>\n'
'  <div id="kq-box" class="kq-box"></div>\n'
'</section>\n'
)

anchor = '</section>\n\n<section id="recommender">'
assert anchor in s, "recommender anchor"
s = s.replace(anchor, '</section>\n' + KQ_SECTION + '\n<section id="recommender">', 1)

# ---------- 考情明细 JS ----------
KQ_JS = (
"\n// ===== 2026 考情明细 =====\n"
"function kqOrder(){return [\"成都信息工程大学\",\"成都理工大学\",\"重庆科技大学\",\"西南交通大学\",\"西南大学\",\"四川大学\",\"重庆大学\",\"重庆邮电大学\",\"四川师范大学\",\"西南民族大学\",\"中国民用航空飞行学院\",\"青海大学\",\"海南大学\",\"宁夏大学\",\"贵州大学\",\"新疆大学\",\"广西大学\",\"华北电力大学\",\"陕西师范大学\",\"华中师范大学\",\"河南大学\",\"福州大学\",\"天津工业大学\",\"大连理工大学\",\"上海大学\",\"天津理工大学\"];}\n"
"function kqList(){\n"
"  var order=kqOrder();\n"
"  var arr=S.concat(C).filter(function(d){return d.scope||d.rec!=null||d.adm!=null||d.max_s!=null||d.min_s!=null||d.avg_s!=null;});\n"
"  arr.sort(function(a,b){var ia=order.indexOf(a.n),ib=order.indexOf(b.n);if(ia<0)ia=99;if(ib<0)ib=99;return ia-ib;});\n"
"  return arr;\n"
"}\n"
"var kqState={tier:\"全部\",kw:\"\"};\n"
"function kqCard(d){\n"
"  var f=function(v){return v==null?'<span class=\"na\">—</span>':v;};\n"
"  var kq='<div class=\"kq-card\"><div class=\"kq-head\"><b>'+esc(d.n)+'</b><span class=\"kq-col\">'+esc(d.c)+'</span><span class=\"kq-tag '+((d.verified||'').indexOf('✅')>=0?'ok':'warn')+'\">'+esc(d.verified||'查无')+'</span></div>';\n"
"  kq+='<div class=\"kq-grid\">';\n"
"  kq+='<div class=\"kq-item\"><label>2026复试线</label><b>'+f(d.l)+'</b></div>';\n"
"  kq+='<div class=\"kq-item\"><label>拟招</label><b>'+f(d.plan)+'</b></div>';\n"
"  kq+='<div class=\"kq-item\"><label>复试人数</label><b>'+f(d.rec)+'</b></div>';\n"
"  kq+='<div class=\"kq-item\"><label>录取人数</label><b>'+f(d.adm)+'</b></div>';\n"
"  kq+='<div class=\"kq-item\"><label>复录比</label><b>'+f(d.rr==null?null:d.rr)+'</b></div>';\n"
"  kq+='<div class=\"kq-item\"><label>报录比</label><b>'+f(d.ratio==null?null:d.ratio)+'</b></div>';\n"
"  kq+='<div class=\"kq-item\"><label>录取最高</label><b>'+f(d.max_s)+'</b></div>';\n"
"  kq+='<div class=\"kq-item\"><label>录取最低</label><b>'+f(d.min_s)+'</b></div>';\n"
"  kq+='<div class=\"kq-item\"><label>录取平均</label><b>'+f(d.avg_s)+'</b></div>';\n"
"  kq+='</div>';\n"
"  kq+='<div class=\"kq-scope\">'+esc(d.scope||'查无')+'</div>';\n"
"  if(d.srcu){kq+='<div class=\"kq-src\"><a href=\"'+esc(d.srcu)+'\" target=\"_blank\" rel=\"noopener\">查看来源 ↗</a></div>';}\n"
"  kq+='</div>';\n"
"  return kq;\n"
"}\n"
"function renderKQ(){\n"
"  var arr=kqList().filter(function(d){\n"
"    if(kqState.tier==='川渝'&&['四川','重庆'].indexOf(d.p)<0)return false;\n"
"    if(kqState.tier==='外地'&&['四川','重庆'].indexOf(d.p)>=0)return false;\n"
"    if(kqState.kw){var hay=(d.n+d.c).toLowerCase();if(hay.indexOf(kqState.kw)<0)return false;}\n"
"    return true;\n"
"  });\n"
"  document.getElementById('kq-box').innerHTML=arr.map(kqCard).join('');\n"
"}\n"
"document.getElementById('kq-tier').addEventListener('click',function(e){\n"
"  if(!e.target.dataset.v)return;\n"
"  this.querySelectorAll('button').forEach(function(b){b.classList.toggle('active',b===e.target);});\n"
"  kqState.tier=e.target.dataset.v;renderKQ();\n"
"});\n"
"document.getElementById('kq-kw').addEventListener('input',function(e){kqState.kw=e.target.value.trim();renderKQ();});\n"
"renderKQ();\n"
)
anchor2 = "// ===== 热度榜"
assert anchor2 in s, "heat anchor"
s = s.replace(anchor2, KQ_JS + "\n" + anchor2, 1)

# ---------- SRCS 追加 ----------
NEW_SRCS = [
["成都信息工程计算机学院2026复试成绩","https://jsjxy.cuit.edu.cn/info/1062/3251.htm"],
["成都信息工程人工智能学院研究生页","https://qkl.cuit.edu.cn/rcpy/yjsjy.htm"],
["成都理工大学计算机学院（412反爬）","https://cist.cdut.edu.cn/info/1145/7596.htm"],
["重庆科技大学085410考情(启航)","https://jixun.iqihang.com/schoolkyfs/20265391.html"],
["中飞院2026拟录取公示","https://grs.cafuc.edu.cn/info/1009/2922.htm"],
["四川师大2026各专业录取最低分(中公)","http://sa.kaoyan365.cn/yanzhaoxinxi/sakylq/66939.html"],
["西南民大2026拟录取公示(附件反爬)","https://yjsglxt.swun.edu.cn/info/1047/2338.htm"],
["天津工业AI学院2026拟录取名单PDF","https://ai.tiangong.edu.cn/2026/0330/c5000a113645/page.htm"],
["西南交大085410招生(kaoyana)","https://www.kaoyana.com/s1071/085410/"],
["贵州大学2026复试结果公示","http://cs.gzu.edu.cn/_t2870/2026/0330/c16270a266766/page.htm"],
["广西大学2026调剂复试名单","https://scei.gxu.edu.cn/info/1005/4015.htm"],
["陕西师大2026录取最低分(中公)","http://sa.kaoyan365.cn/yanzhaoxinxi/sakyfsx/67721.html"],
["新疆大学2026录取最低分(中公)","http://sa.kaoyan365.cn/yanzhaoxinxi/sakyfsx/66985.html"],
["宁夏大学2026拟录取名单公示","https://graduate.nxu.edu.cn/info/1020/8544.htm"],
["华中师大2026拟录取名单公示","http://gs.ccnu.edu.cn/info/1028/6263.htm"],
["河南大学AI学院2026复试细则","https://ai.henu.edu.cn/info/1085/16422.htm"],
["福州大学085410招生(kaoyana)","https://www.kaoyana.com/s1096/085410/"],
["大连理工085410招生(kaoyana)","https://www.kaoyana.com/s1029/085410/"],
["华北电力085410招生(kaoyana)","https://www.kaoyana.com/s1090/085410/"],
["上海大学2026录取最低分(中公)","http://sa.kaoyan365.cn/yanzhaoxinxi/sakyfsx/67529.html"],
["青海大学2026一志愿成绩公示PDF","https://cs.qhu.edu.cn/docs//2026-03/5044754f48e142f1a58bae040c554215.pdf"],
["海南大学2026复试细则","https://sice.hainanu.edu.cn/info/1026/9883.htm"],
]
new_src_block = ",\n".join(json.dumps(x, ensure_ascii=False) for x in NEW_SRCS)
anchor3 = "];\n\n// ===== 工具函数"
assert anchor3 in s, "SRCS anchor"
s = s.replace(anchor3, ",\n".join([new_src_block, anchor3]), 1)

# ---------- CSS ----------
CSS = (
"\n#kq-box{display:grid;grid-template-columns:repeat(auto-fill,minmax(330px,1fr));gap:12px;margin-top:12px}\n"
".kq-card{background:var(--bg2);border:1px solid var(--rule);border-radius:12px;padding:14px 16px;box-shadow:0 1px 3px rgba(0,0,0,.04)}\n"
".kq-head{display:flex;flex-wrap:wrap;align-items:center;gap:8px;margin-bottom:10px}\n"
".kq-head b{font-size:15px}\n"
".kq-col{color:var(--muted);font-size:12px;flex:1;min-width:120px}\n"
".kq-tag{font-size:11px;padding:2px 8px;border-radius:99px;white-space:nowrap}\n"
".kq-tag.ok{background:#ecfdf5;color:var(--ok);border:1px solid #a7f3d0}\n"
".kq-tag.warn{background:#fffbeb;color:var(--warn);border:1px solid #fde68a}\n"
".kq-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:6px 10px;margin-bottom:10px}\n"
".kq-item{background:#f8fafc;border:1px solid var(--rule);border-radius:8px;padding:6px 8px;text-align:center}\n"
".kq-item label{display:block;font-size:11px;color:var(--muted)}\n"
".kq-item b{font-size:14px;color:var(--ink)}\n"
".kq-scope{font-size:12px;color:var(--muted);line-height:1.6;border-top:1px dashed var(--rule);padding-top:8px}\n"
".kq-src{margin-top:8px;text-align:right}\n"
".kq-src a{color:var(--accent);text-decoration:none;font-size:12px}\n"
"td.kq-num{background:#f0fdfa;color:#0f766e;font-weight:600}\n"
"td.kq-scope{font-size:11px;color:var(--muted);max-width:240px}\n"
"@media (max-width:720px){.kq-grid{grid-template-columns:repeat(3,1fr)}#kq-box{grid-template-columns:1fr}}\n"
)
assert "</style>" in s
s = s.replace("</style>", CSS + "\n</style>", 1)

# ---------- 章节重编号 ----------
for old, new in [("五、智能择校推荐器", "六、智能择校推荐器"), ("六、2027 报考时间轴", "七、2027 报考时间轴"), ("七、就业前景", "八、就业前景")]:
    assert old in s, old
    s = s.replace(old, new, 1)

io.open(HTML, "w", encoding="utf-8").write(s)
print("考情明细区块完成，SRCS 追加:", len(NEW_SRCS))
