# 06 — สถานะและ State Transitions

สถานะใน catalog เป็น `text` เพื่อให้ขยายผ่าน migration ได้ แต่ทุกฟิลด์ต้องมี CHECK allowlist และ application transition guard ห้ามใช้ข้อความอิสระจาก client ตารางนี้กำหนด baseline vocabularies; generated/derived status ไม่สร้าง editable column ซ้ำ

## 1. ทะเบียนเอกสารและ Approval

| Entity/field | ค่าที่อนุญาต | กฎเปลี่ยนสถานะ |
|---|---|---|
| documents.status | DRAFT, SUBMITTED, APPROVED, CONFIRMED, POSTED, HELD, CLOSED, CANCELLED, REVERSED | ใช้ subset ตาม kind; P confirmation ใช้ CONFIRMED ไม่ใช้ POSTED ที่สื่อ stock; operation post ต้อง ledger atomic |
| documents.kind | PO, DELIVERY, WAREHOUSE_RECEIPT, PO_CLOSE, TERMINAL_RESOLUTION, OPENING, TRANSFER, TRANSFER_RECEIPT, COUNT, ADJUSTMENT, WITHDRAWAL_REQUEST, ISSUE, CONSUMPTION, RETURN, PROCESSING, WASTE, STOCK_STATUS, SUPPLIER_CLAIM, SUPPLIER_RETURN, SETTING_CHANGE, COST_ADJUSTMENT, REPACK, IMPORT | one typed header/line model ตามชนิด; COST_ADJUSTMENT/REPACK ใช้ cost_adjustment_lines/repack_lines + ledger source ไม่สร้าง arbitrary qty |
| approval_requests.status | PENDING, APPROVED, REJECTED, RETURNED, WITHDRAWN, SUPERSEDED | APPROVED เมื่อ quorum/steps ครบและ subject_hash/version ยังตรง; เปลี่ยนเนื้อหาให้คำขอเดิม SUPERSEDED และคำขอใหม่ |
| approval_decisions.decision | APPROVE, REJECT, RETURN | Append-only; หลัง rejection ต้องสร้าง request ใหม่ ไม่ลบ decision เก่า |
| po_revisions.state | DRAFT, SUBMITTED, RETURNED, REJECTED, WITHDRAWN, APPROVED, ISSUED, SUPERSEDED | ISSUED content immutable; SUPERSEDED เมื่อ issued revision ใหม่มีผล เก็บ revision เก่าทั้งหมด |
| PO header lifecycle | ไม่มี enum OPEN ใน registry; DRAFT/SUBMITTED/APPROVED/CONFIRMED/CLOSED/CANCELLED ตาม registry | CONFIRMED หมายถึง issued effective revision ใน PO; held boolean แยกการพัก ป้องกันสูญ status เดิม |
| po_dispatches.status | PREPARED, SENT, FAILED, ACKNOWLEDGED | SENT มี sent_at+evidence; ACK มี acknowledgement time; retry เป็น attempt ใหม่ อัปเดตสถานะเดิมมี Audit |
| po_closures.action | CLOSE, REOPEN | document ต้อง APPROVED/CONFIRMED ก่อนยอดมีผล; REOPEN อ้าง CLOSE และไม่เกินส่วนที่เหลือ |

การใช้ document status ร่วมกันไม่ได้หมายความว่าทุก kind กระโดดไปทุกสถานะได้ ต้องมี mapping `allowedTransitions[kind]` ใน application พร้อม tests และ trigger สำหรับ confirmed immutability

## 2. การส่งมอบและการรับเข้าคลัง

