const fs = require('fs');
const file = process.argv[2];
const html = fs.readFileSync(file, 'utf8');
const script = html.match(/<script>([\s\S]*)<\/script>/)[1];

const dataStart = script.indexOf('var S=[');
const dataEnd = script.indexOf('// ===== 工具函数', dataStart);
eval(script.slice(dataStart, dataEnd));

function esc(s){return String(s==null?"—":s);}
const els = {};
function el(id){ if(!els[id]) els[id] = {innerHTML:'', value:0, addEventListener(){}, textContent:''}; return els[id]; }
global.document = { getElementById: el };

const kqStart = script.indexOf('// ===== 2026 考情明细');
const kqEnd = script.indexOf('// ===== 热度榜', kqStart);
if (kqStart < 0 || kqEnd < 0) { console.error('FAIL: 考情明细 JS 段定位失败'); process.exit(1); }
eval(script.slice(kqStart, kqEnd));

const box = el('kq-box').innerHTML;
const cards = (box.match(/class="kq-card"/g) || []).length;
const hasLink = box.indexOf('查看来源') >= 0;
const hasScope = box.indexOf('kq-scope') >= 0;
const hasVerified = box.indexOf('kq-tag') >= 0;
console.log('考情卡片数:', cards);
console.log('含来源链接:', hasLink, '| 含口径:', hasScope, '| 含核实状态:', hasVerified);
console.log('含贵州大学:', box.indexOf('贵州大学') >= 0, '| 含天津工业:', box.indexOf('天津工业大学') >= 0);
