# HOTPOTMAN — Database Design ทั้งระบบ

**ฉบับออกแบบ 1.0 · 23 กันยายน 2569 · PostgreSQL + Prisma · ยังไม่ใช่ Migration พร้อม Deploy**

แบบนี้ครอบคลุม HOTPOTMAN ตามบรีพและคำแก้ไขล่าสุด: จัดซื้อเอง ดูแลสินค้า/Supplier เอง สำนักงานใหญ่อัตโนมัติ การยืนยันส่งมอบก่อนชั่งรับเข้าคลัง และงานคลังต่อเนื่องทั้งหมด ไม่รวมการสร้าง POS, HR, CRM หรือบัญชีแยกประเภทเต็มระบบ

## เปิดอ่านตามลำดับ

| ไฟล์ | ใช้ทำอะไร |
|---|---|
| [01-architecture-and-erd.md](01-architecture-and-erd.md) | ภาพรวม ขอบเขตเจ้าของข้อมูล ความสัมพันธ์ และ ER Diagram แยกกลุ่ม |
| [02-data-dictionary.md](02-data-dictionary.md) | รายละเอียด 128 ตาราง 1,481 คอลัมน์ พร้อมชนิดข้อมูล NULL, FK, Unique/Index และกฎเฉพาะ |
| [03-invariants-and-transactions.md](03-invariants-and-transactions.md) | สมการยอด สถานะเอกสาร Tenant, Transaction, Lock, Reversal และความถูกต้องของข้อมูล |
| [04-migration-and-acceptance.md](04-migration-and-acceptance.md) | ลำดับสร้าง Migration ตามเฟส การย้ายระบบ และกรณีทดสอบตรวจรับ |
| [05-reports-and-decisions.md](05-reports-and-decisions.md) | รายงาน/View ฐานคำนวณราคา ตัวกรอง Dashboard และประเด็นที่ต้องยืนยันก่อนลง Migration |
| [06-state-machines.md](06-state-machines.md) | สถานะและ transition ที่อนุญาตของเอกสารและงานเบื้องหลัง |
| [VALIDATION.md](VALIDATION.md) | ผลตรวจเอกสารและขอบเขตที่ยังไม่ได้ทดสอบกับฐานข้อมูลจริง |
| [model.catalog.json](model.catalog.json) | รายการตาราง/คอลัมน์/ความสัมพันธ์ที่เครื่องมือตรวจอ่านได้ เป็น catalog ไม่ใช่ schema ที่ deploy ได้ |
| [tools/build_catalog.py](tools/build_catalog.py) | สร้าง catalog และ Data Dictionary ซ้ำได้ ไม่เชื่อมต่อฐานข้อมูล |
| [tools/validate_design.py](tools/validate_design.py) | ตรวจความสอดคล้องของ catalog/ERD/ไฟล์เอกสาร ไม่ใช่ database integration test |

## หลักที่ล็อกตามคำสั่งล่าสุด

1. สร้างบริษัทต้องได้สำนักงานใหญ่หนึ่งแห่งและคลังหลักพร้อมกัน สำนักงานใหญ่ลบ/ปิดใช้งานไม่ได้
2. ทุกสาขามีคลังหลักลบไม่ได้; location ใช้เมื่อเฟสคลังเริ่มทำงาน
3. HOTPOTMAN เป็นเจ้าของ Master และ PO; ERP เป็นปลายทางเชื่อมต่อได้ ไม่เป็นเงื่อนไขก่อนซื้อ
4. **Delivery Confirmation ไม่สร้าง Stock Movement** และไม่ทำให้สินค้าเบิกได้
5. **Warehouse Receipt หลังชั่ง** จึงสร้าง Lot/Package และ Stock Movement ใน transaction เดียว
6. ยอดค้างส่งมอบ ยอดยืนยันแล้วรอเข้าคลัง และยอดสต็อกพร้อมใช้เป็นคนละยอด
7. การเปลี่ยนราคา/หน่วย/กฎปัจจุบันไม่ย้อนเปลี่ยนเอกสารเก่า
8. รายการที่ยืนยันแล้วไม่ลบทิ้ง ใช้ reversal และเก็บสายอ้างอิงต้นทาง
9. รายงานและ Dashboard ใช้ฐานข้อมูล/นิยามเดียวกันและเคารพสิทธิ์บริษัท/สาขา/คลัง

