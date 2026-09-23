# 04 — แบ่ง Migration ตาม Phase 1 และงานต่อเนื่อง

## 1. ขอบเขตอ้างอิงหลัก

ใช้ [phase1_work_plan_24-30_sep_2026.md](../phase1_work_plan_24-30_sep_2026.md) เป็นขอบเขตหลัก **ทั้งแผน Phase 1 ไม่ใช่เฉพาะ Backend Foundation** ส่วนขั้นหลัง Phase 1 ใช้หัวข้อ 11 ของแผนร่วมกับรายละเอียดงานคลังในบรีพเดิมที่ไม่ขัดคำแก้ไขล่าสุด

| ข้อกำหนดในแผน Phase 1 | ตาราง/กลไกที่รองรับ | เริ่มใช้ |
|---|---|---|
| บริษัทและสำนักงานใหญ่บังคับ | org.companies, branches, warehouses + exact-one constraints | F |
| สาขาและคลังเพิ่มเติม | org.branches, warehouses, security.access_scopes | F |
| สมาชิก/สิทธิ์รายบริษัท สาขา คลัง | users, memberships, membership_scopes, roles, assignments | F |
| ตั้งค่าสินค้า | products, categories, units, product_translations | F |
| หน่วยซื้อ/หน่วยเก็บ/น้ำหนักแปรผัน | product_units + immutable conversion snapshots | P |
| Supplier/ข้อมูลติดต่อ/เงื่อนไขซื้อ | suppliers, supplier_contacts, supplier_addresses | P |
| ราคาแยกผู้ขายและสิทธิ์ซื้อรายสาขา | supplier_products, supplier_prices, branch_supplier_products | P |
| PO ครบวงจร | purchase_orders, po_lines, revisions, revision_lines, charges | P |
| อนุมัติ/วงเงิน/รุ่นเอกสาร | approval_policies, steps, requests, decisions, document registry | P |
| ส่ง PO และติดตามนัดส่ง | po_dispatches, delivery_schedules | P |
| ระงับ/ยกเลิก/ปิดและเปิดค้าง | documents state, held flag, po_closures, progress | P |
| ตรวจการส่งมอบจริง/หลักฐาน | confirmations, confirmation_lines, document_files | P |
| ยืนยันจำนวนผ่านและจัดการปัญหา | acceptance_entries, issues, issue_actions | P |
| ไม่เพิ่มสต็อกก่อนชั่ง | delivery.line_progress แยก ledger, ไม่มี stock writer ใน Phase 1 | P |
| คิวพร้อมรอชั่งรับเข้าคลัง | line_progress + confirmation state/legacy status views | P |
| Report/Dashboard ซื้อ–ส่งมอบ–ราคา | price_observations stage-specific + views ใน 05 | P |
| Audit/เลขเอกสาร/ไฟล์/ตั้งค่า | platform schema | F/P |
| ย้ายข้อมูล PO/ส่งมอบเดิม | import_batches, import_rows, external_mappings | P |
| UAT/Production แยก environment | คนละ DB/role/secret/object storage และ migration history | F |
| ชั่งจริง/OCR/Label | devices + receiving + inventory lot/package | W |
| คลัง Location, stock ledger/cost/balance | org.locations, inventory kernel | W |
| ตรวจนับ เบิก โอน คืน แปรรูป และ Claim | O tables และ workflow ใน 03 | O |
| รายงานเต็ม/บัญชี/แจ้งเตือน | Views ตาม source readiness, integration/notification | P/W/O/R |

F เป็นส่วนแรกของ Phase 1 ไม่ใช่เฟสธุรกิจแทน Phase 1; P ต้องตาม F ให้ครบก่อนกล่าวว่างานจัดซื้อ/ยืนยันส่งมอบเสร็จ การออกแบบ F/P/W/O/R ไม่เปลี่ยนวันที่ตามสัญญาหรือรับรองกำหนดการที่ยังไม่ตรวจทรัพยากร

## 2. ลำดับ Migration ที่เสนอ