| Entity/field | ค่าที่อนุญาต | กฎ |
|---|---|---|
| delivery confirmation document | DRAFT → SUBMITTED → CONFIRMED; DRAFT/SUBMITTED → CANCELLED; CONFIRMED → REVERSED ตามเงื่อนไข | มี acceptance เฉพาะส่วนที่ผ่านแล้ว; issue บางส่วนไม่ทำให้ทั้งเอกสารเป็น stock พร้อมใช้ |
| issues.status | OPEN, INVESTIGATING, RESOLVED, REJECTED | ต้องมี issue_action/evidence ก่อนปิด; resolved ไม่เพิ่ม accepted เอง |
| issues.kind | SHORT, EXCESS, DAMAGED, WRONG_ITEM, PRICE, UNIT, DOCUMENT | affected_qty กรณีไม่เป็นจำนวนอาจ0; ห้ามถือทุก issue qty เป็นของอีกกองหนึ่ง |
| acceptance_entries.action | ACCEPT, REVERSE | Append; qty>0; source referenced actionต้องถูกชนิด; derived sums transaction locked |
| legacy_warehouse_state | NOT_STOCKED, ALREADY_STOCKED, UNKNOWN | รายการใหม่ NOT_STOCKED; import UNKNOWN ไม่ ready; flag ไม่ใช่สิทธิ์ลบ receipt; เปลี่ยนมี Audit/evidence |
| terminal resolutions | document APPROVED → CONFIRMED; reversal ผ่านเอกสารใหม่ | สูญเสียหลังยืนยันก่อนstock ไม่สร้าง stock movement; ไม่เปิด POค้างอัตโนมัติ |
| Warehouse Receipt document | DRAFT → SUBMITTED → APPROVED เมื่อจำเป็น → POSTED; POSTED → REVERSED ตาม downstream constraints | ไม่มีการถือ CONFIRMED delivery เท่ากับ POSTED receipt |
| receipt_lines.quality_status | ACCEPTABLE, QUARANTINE, REJECTED | REJECTED stock_qtyต้อง0 และไม่ consume accepted quantity ด้วยการสร้าง positive stock; ใช้ variance/terminal resolution แทน |
| variances.kind/status | QUANTITY, WEIGHT, PRICE, QUALITY, UNIT / OPEN, APPROVAL_PENDING, APPROVED, REJECTED, RESOLVED | ไม่ post ทั้งส่วนที่ blocked; line ที่ผ่านแยกออกได้ ต้อง preserve totals |
| ocr_runs.status | QUEUED, RUNNING, EXTRACTED, REVIEWED, FAILED, CANCELLED | REVIEWED ต้องมี user/time/confirmed_values; retry runใหม่ |
| ready queue status (derived) | NOT_READY, READY, PARTLY_RECEIVED, FULLY_RECEIVED, TERMINATED | จาก accepted/warehouse/terminal+legacy flags ไม่มี fieldให้ผู้ใช้เขียนเอง |

## 3. Stock/Operations

| Entity/field | ค่าที่อนุญาต | กฎ |
|---|---|---|
| stock_accounts.kind | WAREHOUSE, TRANSIT, CUSTODY, EXTERNAL | CHECK shape และ relationship ตาม03 |
| stock_status | AVAILABLE, QUARANTINE, DAMAGED, EXPIRED, NOT_APPLICABLE | nonwarehouse account ใช้ NOT_APPLICABLE; availability ตรวจ expires_atเพิ่ม |
| packages.status | OPEN, SPLIT, DEPLETED, VOID | projection/status ไม่เปลี่ยนยอดด้วยตัวเอง; DEPLETEDจากledger0 และ SPLITมีเอกสาร |
| reservations.status | HELD, CONSUMED, RELEASED, EXPIRED | HELDลด available; CONSUMEDเมื่อ postingเกิดจริง atomically; expireไม่มีstock delta |
| transfers document | DRAFT, SUBMITTED, APPROVED, CONFIRMED, CLOSED, CANCELLED, REVERSED | CONFIRMED=dispatched; fulfillment derived PARTIAL/RECEIVED/RESOLVED; CANCELLEDก่อนdispatchเท่านั้น |
| count_sessions document | DRAFT, CONFIRMED, SUBMITTED, APPROVED, CLOSED, CANCELLED | CONFIRMEDเปิดfreeze/snapshot; CLOSEDเมื่อ adjustment posted/releasedครบ; cancelปล่อยfreezeไม่ปรับstock |
| adjustment document | DRAFT → SUBMITTED → APPROVED → POSTED → REVERSED | maker-checker; version/snapshotยังตรงตอนpost |
| withdrawal request | DRAFT → SUBMITTED → APPROVED → CONFIRMED → CLOSED | CONFIRMEDเริ่มจ่าย; progress derived; cancelเฉพาะremaining unissued |
| issue/return/consumption/waste | DRAFT → APPROVEDตามpolicy → POSTED; REVERSEDผ่านเอกสารใหม่ | ยอด custody/warehouse ตรวจพร้อมกัน |
| processing job | DRAFT → APPROVEDตามpolicy → CONFIRMED → POSTED → CLOSED | CONFIRMEDเริ่มงานและallocate input; POSTEDลงผล atomic; ไม่ cancelทิ้งหลังoutputใช้ต่อแล้ว |
| claim.status | DRAFT, SUBMITTED, APPROVED, SENT, IN_PROGRESS, SETTLED, REJECTED, CANCELLED | SETTLEDเมื่อผลทุกlineครบตามที่ตกลง ไม่แปลว่าชำระเงินจริงในระบบบัญชี |
| settlement.kind | REFUND, CREDIT, REPLACEMENT, REJECTED | หลักฐาน provider/document reference; no automatic stock delta |

