"""Generate COMMENT statements and index inventory; never execute SQL."""
from pathlib import Path
import json
R=Path(__file__).resolve().parents[1]
ts=json.loads((R/'model.catalog.json').read_text())['tables']
def literal(s):return "'"+s.replace("'","''")+"'"
def ident(s):return '.'.join('"'+p+'"' for p in s.split('.'))
out=['-- DESIGN ONLY: apply only after reviewed migrations create the matching schema.', '-- This file creates no tables, keys or indexes and has NOT been executed.', 'BEGIN;']
for t in ts:
 out.append(f"COMMENT ON TABLE {ident(t['name'])} IS {literal(t['comment_th'])};")
 for c in t['columns']:
  out.append(f"COMMENT ON COLUMN {ident(t['name']+'.'+c['name'])} IS {literal(c['comment_th'])};")
out+=['COMMIT;','']
(R/'comments.th.sql').write_text('\n'.join(out))
lines=['# 09 — บัญชี PK / Unique / Index รายตาราง','',
'สถานะ: ข้อกำหนดออกแบบ ไม่ใช่ผลตรวจ Index ใน PostgreSQL จริง ยังไม่มี migration หรือ EXPLAIN ANALYZE', '',
'ทุกตารางมี PK(id) เป็น UUID; U หมายถึง Unique และ I หมายถึง Index ที่ระบุในแบบ ตาราง tenant ต้องเพิ่ม UNIQUE(company_id,id) สำหรับ composite FK ด้วย แม้ไม่ได้พิมพ์ซ้ำในช่อง Candidate ด้านล่าง', '',
'Unique/PK สร้างดัชนีรองรับเมื่อสร้าง constraint จริง แต่ FK ไม่สร้าง index ฝั่งลูกอัตโนมัติ ห้ามสรุปว่ามี FK แล้ว query จะเร็ว ส่วน FK ที่ยังไม่มีดัชนีตรงรูปแบบ query ต้องประเมินจาก workload ไม่เพิ่มทุกคอลัมน์โดยอัตโนมัติ', '',
'ค่าด้านล่างเป็น notation ไม่ใช่ SQL ที่รันได้; NULLS NOT DISTINCT, partial predicates, expression indexes และคอลัมน์ซ้ำใน composite ต้องลง migration และตรวจชื่อ/ชนิด/ลำดับจริง', '',
'| ตาราง | PK | Unique / Index ที่ออกแบบไว้ | FK ที่ต้องตรวจแผน query ฝั่งลูก |', '|---|---|---|---|']
for t in ts:
 fks=', '.join(c['name'] for c in t['columns'] if c['reference']) or 'ไม่มี'
 lines.append(f"| `{t['name']}` | `id UUID` | {t['keys']} | {fks} |")
lines+=['','## งานที่ต้องทำก่อนยืนยันเป้าหมาย GET 25 รายการ / 50 ms','',
'- หน้า products เรียง created_at DESC, id DESC: ประเมิน partial B-tree (company_id,created_at DESC,id DESC) WHERE deleted_at IS NULL; active filter ต้องวัดก่อนเลือกเพิ่ม active ใน key ไม่สร้างคู่ซ้ำโดยไม่มีเหตุผล',
'- หน้า suppliers: ประเมินรูปแบบเดียวกับ products เมื่อ query มี deleted_at IS NULL และเรียงด้วย created_at/id',
'- หน้า PO: กรองบริษัท/สาขา/ชนิด/สถานะผ่าน platform.documents แล้ว join purchase_orders; ต้อง EXPLAIN ทั้ง query และตรวจว่ารายการจำกัด 25 header ก่อนโหลดรายละเอียด ห้ามสรุปจาก index บน po_id เพียงตัวเดียว',
'- ค้นหา contains ชื่อสินค้า: B-tree ทั่วไปไม่พอสำหรับทุก pattern; ประเมิน trigram/รูปแบบค้นหาจากข้อมูลภาษาไทยและ selectivity จริง',
'- FK ที่ใช้ join/filter หรือเช็ค parent deletion บ่อย: ตรวจ leftmost columns ของดัชนีที่มีอยู่ก่อนเพิ่ม composite index; ดัชนีเริ่ม company_id ใช้เมื่อ query มีขอบเขตบริษัท ไม่เทียบเท่า index UUID เดี่ยวสำหรับงานข้ามบริษัท',
'- ทดสอบ authorization, RLS, count totals, sort/filter และ deep pagination พร้อม EXPLAIN (ANALYZE, BUFFERS) ใน UAT ข้อมูลใกล้จริง; p95 Backend response <50 ms เป็นเป้าหมายที่ยังไม่พิสูจน์',
'- ก่อน Production ตรวจ pg_indexes/pg_constraint จริงและเก็บ DDL + query plan; รายงานดัชนีซ้ำ/ไม่ถูกใช้และผลกระทบต่อการเขียนด้วย', '',
'อ้างอิง: [PostgreSQL constraints](https://www.postgresql.org/docs/18/ddl-constraints.html)', '']
(R/'09-index-inventory.md').write_text('\n'.join(lines))
print(f'Generated {len(ts)} table and {sum(len(t["columns"]) for t in ts)} column comments, plus index inventory')