| ชุด | เนื้อหา | Dependency / เกณฑ์พร้อม |
|---|---|---|
| M001 | schema, roles, users, companies/branches/warehouses, memberships/access | provision exact-one + rollback/idempotency tests ผ่าน |
| M002 | sessions/token, permissions/roles, files, settings definitions/UI features/audit, outbox/inbox | tenant/credential/session isolation ผ่าน |
| M003 | catalog products/categories/units, Supplier/contact/address/unit offerings/prices/branch catalog | ไม่ reuse code, unit compatibility, period overlap ผ่าน |
| M004 | document/line registry, numbering, approval, setting versions, PO/revisions/lines/charges/dispatch/schedules/closure/progress | approved content hash และ relation trigger ผ่าน |
| M005 | Delivery Confirmation, acceptance ledger, issues/actions, ready progress, price observations, imports/mapping และ Phase 1 views | สั่ง 10 ส่ง 8; ไม่มี stock change ทุก workflow |
| M006 | Location/usage point, Device/Weighing, Lot/Package/Barcode, Accounts/Posting/Ledger/Balance/Cost/Reservations | base stock invariants และ stable weights พร้อม |
| M007 | Warehouse Receipt/splits/variances/OCR, Terminal Resolutions, labels/print jobs/attempts, opening balance | ต้นทาง delivery gate และ atomic post/reversal ผ่าน |
| M008 | Transfer/receipt, Count/Adjustment, status changes, Withdrawal/Issue/Consumption, Return | custody/transit ไม่ตัดซ้ำ; partial transfer/count freeze ผ่าน |
| M009 | Processing/inputs/outputs/dispositions, lot genealogy, waste และ Claim/Supplier Return | mass/cost/yield/return expiry ผ่าน |
| M010 | export/refresh jobs, notification/integration deliveries, advanced report views/materialized views | reports reconcile/correct scopes/freshness/outbound mapping ผ่าน |

การแบ่งชุดเป็น dependency เชิงตรรกะ ตารางที่มี FK วงรอบ เช่น lots.origin_document_line, receipt_lots และ processing outputs/genealogy ให้สร้างตารางก่อนแล้วเพิ่ม FK ภายในชุด migration เดียวที่เกี่ยวข้องหรือชุดตามหลัง ห้ามเปิดการเขียนปลายทางก่อนเพิ่มข้อบังคับครบ FKs ภายใน transaction ที่สร้างเอกสารใหม่ใช้ DEFERRABLE เมื่อจำเป็น ไม่ตั้งทั้งหมด deferred โดยไม่มีเหตุผล

`reporting.export_jobs`/notification in-app ที่ Phase 1 ต้องใช้งาน สามารถย้ายการสร้างตารางย่อยจาก M010 มาพร้อม M005; R หมายถึงสิ่งสนับสนุนที่ deploy ตามโมดูล ไม่ใช่ต้องรอหลังคลังทุกครั้ง

## 3. Prisma และ SQL implementation contract

- สร้าง Prisma schema ตามรุ่นที่เลือกจริงและ multi-schema support ที่รองรับ ไม่คัดลอก syntax ข้าม major
- CRUD/schema fields ใน Prisma; constraints/partial indexes/deferred trigger/RLS/views/locking functions เพิ่ม custom migration SQL พร้อมชื่อแน่นอนและ test
- ห้ามใช้ db push แทน migration ใน UAT/Production หรือปล่อย introspection ลบ custom DB objects
- เลือก constraint approach ของ exact-one, range overlap, document typed child และ stock posting แล้วทดสอบ runtime role ด้วย raw SQL ที่พยายามหลบ service
- หลังเพิ่ม schema ตั้ง grant/revoke ต่อ table/function; read replica account อ่าน view อย่างเดียว
- Application runtime ไม่ใช้ migrator password และไม่สามารถ TRUNCATE/DROP/DISABLE TRIGGER เพื่อเลี่ยงกฎได้
- migration runner หนึ่งตัวต่อ release และ advisory lock; อย่าให้ทุก API replica migrate ตอนเริ่ม

## 4. ย้ายข้อมูลระบบเดิมแบบไม่เพิ่มยอดซ้ำ

### ก่อนตัดระบบ

1. ส่งออกสินค้า หมวด หน่วย Supplier ราคา/สิทธิ์ซื้อรายสาขา PO ทุก line ยอดส่งแล้ว/ปิดแล้ว และเอกสารประกอบ
2. Staging import_rows เก็บ raw+validation errors; ตรวจชื่อคล้ายกันไม่ merge อัตโนมัติ และเช็กหน่วยราคา 0/1 บาทที่เป็น placeholder
3. สร้าง UUID ภายในและ external mapping unique ต่อ connection/type/external ID; ห้ามใช้เลขเอกสารเป็น primary key
4. Po revisions สำหรับข้อมูล legacy ต้องระบุ snapshot ที่มีหลักฐาน หากขาดให้ status NEEDS_REVIEW ห้ามปลอมผู้อนุมัติหรือ Device weighing
5. Import approved accepted totals เป็น explicit legacy confirmation/acceptance records พร้อม flags/เอกสารต้นทาง ไม่สร้างจากสรุปยอดโดยไม่มี reconciliation
6. แยก `ALREADY_STOCKED`, `NOT_STOCKED`, `UNKNOWN` ของ legacy delivery; UNKNOWN ไม่เข้า ready queue จนคนตรวจยืนยัน

