# 03 — กฎข้อมูล สถานะ และ Transaction

## 1. Conventions ที่ใช้ทั้งฐาน

- `id UUID PK`, เวลา `timestamptz` UTC, วันที่ธุรกิจ `date`, UI ใช้ Asia/Bangkok; วันที่หมดอายุที่มีแต่วันแปลงเป็น instant โดย policy ที่ snapshot ชัดเจน
- เงินรวมเอกสาร `numeric(20,2)` ตาม THB; unit cost/stock value `numeric(20,6)`; quantity/weight `numeric(20,6)`; conversion `numeric(24,9)`; rate `numeric(9,6)` กำหนดว่า percent อยู่ 0..100
- API decimal เป็น string ไม่ใช้ JS floating point คำนวณเงิน; ราคา/จำนวน input ตรวจ scale/range ไม่ปล่อย DB ปัดเงียบ ๆ
- `created_at/updated_at` เก็บเวลาระบบ; `effective_at/occurred_at/posted_at` แยกวันที่เหตุการณ์และวันที่ลงบัญชี การลงย้อนหลังต้องผ่านสิทธิ์และไม่เปลี่ยนลำดับ FEFO ที่เคยใช้แล้ว
- Tenant table ทุกตัวมี NOT NULL `company_id`, `UNIQUE(company_id,id)` และ FK `(company_id,parent_id)` → `(company_id,id)` ไม่ใช่ FK UUID เดี่ยว; parent เป็น global table เช่น User/Permission/geo reference ใช้ UUID FK และ application authorization เพิ่ม
- Child ต้องตรง parent เพิ่มเติม: Warehouse.branch_id, Location.warehouse_id, PO line.po_id, RevisionLine.revision.po_id, confirmation.po_revision.po_id, Receipt.confirmation_line.confirmation_id, lot.product_id, package.lot_id ต้องไม่ขัดกับค่าที่ซ้ำใน row
- เพิ่ม composite unique ที่ต้องใช้ refer เช่น `(company_id,warehouse_id,id)` บน locations และ composite FK จาก child ที่ระบุ warehouse; ถ้าหลายทอด ใช้ constraint trigger ตอน commit ไม่ใช้ CHECK ที่ query ตารางอื่น
- `RESTRICT/NO ACTION` deletion เป็นปริยาย; business document, ledger, weighing, approval decision และ audit ไม่มี hard delete จาก runtime role
- Draft แก้ได้ด้วย optimistic `version`; confirmed content immutable ใช้ revision/reversal; status projection เปลี่ยนผ่าน transition เท่านั้น
- ค่า `status/kind/action` ใช้ CHECK หรือ lookup ที่ควบคุมโดย migration ไม่รับค่า arbitrary; เพิ่มค่าแบบ backward compatible

## 2. Tenant isolation และสิทธิ์

User กลางหนึ่งคนมีหลาย CompanyMembership; membership → membership_scope → role_assignments → role_permissions Scope hierarchy: COMPANY ครอบคลุมสาขาของบริษัทนั้น, BRANCH ครอบคลุมคลังในสาขา, WAREHOUSE เฉพาะคลัง โดย effective permission คือ role ที่มี scope ครอบคลุม resource ไม่ใช่ union ทุกบริษัท

