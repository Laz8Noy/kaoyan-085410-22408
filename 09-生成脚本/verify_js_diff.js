// 精确验证：模板 vs 终极版 的 script 内容是否一致（排除注入破坏）
const fs = require('fs');
const tpl = '<SOURCE_DIR>/02_院校数据_原有/全国408_085410双非热度版_20260820.html';
const fin = '<SOURCE_DIR>/02_院校数据_原有/全国408_085410双非热度版_终极版_20260824.html';

function getScript(p) {
  const h = fs.readFileSync(p, 'utf8');
  const m = h.match(/<script>([\s\S]*?)<\/script>/);
  return m ? m[1] : null;
}
const jsTpl = getScript(tpl);
const jsFin = getScript(fin);
console.log('模板 script 长度:', jsTpl ? jsTpl.length : 'null');
console.log('终极版 script 长度:', jsFin ? jsFin.length : 'null');

// 模板 script 本身能否解析（如果模板也报错，说明是提取方式问题）
try {
  new Function(jsTpl);
  console.log('模板 JS 解析: ✅');
} catch (e) {
  console.log('模板 JS 解析: ❌', e.message.slice(0, 120));
}
try {
  new Function(jsFin);
  console.log('终极版 JS 解析: ✅');
} catch (e) {
  console.log('终极版 JS 解析: ❌', e.message.slice(0, 120));
}

// 对比差异位置
if (jsTpl && jsFin && jsTpl !== jsFin) {
  for (let i = 0; i < Math.max(jsTpl.length, jsFin.length); i++) {
    if (jsTpl[i] !== jsFin[i]) {
      console.log('\n首个差异 @', i);
      console.log('模板:', jsTpl.slice(i - 80, i + 80));
      console.log('终极:', jsFin.slice(i - 80, i + 80));
      break;
    }
  }
}
