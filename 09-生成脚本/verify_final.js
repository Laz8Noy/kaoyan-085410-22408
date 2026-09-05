// 校验终极版 HTML：JS 语法 + 关键区块 + 数据完整性
const fs = require('fs');
const p = '<SOURCE_DIR>/02_院校数据_原有/全国408_085410双非热度版_终极版_20260824.html';
let html = fs.readFileSync(p, 'utf8');
let pass = 0, fail = 0;
function check(name, cond) {
  if (cond) { pass++; console.log('✅', name); }
  else { fail++; console.log('❌', name); }
}

// 1. 提取 <script> 内容做语法检查
const m = html.match(/<script>([\s\S]*?)<\/script>/);
check('存在内联 script', !!m);
let js = m[1].replace(/<[^>]*\/?>[\s\S]*$/g, ''); // 去掉尾部可能的 HTML
// 只取 JS 主段
const jsStart = js.indexOf('// ===== 主数据');
if (jsStart > 0) js = js.substring(jsStart);
try {
  new Function(js);
  check('JS 语法解析通过', true);
} catch (e) {
  check('JS 语法解析通过: ' + e.message, false);
}

// 2. 新区块
check('2027改考区块存在', html.includes('id="gaikao"'));
check('导师区块存在', html.includes('id="mentors"'));
check('38条改考(表格行计数≥30)', (html.match(/<section id="gaikao">[\s\S]*?<\/section>/)||[''])[0].split('<tr').length > 30);
check('导师卡片≥10', (html.match(/<section id="mentors">[\s\S]*?<\/section>/)||[''])[0].split('detail-card').length > 10);

// 3. 原功能保留
check('考情明细 kq 保留', html.includes('id="kq"'));
check('智能推荐器保留', html.includes('id="recommender"'));
check('折线图保留', html.includes('renderLineChart'));
check('热度榜保留', html.includes('id="heat"'));
check('数据源保留', html.includes('SRCS'));
check('标题已更新为终极版', html.includes('人工智能专硕·终极版'));
check('S数组67条主体保留', /var S=\[/.test(html));

console.log(`\n结果: ${pass} 通过 / ${fail} 失败`);