- Branch/Warehouse scopes ต้องตรวจว่าอยู่บริษัทเดียวกัน แม้ UUID ถูกเดาถูก
- ใบโอนต้องมีสิทธิ์ต้นทางและปลายทาง ส่วน list ให้แสดงตามสิทธิ์งานส่ง/รับที่เหมาะสม ไม่เผยข้อมูลสาขาอื่นทั้งหมด
- ตรวจ permission ทุก mutation/อ่านไฟล์/export; current user/membership active; ไม่เชื่อ role/company claim เก่าตลอดอายุ JWT
- Runtime role ไม่มี DDL, bypassrls หรือ table ownership; migrator แยก credential; reporting role read-only views ที่มี tenant/branch filters
- เสนอ RLS เป็น defense-in-depth บน tenant tables ก่อน Production: `SET LOCAL app.company_id` ภายใน transaction, policy USING + WITH CHECK แบบ fail closed, runtime role ไม่ owner และ FORCE RLS ตามความเหมาะสม Worker/export ต้องตั้ง context เช่นเดียวกัน ห้ามปล่อย connection context ค้างใน pool
- RLS บริษัทไม่แทนสิทธิ์สาขา/คลัง; branch scopes ยังต้องตรวจใน service/report query และทดสอบ owner/bypass edge case
- Provision company เป็น privileged use case ที่มี role/function เฉพาะ ไม่เปิด bypass RLS ทั่ว API และใช้ `security.provision_requests` เพราะก่อนสร้างยังไม่มี company_id
- สองคำสั่งปิด admin พร้อมกันต้องล็อก membership/role ownership ของบริษัทก่อนตรวจ count เพื่อไม่ให้เหลือศูนย์

## 3. บริษัท/สำนักงานใหญ่/คลังหลัก

Transaction `CreateCompany`:

1. ตรวจ global provision permission + idempotency key และ request hash
2. สร้าง company → head-office branch(active=true,is_head_office=true) → warehouse(is_default=true,active=true) พร้อม initial membership/admin scope
3. บันทึก Audit + Outbox + result_company_id ใน transaction เดียว
4. Commit หลัง deferred constraints ตรวจ exact-one

ข้อบังคับ DB:

- partial unique ป้องกันสำนักงานใหญ่เกินหนึ่งต่อบริษัท/คลังหลักเกินหนึ่งต่อสาขา
- deferred constraint trigger บน company/branch/warehouse INSERT/UPDATE/DELETE ตรวจ “มีหนึ่งเสมอ” ตอน commit; ต้องตรวจบริษัท/สาขาที่เปลี่ยนทั้ง OLD/NEW
- BEFORE trigger ห้าม DELETE/ย้าย company/ถอด is_head_office/active=false ของสำนักงานใหญ่ และห้ามเปลี่ยนตัวคลังหลักโดยเลี่ยงข้อห้ามลบ
- ห้ามลบ company ที่ provision แล้ว; ไม่ใช้ Cascade bypass
- คลังหลักของสาขา active ต้อง active; สำนักงานใหญ่ active เสมอ
- ปิดสาขาทั่วไปต้องไม่มี PO ค้าง, ready delivery, stock/custody/transit/reservation หรือ open operations; reject พร้อมรายการที่ต้องเคลียร์ ไม่ทำ auto-close

Unique constraint เพียงอย่างเดียวทำได้แค่ “ไม่เกินหนึ่ง” ไม่รับรอง “ต้องมีหนึ่ง”; application check อย่างเดียวไม่พอเมื่อทำพร้อมกัน

## 4. หน่วย จำนวน น้ำหนัก และราคา

### 4.1 สามฐานปริมาณ

| ฐาน | ตัวอย่าง | ใช้กับ |
|---|---|---|
| Order basis | ถุง/ลัง/กิโลกรัมตาม PO | ordered, observed, accepted, closed, ready delivery |
| Stock basis | กก. หรือชิ้นตาม product.stock_unit | ledger, balance, reserve, count, issue |
| Actual weight | net kg จากเครื่องชั่ง | measured evidence, DUAL tracking, Yield |

FIXED conversion ใช้เมื่อขนาดบรรจุคงที่และแปลงได้จริง เช่น 1 กล่อง=12 ชิ้น Snapshot factor ณ ออกเอกสาร ส่วน VARIABLE_WEIGHT เช่น “1 ถุงเนื้อ” มีน้ำหนักไม่ตายตัว ห้าม factor สมมติ 1 ถุง=1 กก.

