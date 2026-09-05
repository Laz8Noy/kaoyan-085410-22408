# -*- coding: utf-8 -*-
"""2026 考情精细数据整合：总览表 / 招录比表加列（第 2 步）"""
import io, re, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

HTML = r"<SOURCE_DIR>\02_院校数据_原有\全国408_085410双非热度版_20260820.html"
s = io.open(HTML, encoding="utf-8").read()

def span(bm, em):
    a = s.index(bm)
    b = s.index(em, a)
    return a, b

def rep(a, b, new):
    global s
    s = s[:a] + new + s[b:]

# ---- OV_COLS ----
a = s.index("var OV_COLS=[")
b = s.index("];", a) + 2
NEW_OV = """var OV_COLS=[
  ["院校","#",0],["省份","#",1],["大区","#",2],["层次","#",3],["学院","#",4],
  ["初试科目","#",5],["方向","#",6],["2026复试线","num",7],["历年线(23/24/25/26)","#",8],["线差","num",9],["拟招","#",10],
  ["一志愿/调剂","#",11],["报录比","num",12],["复录比","num",13],
  ["复试人数","num",14],["录取人数","num",15],["录取最高","num",16],["录取最低","num",17],["录取平均","num",18],["口径","#",19],
  ["AI方向备注","#",20],["来源","#",21],["网络热度","num",22],["备注","#",23]
];"""
rep(a, b, NEW_OV)

# ---- ovRow ----
a, b = span("function ovRow(r){", "function ovPass")
NEW_OVROW = """function ovRow(r){
  var d=S[r];
  return "<tr>"+
    "<td><b>"+d.n+"</b></td>"+
    "<td>"+d.p+"</td>"+
    "<td>"+regionCell(d.r)+"</td>"+
    "<td>"+tierTag(d.t)+"</td>"+
    "<td>"+esc(d.c)+"</td>"+
    "<td>"+exCell(exKey(d))+"</td>"+
    "<td>"+esc(d.d)+"</td>"+
    "<td>"+lineCell(d.l)+"</td>"+
    '<td class="lh-col">'+lhCell(d)+"</td>"+
    '<td class="num">'+(gapOf(d)===null?'<span class="na">—</span>':(gapOf(d)===0?'=国家线':"+"+gapOf(d)))+"</td>"+
    "<td>"+esc(d.plan)+"</td>"+
    "<td>"+esc(d.fc)+"</td>"+
    '<td class="num '+(d.ratio!=null?"num-hl":"")+'">'+numOrNa(d.ratio==null?null:d.ratio)+"</td>"+
    '<td class="num '+(d.rr!=null?"num-warn":"")+'">'+numOrNa(d.rr==null?null:d.rr)+"</td>"+
    '<td class="num kq-num">'+numOrNa(d.rec==null?null:d.rec)+"</td>"+
    '<td class="num kq-num">'+numOrNa(d.adm==null?null:d.adm)+"</td>"+
    '<td class="num kq-num">'+numOrNa(d.max_s==null?null:d.max_s)+"</td>"+
    '<td class="num kq-num">'+numOrNa(d.min_s==null?null:d.min_s)+"</td>"+
    '<td class="num kq-num">'+numOrNa(d.avg_s==null?null:d.avg_s)+"</td>"+
    '<td class="kq-scope">'+esc(d.scope||"—")+"</td>"+
    "<td>"+aiTag(d.ai)+"</td>"+
    "<td>"+relTag(d.src)+"</td>"+
    '<td class="num">'+d.net+"</td>"+
    '<td class="score-cell">'+esc(d.note)+"</td></tr>";
}"""
rep(a, b, NEW_OVROW)

# ---- ovSortKey ----
a, b = span("function ovSortKey(i){", "function renderOv")
NEW_OVSORT = """function ovSortKey(i){
  var d=S[i];
  var c=OV_COLS[ov.sort][1];
  if(c==="num"){
    if(ov.sort===7)return d.l==null?-9999:d.l;
    if(ov.sort===8)return lastLine(d);
    if(ov.sort===9)return gapOf(d)===null?-9999:gapOf(d);
    if(ov.sort===12)return d.ratio==null?-9999:d.ratio;
    if(ov.sort===13)return d.rr==null?-9999:d.rr;
    if(ov.sort===14)return d.rec==null?-9999:d.rec;
    if(ov.sort===15)return d.adm==null?-9999:d.adm;
    if(ov.sort===16)return d.max_s==null?-9999:d.max_s;
    if(ov.sort===17)return d.min_s==null?-9999:d.min_s;
    if(ov.sort===18)return d.avg_s==null?-9999:d.avg_s;
    if(ov.sort===22)return d.net==null?-9999:d.net;
  }
  if(ov.sort===0)return d.n;
  if(ov.sort===1)return d.p;
  if(ov.sort===2)return d.r;
  if(ov.sort===3)return d.t;
  if(ov.sort===4)return d.c;
  if(ov.sort===5)return exKey(d);
  if(ov.sort===6)return d.d;
  if(ov.sort===19)return d.scope;
  if(ov.sort===20)return d.ai;
  return esc(S[i].note);
}"""
rep(a, b, NEW_OVSORT)

