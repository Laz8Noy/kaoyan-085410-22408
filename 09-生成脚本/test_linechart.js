const fs = require('fs');
const file = process.argv[2];
const html = fs.readFileSync(file, 'utf8');
const script = html.match(/<script>([\s\S]*)<\/script>/)[1];

const dataStart = script.indexOf('var S=[');
const dataEnd = script.indexOf('// ===== 工具函数', dataStart);
eval(script.slice(dataStart, dataEnd));
function esc(s){return String(s==null?"—":s);}

// DOM 桩
const els = {};
function el(id){ if(!els[id]) els[id] = {innerHTML:'', value:0, addEventListener(){}, textContent:''}; return els[id]; }
global.document = { getElementById: el };

const lineStart = script.indexOf('// ===== 图5');
const lineEnd = script.indexOf('// ===== 统计', lineStart);
eval(script.slice(lineStart, lineEnd));

const chart = el('line-chart').innerHTML;
const sel = el('line-school').innerHTML;
console.log('折线图渲染: SVG =', chart.indexOf('<svg') >= 0, '| 长度 =', chart.length);
console.log('下拉选项数:', (sel.match(/<option/g) || []).length);
console.log('含国家线虚线:', chart.indexOf('stroke-dasharray') >= 0);
console.log('含年份2026:', chart.indexOf('2026') >= 0);