## 4. Infrastructure

| Entity/field | ค่าที่อนุญาต | กฎ |
|---|---|---|
| idempotency/provision status | IN_PROGRESS, SUCCEEDED, FAILED | request hash immutable; leaseหมดตรวจ transactionผลจริงก่อนretry; responseไม่เก็บtokens |
| outbox.status | PENDING, PROCESSING, RETRY, SENT, DEAD | claim lease, acknowledgementก่อนSENT; retriesไม่เปลี่ยนeventId |
| import batch/row status | UPLOADED, VALIDATING, INVALID, READY, APPLYING, APPLIED, FAILED, CANCELLED | row subset PENDING/INVALID/READY/APPLIED/FAILED; batch APPLIEDต้องreconcile |
| files.scan_status | PENDING, CLEAN, REJECTED, FAILED | ไฟล์ไม่CLEANไม่เปิดinline/ใช้OCRตามpolicy |
| print_jobs.status | QUEUED, SENT, ACKNOWLEDGED, FAILED, UNKNOWN, CANCELLED | UNKNOWNผลลัพธ์ไม่ชัด ให้ตรวจ/สั่งreprintมีเหตุผล ไม่generatebarcodeใหม่ |
| print_attempts.status | SENT, ACKNOWLEDGED, FAILED, UNKNOWN | recordผล/attempt append; callback eventซ้ำไม่เพิ่มattempt |
| integration.deliveries.status | PENDING, SENDING, ACCEPTED, COMPLETED, RETRY, FAILED | ACCEPTEDอาจเป็น202; COMPLETEDมีหลักฐานปลายทางตามcontract |
| export_jobs.status | QUEUED, RUNNING, COMPLETED, FAILED, EXPIRED, CANCELLED | COMPLETEDเมื่อfileพร้อมและscopeถูกต้อง; downloadตรวจสิทธิ์ปัจจุบัน |
| refresh_runs.status | RUNNING, COMPLETED, FAILED | watermarkเปลี่ยนเมื่อrefreshสำเร็จเท่านั้น |
| notification.attempts.status | PENDING, SENT, DELIVERED, FAILED, UNKNOWN | ไม่สมมติ deliveryจากenqueue; retriesตามchannel |

## 5. Reversal semantics

`documents.reverses_document_id`, `postings.reverses_posting_id` และ specific reversal entry FK ต้องอ้าง original ในcompanyเดียวกันและชนิดที่อนุญาต ห้าม self/cycle

- เอกสาร reversal แยกตัวตนจาก original ไม่ reuseหมายเลข
- Full warehouse posting reversal ได้ครั้งเดียวตาม unique FK; ถ้าต้องการแก้บางส่วนให้เอกสาร adjustment/return/variance ที่มีนโยบายเฉพาะ ไม่ทำpartial posting reversalอย่างกำกวม
- Delivery ACCEPT และ PO CLOSE รองรับ partial reverse/reopen หลายครั้ง แต่รวมไม่เกินต้นทางและส่วนที่ยังไม่ถูกใช้
- ไม่ใช้ REVERSED status แทนการลง ledger/คืนprogress ต้องเกิดทั้งหมดในtransactionเดียว