### วันเริ่ม Phase 1

- หยุดแก้ PO/ยืนยันส่งมอบระบบเดิมตาม cutoff; นำเข้า delta รอบสุดท้ายด้วย idempotency/checksum แล้วเทียบยอดราย line
- PO ที่ส่งให้ Supplier ไปแล้วต้องไม่ถูกออก/ส่งใหม่อัตโนมัติ
- เก็บสต็อกเก่าเพื่อเตรียมเฟสคลังได้ แต่ Phase 1 ไม่สร้าง Opening stock/Stock Movement
- รายการใหม่หลัง cutoff ทำในระบบใหม่จุดเดียว; fallback manual log ต้องมีเลขอ้างอิงเพื่อ import โดยไม่ซ้ำ

### วันเปิดชั่งรับเข้าคลังเฟสถัดไป

- ทำ physical count/opening ณ cutoff W แยก Lot/Package/Location/status/หน่วย/ต้นทุน; ไฟล์ opening ต้องมี source evidence และอนุมัติ
- confirmation ที่ถูกนำเข้าคลังจริงนอกระบบระหว่าง Phase 1 ถึง W ต้อง mark/import linkage เป็น ALREADY_STOCKED ก่อนสร้าง ready queue
- ของที่รวมอยู่ใน opening แล้วห้ามสร้าง Warehouse Receipt ใหม่ซ้ำ; เก็บ relationship source evidence ได้แต่ไม่ post receipt ซ้ำ
- ยอดที่ยังไม่เข้าคลังใช้ confirmation ready เป็น source เท่านั้น
- legacy stock ที่หาที่มาของ PO ไม่ได้ใช้ origin_kind OPENING/import document line ไม่สร้าง PO/Receipt ปลอมเพื่อให้ FK ครบ

## 5. กรณีตรวจรับที่ต้องรันกับ PostgreSQL จริงภายหลัง

### องค์กร/สิทธิ์

- สร้างบริษัทสำเร็จได้สำนักงานใหญ่+คลังหลักอย่างละหนึ่ง; error หลัง branch insert ต้อง rollback หมด
- สองคำขอ idempotency key เดียวได้ company เดิม; key เดิม payload ต่าง reject
- ลบ/ปิด/ย้ายสำนักงานใหญ่หรือถอด flag ผ่าน API/raw SQL/runtime role ต้อง fail; company insert เดี่ยว commit ต้อง fail
- สร้าง default warehouse ซ้ำ/ปิด default ของ active branch fail
- ผูก product/PO/warehouse/member/ไฟล์ข้ามบริษัท fail ทั้ง composite FK และ authorization
- ปิด admin คนสุดท้ายพร้อมกันสอง transaction ต้องไม่เหลือศูนย์
- RLS unset context, pool reuse, worker scope และ read reports ต้องไม่หลุดข้อมูล

### PO/Delivery

- Stable line ID อยู่ครบหลัง revision; approved hash ต้องตรงก่อน issue
- Acceptance10+concurrent close2 บน order10 ต้องไม่มีผลรวมเกิน10
- สั่ง10 พบ8 ผ่าน8 → accepted8/outstanding2/ready8/stock delta0
- พบ8 ผ่าน7 damage1 → accepted7/outstanding3; resolve pass1 → accepted8 โดย observed ยัง8
- เกิน order เก็บ issue ได้ แต่ accepted เกิน fail จน revise/approve
- close2 หลัง accepted8 → ordered10/accepted8/closed2 ไม่เรียกรับครบ; reopen ไม่เกิน2
- Reverse acceptance ที่มี receipt consume แล้วต้อง fail หรือย้อนปลายทางก่อน
- double confirm, retry after timeout, issue resolve ซ้ำ ต้องไม่มี accepted/ready ซ้ำ
- หลังทุก action Phase 1 จำนวน Ledger Entries ยังคงศูนย์/ไม่เปลี่ยน

### Receipt/Stock