ตัวอย่าง: PO 10 ถุง ยืนยัน 8 ถุง; Receipt ใช้ accepted_order_qty_used=8 ถุง, stock_qty=15.600 กก., net_weight_kg=15.600 กก. ไม่มีการเปรียบเทียบ 15.600 กับ 8 ว่าเกิน PO ต้องตรวจหน่วยแยกกัน

- WEIGHT: stock unit ต้องเป็น MASS และ normalized net weight สัมพันธ์กันตามหน่วย
- QUANTITY: stock unit COUNT; weight optional เป็นหลักฐาน ไม่เปลี่ยน quantity อัตโนมัติ
- DUAL: stock primary quantity และ actual kg ต้องควบคุมทั้งสองมิติ ไม่คำนวณ kg จากจำนวนชิ้นแบบคงที่ถ้าไม่จริง
- กรณีแบ่งถุงรับหลายรอบ อนุญาต fractional order qty ได้เฉพาะ order_precision ที่กำหนด; ถ้าไม่อนุญาตให้จบการรับทั้งหน่วยบรรจุในครั้งเดียวและแบ่งหลาย lot ภายใน Receipt เดียว
- Product base unit/tracking mode ห้ามเปลี่ยนย้อนหลังหลังมี transaction; เปลี่ยนต้อง migration/reclassification ที่มีเอกสารเฉพาะ

### 4.2 เงิน

- เก็บราคา/ส่วนลด/ภาษี/หน่วย/ที่อยู่ใน immutable snapshot; line+document totals reconcile
- ปันส่วนส่วนลดท้ายเอกสาร/ค่าขนส่งลงแต่ละ line ด้วย basis ที่ snapshot และแจกเศษสตางค์แบบ deterministic
- Inventory value แยกจาก gross invoice; VAT ขอคืนได้ไม่รวมต้นทุนตาม policy ที่ต้องยืนยันใน 05
- Currency baseline THB; schema เก็บ currency ชัดเจน ไม่รวมต่างสกุลใน Dashboard และไม่ถือว่ามี FX accounting แล้ว
- ราคาต่าง PO baseline ±2% ต้องอนุมัติเมื่อเกิน; zero denominator ต้องเป็น exception ไม่หารด้วยศูนย์

## 5. PO revisions และการอนุมัติ

- `documents` เป็น identity ของ PO, `purchase_orders` owner header, `po_lines` identity คงที่; `po_revisions` และ `po_revision_lines` เป็น snapshot เนื้อหา
- current_revision_no คือ draft/ล่าสุด; effective_revision_no คือรุ่นที่ issue แล้วมีผล กฎและ FK deferred ต้องชี้ revision ของ PO ตัวเอง
- ก่อน issue ต้องครบ line >0, unit/price/supplier/branch/warehouse active, sum totals, approval subject_hash ตรง revision
- State เนื้อหา revision: DRAFT → SUBMITTED → APPROVED → ISSUED; SUBMITTED → RETURNED/REJECTED/WITHDRAWN; approval request ใหม่เมื่อแก้ hash
- Lifecycle PO ที่แสดงให้ผู้ใช้ OPEN/HELD/CANCELLED/CLOSED เป็น derived labels จาก documents.status (CONFIRMED คือ issued) และ held flag; Delivery progress NOT_DELIVERED/PARTIAL/FULFILLED/CLOSED_SHORT คำนวณจาก ledger ไม่ใช่ column enum เดียวครอบทุกด้าน
- ส่ง PO กับ Supplier acknowledgement อยู่ dispatch history; “พิมพ์ PDF” ไม่ใช่ sent
- Draft revision ใหม่หลัง issue ทำให้ held ขณะรออนุมัติ ก่อนเปลี่ยนรุ่น lock PO/progress และตรวจจำนวนใหม่ >= accepted+net closed
- สินค้า/unit/order dimension ของ line ที่มี accepted แล้วเปลี่ยนไม่ได้ หากเปลี่ยนใช้ line ใหม่และ close outstanding ของเดิม
- ยกเลิกทั้ง PO ได้เมื่อ accepted=0 และไม่มียอดใช้ปลายทาง; accepted>0 ใช้ close outstanding ห้ามลบ confirmation/Receipt
- maker-checker, quorum และ approver role/scope ใช้ policy snapshot สำหรับขั้นตอน แต่ตรวจสิทธิ์ปัจจุบันของผู้อนุมัติด้วย; count decisions โดยคนไม่ใช่จำนวน click

