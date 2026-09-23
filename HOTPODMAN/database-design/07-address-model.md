# 07 — ที่อยู่บริษัท สาขา และ Supplier

สถานะ: แบบฐานข้อมูลที่ปรับตามบรีพ วันที่ 23 กันยายน 2026 ยังไม่ได้สร้างตารางหรือนำเข้าข้อมูลพื้นที่จริง

## 1. ตารางและ ID

| ตารางกลาง | Primary key | ข้อมูลและความสัมพันธ์ |
|---|---|---|
| geo.provinces | id UUID | official_code, name_th, name_en; จังหวัด/กรุงเทพมหานคร |
| geo.districts | id UUID | province_id FK; official_code; อำเภอ/เขต |
| geo.subdistricts | id UUID | district_id FK; official_code; ตำบล/แขวง |
| geo.postal_codes | id UUID | code text unique เป็นเลข 5 หลัก |
| geo.subdistrict_postal_codes | id UUID | subdistrict_id + postal_code_id unique; คู่พื้นที่ที่อนุญาต |

ใช้ UUID ภายในระบบแยกจากรหัสพื้นที่ทางการและรหัสไปรษณีย์ ซึ่งเก็บเป็นข้อความ ตาราง geo เป็น reference กลางร่วมทุกบริษัท ไม่มี company_id; ผู้ใช้ทั่วไปอ่านได้ตามสิทธิ์ แต่แก้ไขไม่ได้ ทุกตารางมี active, source_ref, source_version และ timestamps เพื่อทราบแหล่งข้อมูล

การออกแบบ mapping รองรับหลายรหัสไปรษณีย์ต่อตำบลและหลายตำบลต่อรหัสไปรษณีย์ ไม่กำหนดว่าแต่ละตำบลต้องมีรหัสเดียว coverage_note ใช้อธิบายข้อจำกัดพื้นที่ย่อย หากมีเงื่อนไขต้องตรวจที่อยู่รายละเอียดก่อนยืนยัน

## 2. ฟิลด์ที่อยู่ที่ต้องมี

org.companies ใช้เป็นที่อยู่จดทะเบียน, org.branches ใช้เป็นที่อยู่สาขา และ catalog.supplier_addresses ใช้แยกชนิดที่อยู่ Supplier เช่นจดทะเบียน/ติดต่อ/จัดส่ง โดยทุก row มี id UUID ของตัวเองอยู่แล้ว

| ฟิลด์ | ชนิด | บังคับ | ความหมาย |
|---|---|---|---|
| address_line1 | text | ใช่ | บ้านเลขที่ อาคาร ชั้น ห้อง หมู่ ซอย ถนน ตามที่มี; ห้ามข้อความว่าง |
| address_line2 | text | ไม่ | รายละเอียดเพิ่มเติม |
| province_id | UUID FK | ใช่ | จังหวัด |
| district_id | UUID FK | ใช่ | อำเภอ/เขต |
| subdistrict_id | UUID FK | ใช่ | ตำบล/แขวง |
| postal_code_id | UUID FK | ใช่ | รหัสไปรษณีย์ |

ฟิลด์ชุดนี้แทน address JSON เดิมของ master ทั้งสามจุด โดยตั้งใจใช้ address value object รูปแบบเดียวกันใน DTO/service การเก็บชื่อพื้นที่ไว้ใน master ซ้ำไม่ใช่แหล่งข้อมูลหลัก API สามารถคืนทั้ง id และชื่อที่ join แล้วให้ frontend แสดงผล

ขอบเขตชุดนี้คือที่อยู่ในประเทศไทย ถ้าต้องมี Supplier ต่างประเทศต้องเพิ่ม country/address variant อย่างชัดเจนก่อนเปิดใช้ ไม่ใส่ UUID ไทยสมมติเพื่อให้ผ่าน validation

## 3. บังคับความสัมพันธ์ในฐานข้อมูล

นอกจาก FK ไปแต่ละตาราง ต้องสร้าง composite constraints ใน migration จริง:

