# -*- coding: utf-8 -*-
"""2026 考情精细数据整合：S/C 字段更新 + K 映射更新（第 1 步）"""
import io, json, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BASE = r"<SOURCE_DIR>\02_院校数据_原有"
HTML = BASE + r"\全国408_085410双非热度版_20260820.html"
s = io.open(HTML, encoding="utf-8").read()

def grab_array(bm, em):
    a = s.index(bm) + len(bm)
    b = s.index(em, a) + 1
    return s[a:b]

S = json.loads(grab_array("var S=", "];\n// ===== 985/211"))
C = json.loads(grab_array("var C=", "];\n// ===== 初试科目映射"))

UPD = {
 ("成都信息工程大学","计算机学院"): dict(rec=2, adm=None, rr=None, ratio=None, max_s=276, min_s=274, avg_s=275.0,
    scope="一志愿第一批复试成绩公示：仅2人（274/276），后续多批调剂；计划25，线264", verified="官方✅", src="官方",
    srcu="https://jsjxy.cuit.edu.cn/info/1062/3251.htm"),
 ("成都信息工程大学","人工智能学院"): dict(rec=None, adm=None, rr=None, ratio=None, max_s=None, min_s=None, avg_s=None,
    scope="计划12，线264；一志愿/调剂成绩在学院官网动态页未能解析", verified="官方🔍",
    srcu="https://qkl.cuit.edu.cn/rcpy/yjsjy.htm"),
 ("成都理工大学","计算机与网络安全学院"): dict(rec=None, adm=None, rr=None, ratio=None, max_s=None, min_s=None, avg_s=None,
    scope="2026拟招23（不含推免，机构）；官网拟录取页反爬，复试/录取明细查无；复试有C语言机试斩杀线(VS2010)", verified="机构🔍",
    srcu="https://cist.cdut.edu.cn/info/1145/7596.htm"),
 ("重庆科技大学","计算机科学与工程学院（人工智能学院）"): dict(rec=None, adm=None, rr=None, ratio=None, max_s=None, min_s=None, avg_s=None,
    scope="复试线264（官方），差额≥120%；085410调剂9个名额说明一志愿缺额大；拟录取名单在学院官网（附件反爬）", verified="官方✅(线)+🔍(名单)",
    srcu="https://jixun.iqihang.com/schoolkyfs/20265391.html"),
 ("中国民用航空飞行学院","计算机与人工智能学院"): dict(rec=1, adm=1, rr=1.0, ratio=None, max_s=272, min_s=272, avg_s=272.0,
    scope="一志愿复试仅1人（272分，过线即录）；拟录取公示见研招官网", verified="官方✅",
    srcu="https://grs.cafuc.edu.cn/info/1009/2922.htm"),
 ("四川师范大学","计算机科学学院"): dict(rec=None, adm=2, rr=None, ratio=None, max_s=301, min_s=301, avg_s=301.0,
    scope="中公录取数据：085410拟录取2人，初试最低301；复试线264（官方）", verified="机构🔍",
    srcu="http://sa.kaoyan365.cn/yanzhaoxinxi/sakylq/66939.html"),
 ("西南民族大学","计算机与人工智能学院"): dict(rec=None, adm=None, rr=None, ratio=None, max_s=None, min_s=None, avg_s=None,
    scope="复试线264；拟录取名单附件官网反爬(412)，录取人数查无", verified="官方🔍(线)",
    srcu="https://yjsglxt.swun.edu.cn/info/1047/2338.htm"),
 ("天津工业大学","人工智能学院"): dict(rec=None, adm=40, rr=None, ratio=None, max_s=391, min_s=332, avg_s=352.9,
    scope="一志愿拟录取40人（含退役1人314）；普通39人最高391、最低332、均352.9；目录拟招33(31不含推免)", verified="官方✅",
    srcu="https://ai.tiangong.edu.cn/2026/0330/c5000a113645/page.htm"),
 ("天津理工大学","计算机科学与工程学院"): dict(rec=None, adm=None, rr=None, ratio=None, max_s=None, min_s=None, avg_s=None,
    scope="复试线315（官方），拟招42；复试名单/录取明细未单独核查", verified="官方✅(线)"),
 ("重庆邮电大学","人工智能学院"): dict(rec=None, adm=None, rr=1.35, ratio=None, max_s=None, min_s=None, avg_s=None,
    scope="⚠️085410考861自控原理（非408）不满足22408；336线为对照，复录比约1.35", verified="官方✅"),
 ("西南交通大学","计算机与人工智能学院"): dict(rec=None, adm=None, rr=None, ratio=None, max_s=None, min_s=None, avg_s=None,
    scope="计算机与AI学院30人+信息学院18人，均22408（kaoyana）；复试线310（官方）；复试名单PDF下载受限，明细查无", verified="机构🔍(科目)+官方(线)",
    srcu="https://www.kaoyana.com/s1071/085410/"),
 ("西南大学","人工智能学院"): dict(rec=None, adm=None, rr=None, ratio=None, max_s=None, min_s=None, avg_s=None,
    scope="2026年无085410（085400）；2027年改设085410并考408，历史线无", verified="官方✅(2027公告)"),
 ("四川大学","计算机学院（相关）"): dict(rec=None, adm=None, rr=None, ratio=None, max_s=None, min_s=None, avg_s=None,
    scope="全日制未设085410（AI相关为140500学硕·英一数一408或085400电子信息）；2024仅航空航天学院非全085410，不符合22408", verified="机构🔍",
    srcu="https://www.kaoyana.com/s1015/140500/50900/"),
 ("重庆大学","计算机学院（相关）"): dict(rec=None, adm=None, rr=None, ratio=None, max_s=None, min_s=None, avg_s=None,
    scope="未设085410（计算机专硕走085400/085404）", verified="机构🔍"),
 ("贵州大学","计算机科学与技术学院"): dict(rec=60, adm=None, rr=None, ratio=None, max_s=395, min_s=303, avg_s=335.4,
    scope="复试结果公示：085410一志愿60人进复试（2人缺考），初试最高395、最低303、均335.4；2026改考408(数二+408)；拟录取名单另公示", verified="官方✅",
    srcu="http://cs.gzu.edu.cn/_t2870/2026/0330/c16270a266766/page.htm"),
 ("广西大学","计算机与电子信息学院"): dict(rec=None, adm=None, rr=None, ratio=None, max_s=None, min_s=None, avg_s=None,
    scope="全日制67(含推免35)+非全30，均22408(2026)；4/8调剂复试名单：全日制96人+非全44人；一志愿拟录取附件官网404，录取人数查无", verified="机构✅(科目)+官方(名单)",
    srcu="https://scei.gxu.edu.cn/info/1005/4015.htm"),
 ("陕西师范大学","人工智能与计算机学院"): dict(rec=None, adm=9, rr=None, ratio=None, max_s=361, min_s=276, avg_s=324.6,
    scope="中公录取数据：拟录取9人（含退役1人318）；普通全日制8人初试361/325/361/361/314/310/289/276，最高361、最低276、均324.6", verified="机构🔍",
    srcu="http://sa.kaoyan365.cn/yanzhaoxinxi/sakyfsx/67721.html"),
 ("新疆大学","计算机科学与技术学院（相关）"): dict(rec=None, adm=None, rr=None, ratio=None, max_s=None, min_s=None, avg_s=None,
    scope="未单设085410（AI方向在085400电子信息/085404计算机技术内）；085404拟录取274人、初试最低254（中公）", verified="机构🔍",
    srcu="http://sa.kaoyan365.cn/yanzhaoxinxi/sakyfsx/66985.html"),
 ("宁夏大学","信息工程学院"): dict(rec=None, adm=12, rr=None, ratio=None, max_s=391, min_s=259, avg_s=337.2,
    scope="拟录取12人：一志愿5人(259/272/278/280/322)+调剂7人(370/370/373/374/376/381/391)，最高391、最低259、均337.2", verified="官方✅",
    srcu="https://graduate.nxu.edu.cn/info/1020/8544.htm"),
 ("华中师范大学","人工智能教育学部"): dict(rec=None, adm=45, rr=None, ratio=None, max_s=388, min_s=331, avg_s=355.3,
    scope="拟录取名单公示(039学部)：085410共45人（含退役1人309、定向1人263）；统考普通43人最高388、最低331、均355.3", verified="官方✅",
    srcu="http://gs.ccnu.edu.cn/info/1028/6263.htm"),
 ("河南大学","人工智能学院"): dict(rec=35, adm=35, rr=1.0, ratio=None, max_s=None, min_s=None, avg_s=None,
    scope="拟招35、进复试35，复录比≈1:1，线264；复试含机试", verified="官方✅",
    srcu="https://ai.henu.edu.cn/info/1085/16422.htm"),
 ("福州大学","计算机与大数据学院"): dict(rec=None, adm=None, rr=1.2, ratio=None, max_s=None, min_s=None, avg_s=None,
    scope="计划28（kaoyana），线264；复试结果附件在镜像站为付费文档，官网明细查无；复录比1.2为2025口径（62进51）", verified="机构🔍",
    srcu="https://www.kaoyana.com/s1096/085410/"),
 ("大连理工大学","计算机科学与技术学院"): dict(rec=None, adm=None, rr=1.6, ratio=None, max_s=None, min_s=None, avg_s=None,
    scope="⚠️085410考英一数一(11408)，不符合22408；计算机学院统考14人", verified="机构🔍",
    srcu="https://www.kaoyana.com/s1029/085410/"),
 ("华北电力大学","控制与计算机工程学院"): dict(rec=None, adm=None, rr=None, ratio=None, max_s=None, min_s=None, avg_s=None,
    scope="⚠️085410仅非全日制55人，考842自控原理基础（非408）；保定自动化系085410非全考841；不符合全日制22408", verified="机构🔍",
    srcu="https://www.kaoyana.com/s1090/085410/"),
 ("上海大学","计算机工程与科学学院"): dict(rec=None, adm=7, rr=None, ratio=None, max_s=None, min_s=305, avg_s=None,
    scope="中公录取数据：拟录取7人，初试最低305", verified="机构🔍",
    srcu="http://sa.kaoyan365.cn/yanzhaoxinxi/sakyfsx/67529.html"),
 ("上海大学","未来技术学院（人工智能研究院）"): dict(rec=None, adm=90, rr=None, ratio=None, max_s=None, min_s=334, avg_s=None,
    scope="中公录取数据：拟录取90人；普通最低334（另有退役278）", verified="机构🔍",
    srcu="http://sa.kaoyan365.cn/yanzhaoxinxi/sakyfsx/67529.html"),
 ("青海大学","计算机技术与应用学院"): dict(rec=44, adm=None, rr=None, ratio=None, max_s=354, min_s=284, avg_s=308.2,
    scope="一志愿复试成绩公示44人，初试最高354、最低284、均308.2；拟录取名单见研招网公示；计划25/32（口径不一）", verified="官方✅",
    srcu="https://cs.qhu.edu.cn/docs//2026-03/5044754f48e142f1a58bae040c554215.pdf"),
 ("海南大学","信息与通信工程学院"): dict(rec=42, adm=None, rr=1.24, ratio=None, max_s=None, min_s=None, avg_s=None,
    scope="计划37含推免3→统考34；进复试42人（含并列），线254，120%差额；复试笔试数据结构", verified="官方✅",
    srcu="https://sice.hainanu.edu.cn/info/1026/9883.htm"),
}