## 6. Delivery Confirmation และความพร้อมเข้าคลัง

### 6.1 แยกข้อเท็จจริงจากสิ่งที่อนุมัติ

`confirmation_lines.observed_order_qty` คือพบจริง ไม่ใช่ accepted; `acceptance_entries` เป็น signed event แบบ action ACCEPT/REVERSE และ qty positive ส่วน projection คำนวณสุทธิ

ข้อเท็จจริงที่ยืนยันแล้วไม่แก้ทับ หากตรวจพบผิดให้เอกสารแก้ไขที่อ้าง documents.reverses_document_id/line เดิม และดำเนินการ reverse acceptance ที่ยังไม่ถูกใช้ ห้าม reset history

Issues สามารถหลายประเภทบนสินค้าส่วนเดียวกันได้ (เช่น price + quality) จึงไม่ใช้ sum(issue.qty) หัก accepted ตรง ๆ; ขอบเขตจำนวนผ่าน/รอตรวจต้องไม่ทับซ้อนใน acceptance action และตรวจ accepted <= observed ถ้า issue เป็น shortage ไม่บวก observed

### 6.2 สมการ

- `accepted(po_line) = Σ ACCEPT − Σ REVERSE` จาก confirmation lines ของ stable PO line
- `closed(po_line) = Σ approved CLOSE − Σ approved REOPEN`
- `outstanding_delivery = effective_ordered − accepted − closed >= 0`
- `ready(confirmation_line) = accepted − net_warehouse_consumed_order_qty − net_terminal_order_qty >= 0`

ยอดทั้งหมดใช้ order basis เดียวกันตาม snapshot ไม่มี Stock Movement ใน Phase 1

Transaction `ConfirmDelivery`:

1. ล็อก idempotency → PO → progress rows เรียง UUID → confirmation/line rows
2. ตรวจ effective revision, scope, held, approval, observed/accepted partition, unit และหลักฐาน
3. เพิ่ม acceptance entries + update projections + append price observation stage DELIVERY + Audit + Outbox
4. Commit แล้วคิวแสดง ready; ไม่มี event consumer ที่เพิ่ม stock โดยอัตโนมัติ

ตัวอย่าง: สั่ง 10 พบ 8 damaged1 → accepted7, outstanding3, ready7; ถ้าผ่านตรวจ damaged1 ภายหลัง ACCEPT เพิ่ม1 จาก issue เดิม ไม่สร้าง observed เพิ่ม ผลเป็น accepted8,outstanding2,ready8

REOPEN ค้างอ้าง CLOSE เดิม, SUM reopened <= close qty; reverse acceptance อ้าง ACCEPT เดิม, SUM reversed <= accepted unused และห้ามข้าม downstream receipt

Terminal resolution ใช้กรณียืนยันแล้วแต่สูญเสีย/ปฏิเสธก่อนเข้าคลัง: ลด ready ผ่านเอกสารอนุมัติและเก็บข้อแตกต่าง ไม่เพิ่ม stock, ไม่เปิดค้าง Supplier อัตโนมัติ หากต้องการของทดแทนให้ผู้จัดซื้ออนุมัติ reopen/PO revision ตามสภาพจริง

## 7. ชั่งและรับเข้าคลัง

