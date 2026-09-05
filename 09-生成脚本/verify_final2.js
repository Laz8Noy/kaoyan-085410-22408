// 精确验证终极版 HTML 静态结构
const fs = require('fs');
const p = '<SOURCE_DIR>/02_院校数据_原有/全国408_085410双非热度版_终极版_20260824.html';
const html = fs.readFileSync(p, 'utf8');
let pass = 0, fail = 0;
function check(name, cond) { if (cond) { pass++; console.log('✅', name); } else { fail++; console.log('❌', name); } }

// script 边界
const sScript = html.indexOf('<script>');
const eScript = html.indexOf('</script>');
check('script 在 30k 附近(未被注入污染)', sScript > 29000 && sScript < 32000);

// 静态区块顺序（都在 script 之前）
const order = ['overview', 'ratio', 'heat', 'viz', 'gaikao', 'mentors', 'kq', 'recommender', 'timeline', 'career', 'detail', 'other408'];
let prev = -1, ok = true;
for (const id of order) {
  const idx = html.indexOf(`id="${id}"`);
  if (idx < 0) { console.log('❌ 找不到 id=', id); fail++; ok = false; continue; }
  if (idx < prev) { console.log(`❌ 顺序错误: ${id} @${idx} < prev ${prev}`); fail++; ok = false; }
  else if (idx > eScript && !['detail','other408'].includes(id)) { console.log(`⚠️ ${id} 在 script 之后?`); }
  prev = idx;
}
if (ok) { pass++; console.log('✅ 区块顺序正确（gaikao/mentors 插入在 kq 前）'); }

// 新区块内容
const gkSec = html.slice(html.indexOf('<section id="gaikao"'), html.indexOf('<section id="mentors"'));
check('改考表格行 ≥ 38', (gkSec.match(/<tr/g) || []).length >= 38);
check('改考含标题', gkSec.includes('改考动态'));
const mtSec = html.slice(html.indexOf('<section id="mentors"'), html.indexOf('<section id="kq"'));
check('导师卡片 = 16', (mtSec.match(/detail-card/g) || []).length === 16);
check('导师含 Agent 关键词(大模型)', mtSec.includes('大模型'));
check('导师含 具身智能', mtSec.includes('具身智能'));

// 关键功能保留
check('折线图函数', html.includes('renderLineChart'));
check('考情明细渲染', html.includes('renderKQ'));
check('智能推荐器', html.includes('recommend('));
check('数据源数组', html.includes('var SRCS='));
check('标题终极版', html.includes('终极版'));

console.log(`\n结果: ${pass} 通过 / ${fail} 失败`);