- 8 ถุงชั่ง15.600kg → order consumed8, stock+15.600kg ไม่เทียบ8กับ15.600ว่าเกิน
- Receipt5 จาก ready8 เหลือ3; concurrent receipts5+5 ต้องไม่ใช้เกิน8
- สอง receipts reuse weigh event เดียว fail; unstable/stale/ผิดบริษัท fail; manual ไม่มีสิทธิ์ fail
- ล้มเหลวหลังสร้าง lot ก่อน ledger → rollback lot/package/receipt progress หมด
- location ผิดwarehouse, packageผิดlot, lotผิดproduct fail
- reservation/issue พร้อมกันไม่ติดลบ; stock account nullable dimensions ไม่ duplicate
- FEFO ห้าม expired แม้ scheduler ยังไม่ย้าย bucket; override ต้อง reason
- print failed/retry/reprint ไม่เพิ่ม stock/เปลี่ยน barcode และ audit ครบ
- reversal หลัง stock ถูกใช้แล้ว fail จนย้อน downstream; no silent negative

### Operations

- โอน10 รับ8: ต้นทางลด10 ปลายทางเพิ่ม8 transit2; ปิดshortageต้อง approved disposition
- issue10 → custody10; consume6 return3 waste1 ปิด0 โดย warehouse ถูกลดเพียงครั้งแรก
- คืน lot ใหม่ expiry<=เดิมและ<=24h; original lot ไม่ถูกแก้
- Input10kg → usable7kg+return2kg+waste1kg, yield70% ตาม baseline gross input; cost reconcile
- multiple inputs/outputs trace ย้อนทุก lot; lineage cycle fail
- count freeze block movements; snapshot version เปลี่ยนไม่ apply adjustment เก่า; row ที่ไม่ถูกนับยัง null ไม่ใช่0
- supplier return ก่อน stock ไม่ตัดstock; returnหลังstockต้อง stock posting+claim reference

### Reports/Integration/Recovery

- สั่ง/ยืนยันส่งมอบ/ชั่งรับใช้คนละ stage ไม่ sum ซ้ำ
- ราคาลำดับ100,100,110,105 →4ครั้ง2เปลี่ยน และมี prior row นอกช่วงแล้วคิดถูก
- Void/reversal ไม่เหลือราคา observation ที่ active เกินจริง
- partial receipts/splits ไม่ทำให้ sum order/amount ซ้ำจาก join multiplication
- cache/report materialization scope, export revokeสิทธิ์, read replica lag แสดง asOf
- DB commitสำเร็จ brokerล่ม →outbox pending; restartแล้วส่งได้ inboxไม่ทำซ้ำ
- backup/restore ต้องกู้ custom trigger/index/view/RLS/roles และเทียบ ledger/progress projections ได้

## 6. ขอบเขตการตรวจในงานออกแบบนี้

ตรวจชื่อ/PK/FK targets/diagram table references/Markdown links และ render Mermaid ได้โดยไม่รันฐานข้อมูล ผลเหล่านี้รับรองความสอดคล้องของเอกสารเท่านั้น รายการในหัวข้อ5ยังเป็นแผนทดสอบที่ต้องรันเมื่อ implement ไม่ใช่ผลทดสอบผ่านของระบบจริง

## Reference data และที่อยู่ (Foundation / Phase 1)

- สร้างและนำเข้า geo reference ก่อน company provisioning; ตรวจแหล่งข้อมูล รุ่นข้อมูล สิทธิ์ใช้งาน ความครบ และคู่ตำบล–รหัสไปรษณีย์ก่อนใช้จริง ห้าม seed ID หรือรหัสพื้นที่สมมติ
- ย้าย address JSON เดิมผ่าน staging/mapping; รายการที่จับคู่ไม่ชัดต้องแก้ก่อนสร้าง master ที่ใช้งานได้ ไม่เดาจากชื่อหรือ postcode อย่างเดียว
- ทดสอบอำเภอผิดจังหวัด ตำบลผิดอำเภอ คู่รหัสไปรษณีย์ผิด และพื้นที่ inactive ต้องถูกปฏิเสธ รวมถึงทดสอบกรุงเทพฯ เขต/แขวง
- ทดสอบ CreateCompany สร้างสำนักงานใหญ่ด้วยสำเนาที่อยู่ที่ครบใน transaction เดียว และ rollback ทั้งชุดเมื่อที่อยู่ไม่ผ่าน
- ทดสอบ reference เปลี่ยนชื่อแล้ว PO เก่ายังคงที่อยู่ snapshot เดิม; ห้ามลบ geo ที่ถูกใช้งาน
- ตรวจความสัมพันธ์จริงใน PostgreSQL migration เพิ่มเติม; การตรวจเอกสารไม่ถือว่าพิสูจน์ constraint ในฐานข้อมูลแล้ว