- Device measurement immutable มี gross/tare/net/stable/device/operator/time, `net=gross−tare`; server ตรวจ fresh reading, replay event ID และ branch/warehouse scope
- Manual weight ปิดตามปกติ เปิดได้เฉพาะสิทธิ์ฉุกเฉิน+เหตุผล+Audit+approval policy; device_id null เฉพาะ manual มีข้อจำกัดชัด
- Receipt line ต้องอ้าง confirmation line ที่ผ่าน gateและ ready เพียงพอ; receipt header confirmation/warehouse ต้องตรงทุก line
- Price/weight/quality variances มี workflow ที่ไม่แก้ confirmation เงียบ ๆ; เกิน tolerance block post จนอนุมัติ
- `receipt_lots` แบ่ง line หลาย lot/package/location ได้ ผลรวม stock_qty, kg, value ต้องตรง line

Transaction `PostReceipt`:

1. lock confirmation progress → receipt/line → lot/package/account IDs ตามลำดับคงที่
2. recheck ready, receipt status/version, weighing uniqueness และ approver/settings snapshot
3. consume order qty ที่ยืนยันแล้ว สร้าง Lot/Package, warehouse accounts, cost layers
4. เขียน posting + ledger entries (WAREHOUSE +, EXTERNAL supplier contra −) และ update balances ใน transaction เดียว
5. เพิ่ม price observation stage WAREHOUSE, Audit, Outbox และ durable print-job intent
6. Commit แล้วค่อยพิมพ์/แจ้งเตือน งานพิมพ์ล้มเหลวไม่ rollback สต็อกหรือสร้าง Receipt ใหม่

Reversal ต้องสร้าง posting กลับทางและคืน ready/order-consumed พร้อมกัน โดยย้อนทั้ง downstream จนไม่มีของถูกเบิก/โอนไปแล้วที่ทำให้ balance ติดลบ; ห้ามแค่เปลี่ยน status เป็น cancelled โดยไม่ย้อน quantities/cost

## 8. Stock ledger และต้นทุน

### 8.1 Account คือที่อยู่ของ stock ไม่ใช่บัญชี GL

- WAREHOUSE: product/lot/package/location/quality bucket
- TRANSIT: product/lot/package + transfer line ระหว่างส่ง ยังไม่เป็น available ที่ปลายทาง
- CUSTODY: product/lot/package + issue line ของที่เบิกไปถือใช้งาน/แปรรูป ไม่ใช่ของพร้อมเบิกในคลัง
- EXTERNAL: contra เพื่อบันทึกรับจาก Supplier, ใช้หมด, waste หรือ opening; ไม่ใช่ owned stock และอาจติดลบได้
- quality bucket: AVAILABLE/QUARANTINE/DAMAGED/EXPIRED; date expiry ต้องตรวจแม้ยังไม่ได้ย้าย bucket ด้วย scheduler
- account unique ใช้ NULLS NOT DISTINCT หรือ generated canonical key ที่ทดสอบแล้ว เพื่อไม่สร้าง balance ซ้ำเพราะ nullable package; `package_id` ถ้ามีต้องตรง lot/product

Stock ledger append-only; balances เป็น projection lockable; available=WAREHOUSE AVAILABLE balance−HELD reservations และต้องไม่หมดอายุ/non-active

### 8.2 Invariants ของการ post

