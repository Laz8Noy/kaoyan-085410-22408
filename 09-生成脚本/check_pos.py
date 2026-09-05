# -*- coding: utf-8 -*-
import io
p = r'<SOURCE_DIR>\02_院校数据_原有\全国408_085410双非热度版_终极版_20260824.html'
h = io.open(p, encoding='utf-8').read()
s = h.find('<script>')
e = h.find('</script>')
gk = h.find('id="gaikao"')
mt = h.find('id="mentors"')
kq = h.find('<section id="kq"')
print('script 位置:', s, '-', e)
print('gaikao:', gk, '| mentors:', mt, '| kq:', kq)
print('新区块在 script 之前?', gk < s and mt < s and kq < s)
print('script 后仍有 detail/other408?', h.find('id="detail"') > e, h.find('id="other408"') > e)
print('文件总长:', len(h))
