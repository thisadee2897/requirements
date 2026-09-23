# 08 — ข้อกำหนด PK, FK, Type, เวลา และ Comment

สถานะ: Design contract ต้องนำไปสร้างและทดสอบใน migration จริง ไม่ใช่ผลยืนยันฐานข้อมูล Production

## 1. คำอธิบายภาษาไทย

ทุกตารางมี comment_th ระบุว่าหนึ่งแถวเก็บอะไร ทุกคอลัมน์มี comment_th อธิบายความหมาย ชนิดข้อมูลและหน่วยเมื่อเกี่ยวข้อง อ่านได้ใน [Data dictionary](02-data-dictionary.md) หรือ [model catalog](model.catalog.json)

[comments.th.sql](comments.th.sql) มี COMMENT ON TABLE และ COMMENT ON COLUMN ครบ สร้างซ้ำด้วย tools/build_comments.py ไฟล์นี้ไม่ได้สร้างตาราง/PK/FK/Index และยังไม่ได้ execute ต้องใช้หลัง migration สร้างชื่อ schema/table/column ตรงกันเท่านั้น เมื่อเพิ่มคอลัมน์ใหม่ generator ต้อง fail หากไม่มีคำอธิบายไทย

## 2. PK และ FK

- ทุกตารางใช้ id UUID NOT NULL PRIMARY KEY; รหัสบริษัท รหัสสินค้า เลข PO และรหัสพื้นที่ทางการเป็น business key แยกจาก PK ไม่เปลี่ยน UUID ตามการเปลี่ยนชื่อหรือรหัสธุรกิจ
- Tenant table มี company_id NOT NULL และ UNIQUE(company_id,id); FK ไปตาราง tenant ต้องเป็น (company_id,parent_id) → (company_id,id) พร้อม type ตรงกัน ป้องกันอ้างอิงข้ามบริษัท
- FK ไป global tables เช่น geo/users/permissions ใช้ UUID ของตารางนั้น; การมี FK ไป user ไม่ได้แทนการตรวจสิทธิ์สมาชิกบริษัท
- parent_id ที่ nullable อนุญาตไม่มีความสัมพันธ์ได้ แต่เมื่อมีค่าต้องตรวจ composite scope ครบ company_id ไม่ nullable; ห้ามใช้ MATCH FULL กับคู่ company_id + optional parent_id โดยไม่ทบทวน semantics
- คอลัมน์ UUID บางตัว เช่น correlation_id, aggregate_id, internal_id และ target_id เป็นรหัสเหตุการณ์หรือ mapping ไม่ใช่ FK อัตโนมัติ Data dictionary แยก PK/FK ชัดเจน; mapping หลายชนิดต้องมี allowlist resolver ไม่ใช้แทน FK หลักของธุรกิจ
- Referential actions เป็น RESTRICT/NO ACTION ตาม transaction ที่ออกแบบ; ห้าม cascade ลบเอกสาร/ledger/audit; exact-one HQ/default warehouse ใช้ deferred constraint trigger ร่วม unique ตามเอกสาร 03
- ต้องตรวจ composite FK เพิ่มเติมสำหรับที่อยู่ตามเอกสาร 07 และความสัมพันธ์ lot/product, package/lot, warehouse/branch และเอกสารแม่/ลูกตามเอกสาร 03

## 3. PostgreSQL Type และ Prisma mapping

| ข้อมูล | PostgreSQL | ข้อกำหนด implementation |
|---|---|---|
| PK/FK | uuid | Prisma String @db.Uuid; ไม่ใช้ text สำหรับ UUID FK |
| เวลาเหตุการณ์ | timestamptz | Prisma DateTime @db.Timestamptz(3); precision มิลลิวินาทีเป็น baseline สำหรับ API JS |
| วันที่ธุรกิจ | date | Prisma DateTime @db.Date; API date-only string; adapter ห้ามแปลง timezone จนวันเปลี่ยน |
| เงินรวม THB | numeric(20,2) | Prisma Decimal @db.Decimal(20,2); API string |
| ราคา ต้นทุน น้ำหนัก จำนวนละเอียด | numeric(20,6) | Decimal; ตรวจ scale ก่อนเขียน ไม่ยอมให้ปัดเงียบ |
| อัตราแปลง | numeric(24,9) | Decimal; ห้ามใช้ JS float |
| อัตราร้อยละ | numeric(9,6) | 0..100 เมื่อเป็น percentage; กำหนด CHECK ตามความหมายจริง |
| จำนวนครั้ง/ลำดับทั่วไป | integer | ต้องกำหนดช่วงและ CHECK เช่นไม่ติดลบตามบริบท |
| เลข running/ขนาดข้อมูลมาก | bigint | API decimal string เมื่ออาจเกิน JS safe integer |
| สถานะใช้งาน | boolean | true/false จริง ไม่ใช่ข้อความ |
| รหัสไปรษณีย์/ภาษี/โทรศัพท์/บาร์โค้ด | text | รักษาศูนย์นำหน้า ตรวจ pattern/ความยาว |
| สกุลเงิน | char(3) | รหัสสกุลเงินที่อนุญาต ไม่รวมยอดต่างสกุลโดยไม่แปลง |
| เนื้อหา snapshot/config | jsonb | ตรวจ schema/version/size และสิทธิ์; ไม่ใช้เก็บ PK/FK/เงินหลักแทนคอลัมน์ |
| IP | inet | แยกข้อมูล IP ออกจากข้อความ user-agent |