- posting unique(document_id,action); reversal อ้าง original posting; no update/delete entries
- Movement ของ product/lot เดียวกันมี source negative+destination positive ใน base unit เดียวกัน cost ส่งต่อเท่ากัน
- receipt/consumption/waste/opening ใช้ EXTERNAL contra ไม่เพิ่มของโดยไม่มี source explanation
- processing/return lot ใหม่ใช้ contra เฉพาะ transformation class และ lineage บังคับ ไม่บังคับ sum จำนวนข้ามสินค้า/ข้ามหน่วยเป็นศูนย์แบบผิด ๆ; ตรวจ mass basis และ cost reconciliation แยก
- `SUM(value_delta)` ต่อ posting ต้องเท่ากับศูนย์เมื่อรวม contra; quantity balance ตรวจ per product/base unit สำหรับ movement ปกติ; transformation ตรวจ inputs/outputs/dispositions
- Owned balances (warehouse/transit/custody) ไม่ติดลบทั้ง primary qty และ kg เมื่อ tracking DUAL; reservations ไม่เกิน balance
- สร้าง balance row ด้วย unique account ก่อน lock อย่าใช้ SELECT FOR UPDATE กับแถวที่ยังไม่มีแล้วคิดว่าล็อกได้
- lock IDs เรียงคงที่ ป้องกัน deadlock; bounded retry เฉพาะ serialization/deadlock และ idempotent action
- ห้าม business module เขียน balances โดยไม่มี posting; runtime database role แยก privilege/stored procedure สำหรับ posting ตาม feasibility ของ Prisma transaction ที่เลือก

### 8.3 ต้นทุนที่เสนอเพื่อให้ trace ได้

เสนอ cost basis แบบ specific receipt/lot layer แยก physical FEFO/FIFO ออกจากวิธีประเมินมูลค่า ยังต้องยืนยันใน 05

Cost allocation ของ issue ต้องอ้าง layer เดิม Return คืนด้วย cost ของ issue ไม่ใช่ master current price; โอนคลังพามูลค่าเดิมไป; value rounding residual เคลียร์กับ final layer depletion ไม่ทิ้งเศษให้ stock0/value>0

ถ้าได้รับบิลต้นทุนแก้ภายหลัง ให้เอกสาร cost adjustment แยก ปันส่วน remaining stock กับ consumed variance ตาม policy ห้าม rewrite historical receipt/price evidence ค่าใช้จ่ายที่ไม่มี qty ใช้ value-only ledger entries เฉพาะ action ที่อนุมัติแล้ว

## 9. เบิก คืน แปรรูป และป้องกันตัดซ้ำ

### 9.1 เบิก

Request → approve ถ้ากฎกำหนด → reserve → issue warehouse→custody; การ issue เพียงครั้งเดียวลด warehouse stock. Purpose CONSUMPTION ปิดใช้จริง custody→external; Purpose PROCESSING ใช้ custody เป็น input job ไม่หัก warehouse อีกครั้ง

`issued = custody_remaining + consumed + returned + processing_consumed + disposed` ในมิติเดียวกัน ไม่ให้นับ process return ซ้ำในทั้ง returned และ processing_consumed

FEFO: expires_at ASC NULLS LAST, received_at ASC, account.id; FIFO: received_at ASC, account.id; exclude expired/quarantine/reserved ยืนยันเลือกภายใต้ lock และเก็บเหตุผลเมื่อ override

### 9.2 คืน

Return อ้าง issue/custody เดิม ใช้ actual weighing → child lot/package และ genealogy, `new_expiry <= min(original expiry,returned_at+24h)` ตาม baseline/exception snapshot คืนเข้าจุดจริงและต้นทุนจาก issue

ห้ามแก้ expiry บน original lot ที่ยังมีของอื่นอยู่ ทำให้ของไม่เคยถูกเบิกอายุสั้นตามไปด้วย; expired original ไม่กลับเป็น available แม้คืน

### 9.3 แปรรูป

หนึ่ง job มีหลาย input และหลาย output; inputs อ้าง issue custody; output เป็น product/lot ใหม่พร้อม genealogical allocations จากทุก input ที่เกี่ยวข้อง