for d in S + C:
    upd = UPD.get((d["n"], d["c"]))
    if upd:
        d.update(upd)

NOTE_APPEND = {
    "西南交通大学": "；2026计算机与AI学院30+信息学院18，均22408",
    "西南大学": "2026无085410（085400）；2027改设085410+408",
    "四川大学": "全日制无085410；AI相关为140500学硕(英一数一408)/085400",
    "重庆大学": "未设085410",
    "贵州大学": "；2026改考408确认（085410=数二+408）",
    "广西大学": "；2026全日制67+非全30均22408",
    "陕西师范大学": "；拟录取9人（含退役1）",
    "新疆大学": "未单设085410；085404计算机技术274人",
    "宁夏大学": "；拟录取12人（一志愿5+调剂7）",
    "华中师范大学": "；拟录取45人（含退役/定向）",
    "河南大学": "；复录比≈1:1",
    "福州大学": "；计划28",
    "大连理工大学": "；085410为11408，不符合22408",
    "华北电力大学": "；085410仅非全，考842非408",
    "上海大学": "；计院录取7最低305 / 未来技术录取90最低334",
    "青海大学": "；一志愿复试44人",
    "海南大学": "；复试42人/统考计划34",
    "天津工业大学": "；一志愿录取40人（含退役1）",
    "四川师范大学": "；录取2人最低301",
    "成都理工大学": "；复试有C语言机试斩杀线",
    "重庆科技大学": "；调剂9名额说明一志愿缺额",
    "中国民用航空飞行学院": "；一志愿复试1人",
    "西南民族大学": "；拟录取附件反爬",
}
for d in S + C:
    if d["n"] in NOTE_APPEND:
        d["note"] = (d.get("note") or "") + NOTE_APPEND[d["n"]]

K_REPLACE = {
    "大连理工大学": "11408", "华北电力大学": "非408", "贵州大学": "22408", "广西大学": "22408",
    "西南交通大学": "22408", "陕西师范大学": "22408", "新疆大学": "未单设", "四川大学": "无085410",
    "重庆大学": "无085410", "西南大学": "22408(2027)",
}
K = json.loads(grab_array("var K=", "};\nfunction exKey"))
for k, v in K_REPLACE.items():
    K[k] = v

def ser_arr(arr):
    return "[\n" + ",\n".join(json.dumps(d, ensure_ascii=False, separators=(",", ":")) for d in arr) + "\n]"

s = s.replace(grab_array("var S=", "];\n// ===== 985/211"), ser_arr(S))
s = s.replace(grab_array("var C=", "];\n// ===== 初试科目映射"), ser_arr(C))
# K 对象在 C 之后，重新定位再替换（避免旧索引失效）
ka2 = s.index("var K=") + len("var K=")
kb2 = s.index("};\nfunction exKey") + 1
s = s[:ka2] + json.dumps(K, ensure_ascii=False, indent=0) + s[kb2:]

io.open(HTML, "w", encoding="utf-8").write(s)
print("数据更新完成 S:", len(S), "C:", len(C))