ความหมายของ value ที่เป็น JSON คือค่าการตั้งค่า ส่วน value ที่เป็น numeric คือมูลค่า ไม่ตีความจากชื่อคอลัมน์เพียงอย่างเดียว Type ใน dictionary เป็นชนิดหลัก ส่วน precision เวลาให้ใช้ข้อกำหนด timestamptz(3) ใน migration ทุกจุดอย่างสม่ำเสมอ

## 4. วันที่และ timezone

- ตั้ง DB session/connection และ server logs เป็น UTC เก็บเวลาเหตุการณ์ด้วย timestamptz ส่ง API ISO 8601 เช่น 2026-09-23T06:30:00.000Z
- UI แสดงเวลาเดียวกันเป็น 23 กันยายน 2569 13:30:00 ใน Asia/Bangkok ห้ามบวก 7 ชั่วโมงก่อนบันทึกซ้ำอีกครั้ง
- timestamptz เก็บ instant ไม่เก็บชื่อ timezone เดิม จึงใช้ org.companies.timezone เป็น IANA timezone ของธุรกิจ ตรวจชื่อจาก allowlist ที่ runtime รองรับ; baseline Asia/Bangkok
- การเปลี่ยน timezone บริษัทต้องมีสิทธิ์และ audit; เอกสารที่ยืนยันแล้วเก็บ timezone ใน settings/policy snapshot ที่เกี่ยวข้อง เพื่อรายงาน/พิมพ์ประวัติด้วยกฎเดิม ไม่คำนวณย้อนจาก timezone ใหม่
- order_date และ requested_delivery_date เป็น date ส่ง YYYY-MM-DD ใช้ปี ค.ศ. ใน DB/API การแสดง พ.ศ. ทำเฉพาะ UI; fiscal_year ต้องกำหนดให้เก็บ ค.ศ. แล้ว format เลขเอกสาร พ.ศ. ตามนโยบายที่ snapshot
- Input เวลาเหตุการณ์ต้องมี Z หรือ offset; ปฏิเสธ datetime ที่ไม่มี timezone ไม่ตีความจาก timezone เครื่อง frontend โดยเดา
- ตัวอย่างช่วงรายงานวันที่ 2026-09-24 กรุงเทพฯ ใช้ UTC >=2026-09-23T17:00:00Z และ <2026-09-24T17:00:00Z; ใช้ช่วงครึ่งเปิด ไม่ใช้ 23:59:59 และไม่แปลง column ทุกแถวใน WHERE จนดัชนีใช้ไม่ได้
- created_at คือเวลาสร้างแถว, occurred_at คือเวลาเกิดเหตุการณ์, effective_at คือเวลามีผลทางธุรกิจ, posted_at คือเวลาลงรายการ; ห้ามสลับใช้ในการตัดยอด
- now() default ของ updated_at ไม่ได้ทำให้อัปเดตอัตโนมัติเมื่อ UPDATE ต้องให้ทุกช่องทางเขียนอัปเดต หรือกำหนด trigger กลาง รวม raw SQL/worker ด้วย
- สินค้าที่ฉลากระบุแค่วันผลิต/หมดอายุ: เก็บหลักฐานวันต้นฉบับและนโยบาย timezone ใน snapshot/source evidence; แปลงเป็น instant ตาม policy ที่กำหนด ไม่สร้างเวลาเดาแบบไม่มีหลักฐาน หากนโยบายหมดอายุเมื่อสิ้นวัน ให้ใช้เที่ยงคืนวันถัดไปเป็น exclusive expiry

## 5. เกณฑ์ตรวจรับฐานข้อมูลจริง

1. pg_constraint ยืนยัน PK ทุกตาราง, FK ครบรวม composite และ type ตรงกัน; ทดสอบ tenant ผิด/parent ผิด/NULL ผิดต้องถูกปฏิเสธ
2. pg_description ต้องมีคำอธิบายไทยที่ตรง catalog ทุกตารางและทุกคอลัมน์ที่อยู่ใน migration ของเฟสนั้น
3. pg_indexes เทียบกับ [Index inventory](09-index-inventory.md) พร้อม query plan และเหตุผลของดัชนีที่เพิ่ม/ไม่เพิ่ม
4. ทดสอบ round-trip UTC/Asia/Bangkok, รอยต่อวัน/ปี, date-only, input ไม่มี offset, ปี ค.ศ./พ.ศ. และ timezone snapshot
5. ทดสอบ Decimal precision/range, JSON schema, soft delete, uniqueness, concurrent create/update และ raw SQL updated_at
6. เก็บผลทดสอบ PostgreSQL จริงแยกจากการ validate เอกสาร ห้ามรายงานผลเอกสารเป็น migration/performance ผ่าน

อ้างอิง: [PostgreSQL Date/Time](https://www.postgresql.org/docs/18/datatype-datetime.html) และ [Constraints](https://www.postgresql.org/docs/18/ddl-constraints.html)