- Yield baseline `usable output basis / input before processing basis ×100` ฐานหน่วยต้องเดียวกัน เช่น kg; ไม่เอาชิ้นบวกกิโลกรัม
- คืนวัตถุดิบที่ยังไม่แปรรูปแยก input disposition RETURN ไม่ถือเป็น usable output
- conservation: input mass = output mass + unused returned mass + waste/loss mass; residual/evaporation ต้องมี approved reason ไม่เติม fake output ให้ครบ
- ถ้า input basis=0 ห้าม complete; หาก standard/min/max null รายงาน actual ไม่สร้าง low-yield alert อ้างมาตรฐานที่ไม่มี
- Complete job ใช้ ledger postings ของ output/waste/return ตามเอกสารลูกใน transaction เดียวและ key ไม่ซ้ำ การบันทึก draft disposition ไม่ post stock ก่อนเวลา
- ถ้า return/waste ถูก post แยกก่อน complete แล้ว completion ต้องอ้าง posting เดิมไม่ post ซ้ำ; ให้ baseline เลือก complete แบบ atomic เท่านั้นก่อน
- Input consumed/returned/waste ปิด custody ยอดจริง, output cost allocation + returned cost + expense waste cost = input cost ภายใต้ policy ที่ยืนยัน

## 10. โอนย้าย ตรวจนับ และกักกัน

- ย้าย location ในคลังเดียว atomic pair; โอนข้ามคลัง/สาขาใช้ dispatch warehouse→transit และรับหลายรอบ transit→destination
- shortage ไม่หายจาก transit จน approved waste/claim/return; destination excess ต้องตรวจต้นทาง/นับ ไม่สร้าง positive stock ลอย
- Count baseline ใช้ scope freeze: ใช้ count_scope_locks และล็อกทั้ง warehouse ใน baseline แม้นับเฉพาะหมวด/Location (แลก concurrency กับความถูกต้อง); สร้าง snapshot+freeze locks พร้อมกัน งานรับ/เบิก/ย้าย/กักกันใน scope ถูก block จน finalize/cancel; ไม่ถือ network/UI disabled ว่าเป็น DB lock
- Count session ระบุ scope_snapshot และทุก mutation ตรวจ active freeze ภายใต้ lock เดียวกับ account; ใช้ warehouse-level coordination lock ตอนเปิด/ปิด freeze และตรวจทุก posting รวมการสร้าง account ใหม่ เพื่อปิด race ระหว่าง snapshot กับ movement; freeze ที่หมดอายุไม่ auto-adjust ต้อง cancel/recount ตามนโยบาย
- `difference=counted−snapshot`; adjustment approval แล้ว post เฉพาะ version ที่ยังตรง ไม่ apply snapshot เก่าหลัง unfreeze หรือ movement
- สินค้าที่พบแต่นอก snapshot สร้าง zero baseline account ที่ตรวจ Lot/Location ก่อน ไม่เพิ่ม master product ใหม่เงียบ ๆ
- กักกันย้าย AVAILABLE→QUARANTINE account ใน location เดิมพร้อมเหตุผล ปล่อยต้องอนุมัติและไม่หมดอายุ; dispose ต้อง ledger ลดจริง

## 11. เอกสารกลาง Approval และ Outbox

`platform.documents` เป็น FK registry ไม่ใช่ EAV: typed header ที่มีอยู่ (PO, Confirmation, Receipt, Transfer, Count, Withdrawal, Processing, Claim) ต้อง 1:1 กับ document และ kind ตรงกัน; line-only documents (OPENING, ADJUSTMENT, RETURN, WASTE, CONSUMPTION, TRANSFER_RECEIPT, SUPPLIER_RETURN, COST_ADJUSTMENT, REPACK) ใช้ registry header กับ typed lines และ deferred trigger ตรวจ exactly-one typed child ตอนยืนยัน

PO_CLOSE/TERMINAL_RESOLUTION/SETTING_CHANGE ใช้ document header และ dedicated child rows; Approval references revision/hash ที่ตรวจ service+constraint ตอนผลมีผล ไม่ใช้ polymorphic entity_id เป็นยอดธุรกิจ