# ---- RATIO_COLS ----
a = s.index("var RATIO_COLS=[")
b = s.index("];", a) + 2
NEW_RC = """var RATIO_COLS=[
  ["院校","#",0],["大区","#",1],["层次","#",2],["学院","#",3],["初试科目","#",4],
  ["2026线","num",5],["线差","num",6],["拟招","#",7],["一志愿/调剂","#",8],["报录比","num",9],
  ["复录比","num",10],["复试人数","num",11],["录取人数","num",12],["录取最高","num",13],["录取最低","num",14],["录取平均","num",15],
  ["竞争热度","num",16],["来源","#",17]
];"""
rep(a, b, NEW_RC)

# ---- ratioSortKey ----
a, b = span("function ratioSortKey(i){", "function renderRatio")
NEW_RSORT = """function ratioSortKey(i){
  var d=S[i];
  var c=RATIO_COLS[rstate.sort][1];
  if(c==="num"){
    if(rstate.sort===5)return d.l==null?-9999:d.l;
    if(rstate.sort===6)return gapOf(d)===null?-9999:gapOf(d);
    if(rstate.sort===9)return d.ratio==null?-9999:d.ratio;
    if(rstate.sort===10)return d.rr==null?-9999:d.rr;
    if(rstate.sort===11)return d.rec==null?-9999:d.rec;
    if(rstate.sort===12)return d.adm==null?-9999:d.adm;
    if(rstate.sort===13)return d.max_s==null?-9999:d.max_s;
    if(rstate.sort===14)return d.min_s==null?-9999:d.min_s;
    if(rstate.sort===15)return d.avg_s==null?-9999:d.avg_s;
    if(rstate.sort===16)return compScore(d);
  }
  if(rstate.sort===0)return d.n;
  if(rstate.sort===1)return d.r;
  if(rstate.sort===2)return d.t;
  if(rstate.sort===3)return d.c;
  if(rstate.sort===4)return exKey(d);
  if(rstate.sort===8)return d.fc;
  return d.src;
}"""
rep(a, b, NEW_RSORT)

# ---- renderRatio 行模板 ----
a = s.index('document.getElementById("ratio-thr").innerHTML=h;') + len('document.getElementById("ratio-thr").innerHTML=h;')
b = s.index('document.getElementById("ratio-tb").innerHTML=body;', a)
NEW_RBODY = """
  var body="";
  idx.forEach(function(i){
    var d=S[i];
    body+="<tr>"+
      "<td><b>"+d.n+"</b></td>"+
      "<td>"+regionCell(d.r)+"</td>"+
      "<td>"+tierTag(d.t)+"</td>"+
      "<td>"+esc(d.c)+"</td>"+
      "<td>"+exCell(exKey(d))+"</td>"+
      "<td>"+lineCell(d.l)+"</td>"+
      '<td class="num">'+(gapOf(d)===null?'<span class="na">—</span>':(gapOf(d)===0?"=线":"+"+gapOf(d)))+"</td>"+
      "<td>"+esc(d.plan)+"</td>"+
      "<td>"+esc(d.fc)+"</td>"+
      '<td class="num">'+numOrNa(d.ratio==null?null:d.ratio)+"</td>"+
      '<td class="num">'+numOrNa(d.rr==null?null:d.rr)+"</td>"+
      '<td class="num kq-num">'+numOrNa(d.rec==null?null:d.rec)+"</td>"+
      '<td class="num kq-num">'+numOrNa(d.adm==null?null:d.adm)+"</td>"+
      '<td class="num kq-num">'+numOrNa(d.max_s==null?null:d.max_s)+"</td>"+
      '<td class="num kq-num">'+numOrNa(d.min_s==null?null:d.min_s)+"</td>"+
      '<td class="num kq-num">'+numOrNa(d.avg_s==null?null:d.avg_s)+"</td>"+
      '<td class="num"><b>'+compScore(d)+"</b></td>"+
      "<td>"+relTag(d.src)+"</td></tr>";
  });
"""
rep(a, b, NEW_RBODY)

io.open(HTML, "w", encoding="utf-8").write(s)
print("列扩展完成")