- districts UNIQUE(province_id,id); address FK(province_id,district_id) อ้างอิงคู่นี้
- subdistricts UNIQUE(district_id,id); address FK(district_id,subdistrict_id) อ้างอิงคู่นี้
- subdistrict_postal_codes UNIQUE(subdistrict_id,postal_code_id); address FK(subdistrict_id,postal_code_id) อ้างอิงคู่นี้
- ใช้ NO ACTION/RESTRICT ไม่ cascade delete ที่อยู่บริษัทหรือเอกสารเมื่อแก้ reference
- FK รับประกันความสัมพันธ์ ส่วน active/coverage ตรวจ service หรือ DB trigger ที่เขียนเฉพาะงาน; การ retire reference และสร้าง/เปลี่ยนที่อยู่ต้องล็อก reference ที่เกี่ยวข้องด้วยลำดับเดียวกันเพื่อป้องกัน race
- ตรวจ active ทุกระดับเฉพาะเมื่อสร้าง/เปลี่ยนที่อยู่ การ retire ไม่ทำให้เอกสารเก่าเสียหรือบังคับย้ายข้อมูลเงียบ ๆ; การออกเอกสารใหม่จากที่อยู่ที่ retire แล้วต้องแก้ master ก่อน
- ห้ามแก้ parent หรือ code ของ reference ที่ใช้แล้วเพื่อสื่อถึงพื้นที่ใหม่ ใช้ record ใหม่และ retire record เดิม; ชื่อสะกดแก้ได้โดยมี audit

catalog FK ใน data dictionary แสดงรายคอลัมน์; composite constraints ข้างต้นเป็นข้อกำหนดเพิ่มเติมที่ต้องทำใน migration ห้ามถือว่า FK เดี่ยวเพียงพอ

## 4. Flow หน้าจอและสำนักงานใหญ่

เลือกจังหวัด → โหลดอำเภอของจังหวัดนั้น → โหลดตำบลของอำเภอนั้น → โหลดรหัสไปรษณีย์ที่เลือกได้ของตำบล หากมีตัวเลือกเดียวจึงเลือกอัตโนมัติ เมื่อเปลี่ยนพื้นที่ระดับบนต้องล้าง ID ระดับล่างที่ไม่สัมพันธ์ Backend ตรวจทุกครั้งแม้ frontend มี dropdown แล้ว

สร้างบริษัทต้องส่งที่อยู่ครบ และสร้างสำนักงานใหญ่ด้วยสำเนาที่อยู่บริษัทเป็นค่าเริ่มต้นใน transaction เดียวพร้อมคลังหลัก ที่อยู่สำนักงานใหญ่แก้ภายหลังได้ตามสิทธิ์โดยไม่เปลี่ยนที่อยู่จดทะเบียนบริษัทอัตโนมัติ ข้อห้ามลบ/ปิดสำนักงานใหญ่ยังคงเดิม

## 5. ประวัติเอกสารและข้อมูลเดิม

PO revision เก็บ buyer_snapshot, supplier_snapshot และ shipping_snapshot โดยรวมรายละเอียดที่อยู่, ID พื้นที่, ชื่อพื้นที่, รหัสไปรษณีย์ที่แสดง และ source_version ณ เวลาออกเอกสาร การเปลี่ยน master/reference ไม่ทำให้เอกสารที่ออกแล้วเปลี่ยนตาม ห้าม render PO เก่าด้วยชื่อปัจจุบันจาก geo เพียงอย่างเดียว

ย้ายข้อมูลเก่าผ่าน staging แยกจาก master: เก็บ raw address, ผล mapping และปัญหาที่ต้องตรวจ รายการกำกวมค้างใน staging จนแก้ครบก่อนเปิดใช้งานจริง ไม่มีการสร้างพื้นที่ “ไม่ทราบ” ให้ผ่าน FK

## 6. การตรวจรับ

ทดสอบ valid address, missing IDs, blank address_line1, wrong province/district, wrong district/subdistrict, invalid postal mapping, inactive reference, เขต/แขวง, concurrent retire, HQ provisioning rollback และ snapshot ไม่เปลี่ยนตาม master บน PostgreSQL จริงก่อน Production

ดู [Data dictionary](02-data-dictionary.md) และ [ERD ที่อยู่](erd/10-addresses.svg)