- Generic FK audit entity_id/external mapping target_id เป็น evidence/adapter lookup เท่านั้น ต้อง allowlist resolver และไม่เป็น FK ที่ ledger ใช้
- Outbox immutable payload+eventId เขียนกับ business/audit; dispatcher เปลี่ยนเฉพาะ delivery metadata หลัง publish acknowledgement
- Inbox unique consumer/eventId และผล consumer อยู่ local transaction เดียวกัน; lease claim/retry/dead-letter; ไม่อ้าง exactly-once ระหว่าง network
- Integration ไม่เขียน ERP business tables ตรง ๆ และ response accepted/202 ไม่ถือเป็น accounting posting เสร็จ ต้องเก็บ final provider reference/status
- Notification, export, OCR และพิมพ์มี idempotency/retry ไม่ block transaction ที่ถือ stock locks

## 12. กฎ constraints/index ที่ implementation ต้องทำจริง

| กฎ | กลไกหลัก |
|---|---|
| qty/price >=0, gross−tare=net, role scope shape | NOT NULL + row CHECK |
| tenant/relation integrity | Composite FK + parent unique keys |
| one HQ/default warehouse upper bound | Partial unique index |
| exact-one required + cross-row line totals | Deferred constraint trigger + row locks |
| issued snapshot immutable | Trigger/restricted write path + audit |
| no lost update | version predicate, lock, transaction |
| no duplicate ledger/acceptance | unique source action/idempotency + transaction |
| supplier price/setting periods overlap | Exclusion constraint หรือ locked interval validation ด้วย parent lock; เลือกและทดสอบหนึ่งแบบ |
| nullable stock account dimension | NULLS NOT DISTINCT unique; version prerequisite ต้องตรวจ |
| open queues/events | partial index status+next_attempt_at |
| timeline/price/stock history | tenant + entity/product + timestamp + id |
| FEFO | partial stock account/lot query indexes และ EXPLAIN ตามข้อมูลจริง ไม่รวม now() ใน partial index predicate |
| user login case insensitive | normalized fields/expression unique indexes พร้อม query semantics ที่ตรงกัน |

## 13. เอกสารทางการที่ใช้ตรวจกลไก

- PostgreSQL CHECK ไม่ควรอ้างข้อมูลข้ามแถว/ตาราง; ใช้ FK/Unique/Exclusion หรือ trigger ให้เหมาะสม และ nullable unique ต้องออกแบบชัดเจน: [Constraints](https://www.postgresql.org/docs/current/ddl-constraints.html)
- Constraint trigger สามารถ deferred เพื่อตรวจตอนจบ transaction ได้: [CREATE TRIGGER](https://www.postgresql.org/docs/current/sql-createtrigger.html)
- Row lock/deadlock และลำดับล็อกต้องทดสอบจริง: [Explicit Locking](https://www.postgresql.org/docs/current/explicit-locking.html)
- RLS มีข้อยกเว้น owner/superuser และนโยบาย default deny: [Row Security](https://www.postgresql.org/docs/current/ddl-rowsecurity.html)
- Features ที่ ORM schema ไม่รองรับต้องมี custom migration และคงไว้เมื่อ migrate: [Prisma unsupported database features](https://docs.prisma.io/docs/orm/prisma-migrate/workflows/unsupported-database-features)

รายละเอียด version/Prisma API ต้องตรวจ ณ วัน implement แบบนี้ไม่อ้างว่าข้อกำหนดเชิงเอกสารถูก enforce แล้วในฐานจริง

## ที่อยู่แบบมีรหัสอ้างอิง

บริษัท สาขา และที่อยู่ Supplier ใช้ province_id, district_id, subdistrict_id, postal_code_id ที่มี FK จริง พร้อม composite FK ตรวจลำดับพื้นที่และคู่ตำบล–รหัสไปรษณีย์ ตาม [ข้อกำหนดที่อยู่](07-address-model.md) การบันทึกที่อยู่และ snapshot เอกสารต้องอยู่ใน transaction ของงานนั้น
