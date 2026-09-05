# -*- coding: utf-8 -*-
"""
v4：在 20260820 版基础上：
  1) 给"打杠"及主要学校补 lh=[2023,2024,2025] 历年复试线
  2) 总览大表新增"历年线(23/24/25/26)"列
  3) 详情卡片显示历年线
  4) 新增图5：历年复试线趋势折线图
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

# ---------- 1) 注入 lh 历年线字段（2023/2024/2025） ----------
LH = {
    "华北理工大学": [273, 273, 260],
    "河北大学": [273, 273, 260],
    "内蒙古工业大学": [270, 296, 296],
    "大连海洋大学": [273, 273, 260],
    "常州大学": [273, 315, 278],
    "安徽工程大学": [None, None, 260],
    "河北工程大学": [None, None, None],
    "江苏海洋大学": [None, None, None],
    "苏州大学": [334, 273, 351],
    "中国石油大学（华东）": [320, 327, 336],
    "华中农业大学": [295, 317, 306],
    "广西大学": [None, 264, 277],
    "暨南大学": [306, 318, 331],
    "中国矿业大学（徐州）": [None, None, None],
    "西南大学": [None, None, None],
}

def inject_lh(name, arr):
    global s
    pat = re.compile(r'(\{"n":"' + re.escape(name) + r'"[^}]*?),\s*"note":')
    m = pat.search(s)
    if not m:
        raise SystemExit("未找到学校行: " + name)
    lh = ",".join("null" if v is None else str(v) for v in arr)
    s = pat.sub(r'\1,"lh":[' + lh + r'],"note":', s, count=1)

for name, arr in LH.items():
    inject_lh(name, arr)

# ---------- 2) 总览表加"历年线"列 ----------
OV_COLS_OLD = '''var OV_COLS=[
  ["院校","#",0],["省份","#",1],["大区","#",2],["层次","#",3],["学院","#",4],
  ["初试科目","#",5],["方向","#",6],["2026复试线","num",7],["线差","num",8],["拟招","#",9],
  ["一志愿/调剂","#",10],["报录比","num",11],["复录比","num",12],
  ["AI方向备注","#",13],["来源","#",14],["网络热度","num",15],["备注","#",16]
];'''
OV_COLS_NEW = '''var OV_COLS=[
  ["院校","#",0],["省份","#",1],["大区","#",2],["层次","#",3],["学院","#",4],
  ["初试科目","#",5],["方向","#",6],["2026复试线","num",7],["历年线(23/24/25/26)","#",8],["线差","num",9],["拟招","#",10],
  ["一志愿/调剂","#",11],["报录比","num",12],["复录比","num",13],
  ["AI方向备注","#",14],["来源","#",15],["网络热度","num",16],["备注","#",17]
];'''
rep(OV_COLS_OLD, OV_COLS_NEW)

rep('''    "<td>"+lineCell(d.l)+"</td>"+
    '<td class="num">'+(gapOf(d)===null?'<span class="na">—</span>':(gapOf(d)===0?'=国家线':"+"+gapOf(d)))+"</td>"+''',
    '''    "<td>"+lineCell(d.l)+"</td>"+
    "<td>"+lhCell(d)+"</td>"+
    '<td class="num">'+(gapOf(d)===null?'<span class="na">—</span>':(gapOf(d)===0?'=国家线':"+"+gapOf(d)))+"</td>"+''')

rep('''  if(c==="num"){
    if(ov.sort===7)return d.l==null?-9999:d.l;
    if(ov.sort===8)return gapOf(d)===null?-9999:gapOf(d);
    if(ov.sort===11)return d.ratio==null?-9999:d.ratio;
    if(ov.sort===12)return d.rr==null?-9999:d.rr;
    if(ov.sort===15)return d.net==null?-9999:d.net;
  }''',
    '''  if(c==="num"){
    if(ov.sort===7)return d.l==null?-9999:d.l;
    if(ov.sort===8)return lastLine(d);
    if(ov.sort===9)return gapOf(d)===null?-9999:gapOf(d);
    if(ov.sort===12)return d.ratio==null?-9999:d.ratio;
    if(ov.sort===13)return d.rr==null?-9999:d.rr;
    if(ov.sort===16)return d.net==null?-9999:d.net;
  }''')

# ---------- 3) 详情卡片显示历年线 ----------
rep('''    subjects+="<li>"+exCell(exKey(d))+" · 2026复试线 "+lineCell(d.l)+" · "+(gapOf(d)===null?"线差未核":(gapOf(d)===0?"=国家线":"+"+gapOf(d)))+" · "+relTag(d.src)+"</li>";''',
    '''    subjects+="<li>历年复试线(2023/24/25/26)："+lhStr(d)+"</li>";
    subjects+="<li>"+exCell(exKey(d))+" · 2026复试线 "+lineCell(d.l)+" · "+(gapOf(d)===null?"线差未核":(gapOf(d)===0?"=国家线":"+"+gapOf(d)))+" · "+relTag(d.src)+"</li>";''')

# ---------- 4) 图5 折线图：CSS + HTML + JS ----------
CSS = '''
.line-chart{width:100%;overflow-x:auto;-webkit-overflow-scrolling:touch;margin-top:6px}
.line-chart svg{display:block;width:100%;min-width:560px;height:auto}
#line-school{flex:1;min-width:200px;padding:8px 12px;border:1px solid var(--rule);border-radius:8px;font-size:13.5px;background:#fff;color:var(--ink)}
.lc-legend{display:flex;gap:16px;flex-wrap:wrap;font-size:12px;color:var(--muted);margin-top:8px}
.lc-legend i{display:inline-block;width:22px;height:3px;border-radius:2px;margin-right:5px;vertical-align:middle}
'''
rep('</style>', CSS + '</style>')

FIG5 = '''
  <figure class="chart-figure">
    <figcaption>图5｜历年复试线趋势（2023-2026 · 下拉选校 · 橙色虚线=当年A区国家线）</figcaption>
    <div>
      <div class="filters" style="margin-top:0">
        <select id="line-school" aria-label="选择院校"></select>
        <span style="font-size:12px;color:var(--muted)">仅列出有 ≥2 年复试线数据的招生单位；B区院校请对照当年B区国家线</span>
      </div>
      <div id="line-chart" class="line-chart"></div>
      <div class="lc-legend">
        <span><i style="background:#0f766e"></i>院校复试线（实线）</span>
        <span><i style="background:#b45309"></i>A区国家线（虚线，2023/24=273 · 2025=260 · 2026=264）</span>
      </div>
    </div>
  </figure>
'''
rep('''</figure>
  </div>
  <div class="banner tip" style="margin:12px 0">
    <b>怎么读：</b>''', '''</figure>
''' + FIG5 + '''  </div>
  <div class="banner tip" style="margin:12px 0">
    <b>怎么读：</b>''')

LINE_JS = r'''
// ===== 图5：历年复试线趋势（2023-2026）=====
var LINE_NAT_A=[273,273,260,264];
var LINE_YEARS=[2023,2024,2025,2026];
function lhArr(d){return d.lh||[null,null,null];}
function lastLine(d){
  var a=lhArr(d).concat([d.l]);
  for(var i=a.length-1;i>=0;i--){if(a[i]!=null)return a[i];}
  return -9999;
}
function lhStr(d){
  var a=lhArr(d).concat([d.l]);
  return a.map(function(v){return v==null?"—":v;}).join(" / ");
}
function lhCell(d){return '<span style="font-size:11px">'+lhStr(d)+"</span>";}
function lineSchoolList(){
  var map={};
  S.concat(C).forEach(function(d){
    var pts=lhArr(d).concat([d.l]);
    var cnt=pts.filter(function(v){return v!=null;}).length;
    if(cnt<2)return;
    var cur=map[d.n];
    if(!cur||cnt>cur.cnt)map[d.n]={n:d.n,c:d.c,lh:d.lh,l:d.l,cnt:cnt};
  });
  var arr=Object.keys(map).map(function(k){return map[k];});
  arr.sort(function(a,b){return lastLine(b)-lastLine(a);});
  return arr;
}
var lineData=lineSchoolList();
function renderLineChart(){
  var box=document.getElementById("line-chart");
  var sel=document.getElementById("line-school");
  var d=lineData[+sel.value];
  if(!d){box.innerHTML='<div style="padding:16px;color:var(--muted);font-size:13px">所选院校暂无历年线数据</div>';return;}
  var W=720,H=300,PL=48,PR=20,PT=22,PB=36;
  var vals=lhArr(d).concat([d.l]);
  var valid=vals.filter(function(v){return v!=null;});
  var lo=Math.min.apply(null,valid),hi=Math.max.apply(null,valid);
  lo=Math.max(230,Math.floor((lo-12)/10)*10);hi=Math.min(400,Math.ceil((hi+14)/10)*10);
  if(hi-lo<40)hi=lo+40;
  function X(i){return PL+i*(W-PL-PR)/3;}
  function Y(v){return PT+(H-PT-PB)*(1-(v-lo)/(hi-lo));}
  var html='<svg viewBox="0 0 '+W+' '+H+'" preserveAspectRatio="xMidYMid meet">';
  for(var g=lo;g<=hi;g+=20){
    var yy=Y(g);
    html+='<line x1="'+PL+'" y1="'+yy+'" x2="'+(W-PR)+'" y2="'+yy+'" stroke="#edf1ef" stroke-width="1"/>';
    html+='<text x="'+(PL-6)+'" y="'+(yy+4)+'" text-anchor="end" font-size="11" fill="#8a96a0">'+g+"</text>";
  }
  var nat="",natLab="";
  LINE_NAT_A.forEach(function(v,i){
    var yy=Y(Math.max(lo,Math.min(hi,v)));
    nat+=(i?"L":"M")+X(i)+" "+yy+" ";
    natLab+='<text x="'+X(i)+'" y="'+(yy-4)+'" text-anchor="middle" font-size="9.5" fill="#b45309">国'+v+"</text>";
  });
  html+='<path d="'+nat+'" fill="none" stroke="#b45309" stroke-width="1.5" stroke-dasharray="5,4" opacity=".85"/>'+natLab;
  var pts=[];
  vals.forEach(function(v,i){if(v!=null)pts.push(X(i)+" "+Y(v));});
  if(pts.length>=2){
    var pth=pts.map(function(t,j){return (j?"L":"M")+t;}).join(" ");
    html+='<path d="'+pth+'" fill="none" stroke="#0f766e" stroke-width="2.6" stroke-linejoin="round"/>';
  }
  vals.forEach(function(v,i){
    if(v==null)return;
    html+='<circle cx="'+X(i)+'" cy="'+Y(v)+'" r="5" fill="#0f766e" stroke="#fff" stroke-width="1.5"/>';
    html+='<text x="'+X(i)+'" y="'+(Y(v)-10)+'" text-anchor="middle" font-size="12" font-weight="700" fill="#173042">'+v+"</text>";
  });
  LINE_YEARS.forEach(function(y,i){
    html+='<text x="'+X(i)+'" y="'+(H-12)+'" text-anchor="middle" font-size="12" fill="#5d7182">'+y+"年</text>";
  });
  html+='</svg>';
  box.innerHTML='<div style="margin-bottom:4px;font-weight:700;color:var(--ink)">'+d.n+'（'+esc(d.c)+"）</div>"+html;
}
(function(){
  var sel=document.getElementById("line-school");
  lineData.forEach(function(d,i){
    sel.innerHTML+='<option value="'+i+'">'+d.n+" · "+esc(d.c)+"</option>";
  });
  sel.addEventListener("change",renderLineChart);
  renderLineChart();
})();
'''
rep('// ===== 统计', LINE_JS + '\n// ===== 统计')

# ---------- SRCS 补来源 ----------
rep('["研招网2027硕士专业目录（待发布）","https://yz.chsi.com.cn/"],',
    '["研招网2027硕士专业目录（待发布）","https://yz.chsi.com.cn/"],\n'
    '["历年线·启航院校库（河北大学/常州大学/苏大/广西大学等）","https://jixun.iqihang.com/"],\n'
    '["历年线·中公研招信息（华北理工/内蒙工业/大连海洋等）","http://yz.kaoyan365.cn/"],\n'
    '["历年线·黑眼圈院校库（河北大学/苏大/华北理工）","https://www.heiyanquan.fun/"],')

for out in OUTS:
    with io.open(out, "w", encoding="utf-8") as f:
        f.write(s)
    print("已写入:", out, len(s))
print("lh注入数:", len(LH))