## เอกสารต้นทางและการแก้ความขัดแย้ง

ลำดับหลักฐาน: คำยืนยันผู้ใช้ในบทสนทนาล่าสุด → [แผน Phase 1](../phase1_work_plan_24-30_sep_2026.md) → [Backend Foundation Prompt](../backend_foundation_implementation_prompt.md) → [requirements.md](../requirements.md) และ [technical.md](../technical.md) สำหรับงานคลัง/บรีพเดิมที่ยังไม่ถูกแก้

| บรีพเก่า | แบบนี้ใช้ข้อสรุปล่าสุด |
|---|---|
| ERP สร้าง PO/ดูแล Master และใช้ ERP ID เป็น PK | สร้างใน HOTPOTMAN, UUID ภายใน; external mappings เก็บ ERP/legacy IDs |
| TypeORM | Prisma สำหรับ CRUD และ SQL สำหรับกฎ/รายงานที่จำเป็น |
| “รับสินค้า” ขั้นเดียวแล้วเพิ่มสต็อก | แยก Delivery Confirmation กับ Warehouse Receipt อย่างเด็ดขาด |
| งานคลังทั้งหมดตามกำหนด 60 วันเดิม | แบ่งเป็น F/P/W/O/R ในแบบนี้; ไม่รับรองวันส่งมอบเฟสหลังจากแบบออกแบบ |

เอกสารต้นทางเดิมยังไม่ได้แก้ทับ ให้ใช้เอกสารนี้ร่วมกับ Phase 1/Prompt เมื่อลงมือ ไม่นำข้อความ ERP-owned เก่ากลับมาเป็นข้อกำหนดใหม่

## ความครบและข้อจำกัด

แบบนี้เป็น logical/physical design specification ครบโดเมนที่อยู่ในบรีพ พร้อมทิศทาง constraints/index/transactions แต่ **ยังไม่มี Prisma schema, migration SQL, DB instance หรือข้อมูลจริง** จึงยังไม่อ้างว่า migration, concurrency หรือ performance ผ่านแล้ว

นโยบายต้นทุน หน่วยสินค้าที่เป็นน้ำหนักแปรผัน รายละเอียดการชั่งหลายรอบ และการเปลี่ยนสถานะการอนุมัติบางกรณีมีข้อเสนอเริ่มต้นและจุดยืนยันใน [05](05-reports-and-decisions.md) ไม่ได้ทำให้กฎที่ผู้ใช้ยืนยันแล้วกลายเป็นคำถามใหม่

128 ตารางเป็นขอบเขตออกแบบทั้งระบบ มีตารางหลัก/ตารางรายการ/ประวัติ/สิทธิ์/โครงสร้างกลางรวมกัน ไม่ใช่ 128 หน้าจอหรือ 128 Microservices และไม่ต้องสร้างทุกตารางใน Phase 1

รายละเอียดที่อยู่แบบมี ID: [07-address-model.md](07-address-model.md) และ [ERD ที่อยู่](erd/10-addresses.svg) ครอบคลุมบริษัท สาขา และ Supplier

## คำอธิบายไทยและความถูกต้องของฐานข้อมูล

- [08 — PK / FK / Type / Timezone](08-keys-types-timezone.md): กฎชนิดข้อมูล UTC/Asia/Bangkok และเกณฑ์ตรวจรับฐานข้อมูลจริง
- [09 — Index รายตาราง](09-index-inventory.md): PK, Unique, Index ที่ออกแบบ และ FK ที่ต้องประเมิน query plan
- [SQL comments ภาษาไทย](comments.th.sql): คำอธิบาย 128 ตารางและ 1,481 คอลัมน์สำหรับใช้หลังสร้าง schema จริง ยังไม่ได้ execute
- สร้างซ้ำตามลำดับ: python3 tools/build_catalog.py → python3 tools/build_comments.py → python3 tools/validate_design.py
