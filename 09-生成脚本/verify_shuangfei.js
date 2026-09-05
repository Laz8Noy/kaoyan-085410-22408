const fs = require('fs');
const file = process.argv[2];
const html = fs.readFileSync(file, 'utf8');
const m = html.match(/<script>([\s\S]*)<\/script>/);
if (!m) { console.error('FAIL: 未找到 script 块'); process.exit(1); }
const script = m[1];

// 语法检查（仅解析，不执行）
try {
  new Function(script);
  console.log('整段 JS 语法: OK');
} catch (e) {
  console.error('FAIL: 整段 JS 语法错误 ->', e.message);
  process.exit(1);
}

// 数据段（无 DOM 依赖）：var S/C/K/O/SRCS
const dataStart = script.indexOf('var S=[');
const dataEnd = script.indexOf('// ===== 工具函数', dataStart);
if (dataStart < 0 || dataEnd < 0) { console.error('FAIL: 数据段定位失败'); process.exit(1); }
const dataChunk = script.slice(dataStart, dataEnd);
try {
  eval(dataChunk);
} catch (e) {
  console.error('FAIL: 数据段语法错误 ->', e.message);
  process.exit(1);
}

const names = S.concat(C).map(d => d.n);
const need = ['天津工业大学', '吉首大学', '华中师范大学', '中国矿业大学（徐州）', '河南大学', '郑州大学', '上海大学', '苏州大学', '福州大学', '暨南大学', '西南大学'];
const missing = need.filter(n => !names.includes(n));
const needK = ['天津工业大学', '吉首大学', '华中师范大学', '中国矿业大学（徐州）', '中国石油大学（华东）', '宁夏大学', '北京交通大学', '云南大学', '江苏海洋大学', '安庆师范大学', '新疆农业大学', '重庆科技大学', '湖南科技大学'];
const kMissing = needK.filter(n => (K[n] || '') !== '22408');
const lhNeed = ['华北理工大学', '河北大学', '内蒙古工业大学', '大连海洋大学', '常州大学', '安徽工程大学', '苏州大学', '中国石油大学（华东）', '华中农业大学', '广西大学', '暨南大学'];
const lhMissing = lhNeed.filter(n => !S.concat(C).some(d => d.n === n && d.lh && d.lh.length === 3));

console.log('S.length =', S.length, '| C.length =', C.length, '| O.length =', O.length, '| SRCS.length =', SRCS.length);
console.log('新增院校缺失:', missing.length === 0 ? '无 ✓' : missing.join(','));
console.log('K=22408 校验缺失:', kMissing.length === 0 ? '无 ✓' : kMissing.join(','));
console.log('lh 历年线缺失:', lhMissing.length === 0 ? '无 ✓' : lhMissing.join(','));
const lhSample = S.concat(C).filter(d => d.lh && d.lh.length === 3).map(d => d.n + ':' + d.lh.join('/'));
console.log('lh 样例:', lhSample.slice(0, 8).join(' | '));
// 折线图数据筛选逻辑
const lineMap = {};
S.concat(C).forEach(function(d){
  const pts = (d.lh || [null,null,null]).concat([d.l]);
  const cnt = pts.filter(v => v != null).length;
  if (cnt < 2) return;
  const cur = lineMap[d.n];
  if (!cur || cnt > cur.cnt) lineMap[d.n] = {n:d.n, cnt:cnt};
});
console.log('折线图可选学校数:', Object.keys(lineMap).length);
console.log('exKey(天津工业大学) =', exKey(S.find(d => d.n === '天津工业大学')));
console.log('exKey(湖南科技大学) =', exKey(S.find(d => d.n === '湖南科技大学')));
console.log('exKey(华中师范大学) =', exKey(C.find(d => d.n === '华中师范大学')));
const zz = C.find(d => d.n === '郑州大学');
console.log('郑州大学 rr =', zz.rr, '| 线 =', zz.l);
const rk = S.find(d => d.n === '湖南科技大学');
console.log('湖南科技 ratio =', rk.ratio);
// 报录比/复录比非空统计
const ratioCnt = S.filter(d => d.ratio != null).length;
const rrCnt = S.filter(d => d.rr != null).length;
console.log('S中有报录比数据:', ratioCnt, '| 有复录比数据:', rrCnt);
