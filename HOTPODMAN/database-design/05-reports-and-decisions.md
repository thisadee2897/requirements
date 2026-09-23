# 05 — Reports, Dashboard และจุดตัดสินใจ

## 1. Read model ที่เสนอ

Views เป็น read-only ไม่ใช้เป็นตารางเขียนธุรกรรม Filters และสิทธิ์ต้องใช้กับ source ก่อน aggregate ตามกรณี ไม่เอายอดรวมทุกบริษัทมา filter ชื่อสาขาทีหลัง

| View / Read model | Grain และแหล่งข้อมูล | Phase |
|---|---|---|
| `reporting.v_po_outstanding` | หนึ่ง stable PO line + effective revision, net acceptance, net closures; aggregate children ก่อน join | P |
| `reporting.v_delivery_variance` | หนึ่ง confirmation line: stated, observed, accepted, pending/issues; issue qty อาจ overlap ห้าม sum ทุก reason เป็นจำนวนของเสีย | P |
| `reporting.v_ready_for_receipt` | หนึ่ง confirmation line ที่ผ่าน gate/legacy status: accepted−warehouse consumed−terminal resolution | P/W |
| `reporting.v_price_history` | หนึ่ง active source observation แยก stage PO/DELIVERY/WAREHOUSE, currency, normalized unit และ tax basis | P/W |
| `reporting.v_supplier_performance` | Supplier+branch+ช่วงเวลา: นัดส่งเทียบจริง, accepted/order, issue/claim rates มีตัวหารชัด | P/O |
| `reporting.v_stock_balance` | หนึ่ง warehouse/location/product/lot/package/status พร้อม qty/kg/value จาก ledger projection | W |
| `reporting.v_stock_card` | หนึ่ง ledger entry ของ owned accounts ตาม effective posting order; opening+running balance; ไม่เอา contra external มาบวกรวม | W |
| `reporting.v_receipt_variance` | หนึ่ง warehouse receipt line กับ expected/document weight vs measured และ price variance | W |
| `reporting.v_withdrawal_consumption` | แยก requested/issued/custody/consumed/returned ตาม issue line ไม่รวม issueกับconsumeเป็นเบิก2ครั้ง | O |
| `reporting.v_transfer_outstanding` | หนึ่ง transfer line: dispatched/received/transit/approved loss, units consistent | O |
| `reporting.v_count_adjustments` | หนึ่ง count line กับ snapshot/count/difference/posted adjustment; uncounted null | O |
| `reporting.v_processing_yield` | หนึ่ง completed job: basis input/output/return/waste + standard snapshot; numerator/denominator รวมก่อนคิดเปอร์เซ็นต์ | O |
| `reporting.v_claim_status` | หนึ่ง claim line: claimed qty/amount, settlement/currency, outstanding; stock effect แสดง source posting แยก | O |
| `reporting.v_expiry_quarantine` | owned warehouse/custody stock แยกหมดอายุจริง ณ asOf และ bucket; package expiry ที่สั้นกว่า lot ต้องมีผล | W/O |
| `reporting.v_traceability` | recursive genealogy + document lineage → receipt/delivery/PO/supplier และ downstream movement | W/O |
| `reporting.v_audit_timeline` | หนึ่ง audit event พร้อม allowed tenant/document scope; auth global log ไม่ปะปน | F/P |

Dashboard ใช้ query/filter definitions เดียวกับรายงานข้างบน โดย drill-down ส่ง filter เดิมกลับไป ไม่สร้างชุดตัวเลขแยกที่ตีความต่างกัน

## 2. นิยามที่ต้องไม่ปะปน

- PO amount = issued effective revision totals; received delivery amount = accepted order qty ×ราคาเอกสารที่ตรวจแล้ว; warehouse receipt value = quantity/basis measured +cost policy หลังชั่ง
- ยอดยืนยันส่งมอบแล้วรอเข้าคลังไม่ใช่ stock และไม่มี value สำหรับจ่ายสินค้า
- Company-owned stock = WAREHOUSE+TRANSIT+CUSTODY ตามมุมมองบัญชีที่เลือก; available stock = เฉพาะ AVAILABLE WAREHOUSE−reservations และไม่หมดอายุ
- Stock Card แสดง counterpart เพื่ออธิบายการเคลื่อนไหว แต่ sum เฉพาะ account scope ที่ดู ห้ามนับ internal transfer เป็นซื้อ/ใช้
- รายงาน branch view ให้ใช้งานตาม branch ของ account/document event ไม่ติด lot ที่ “สาขาแรก” แล้วโอนย้ายยังแสดงผิด
- History stage WAREHOUSE คือราคาตอนรับจริงตาม BR-09; Phase 1 มีเพียง PO/DELIVERY จึงต้องติดป้าย ไม่แสดงแทนราคาต้นทุนรับเข้าจริง
- จำนวนครั้งรับซื้อใช้จำนวน source receipt line ที่ยืนยัน ไม่ใช้จำนวน lot splits หรือ label prints; หากฝ่ายธุรกิจต้องการจำนวน “ครั้งส่ง” ใช้ distinct receipt/confirmation document แสดง metric คนละชื่อ

## 3. Price change methodology

1. เลือก stage, product, supplier, currency, unit/tax basis ที่เทียบกันได้
2. เลือก observation รุ่นล่าสุดที่ไม่ถูก supersede ต่อ source_line/stage และตัด VOID/reversed source ด้วยข้อมูลอ้างอิง ไม่ delete observation history; confirmation ACCEPT เพิ่มจาก issue ให้ append snapshot ใหม่พร้อม supersedes_id แทนการบวก observations ทุกรุ่น
3. Normalize หลัง conversion ที่ยืนยัน ถ้า variable weight ยังไม่มี measured qty ให้ normalized_price null/ไม่เทียบ ไม่ใช้ guessed factor
4. เรียง observed_at, source sequence/version, id เป็น deterministic order และหา LAG ก่อน filter ช่วงเวลารายงาน เพื่อให้มี prior baseline
5. ราคาเดียวกันไม่ถือเปลี่ยน หากไม่มี prior row แถวแรกเป็น baseline
6. `%change=(new−old)/old×100`; old=0 แสดง amount difference และ percent unavailable
7. ราคา100,100,110,105 ไม่มี prior →4 observations,2 changes; ถ้า priorก่อนช่วง=90 →3 changes
8. คำนวณราคาที่เปรียบเทียบด้วย scale/rounding policy เดียวกัน ไม่ใช้ formatting UI เป็นตัวตัดว่าเท่ากัน

## 4. Query/performance design

- ใช้ parameterized SQL และ allowlist sort/report identifiers
- Statement timeout, bounded pagination, keyset สำหรับ Stock Card/Audit ปริมาณมาก; export เข้า job และ object storage
- Read primary สำหรับ operational outstanding/confirmation gating/authorization; optional replica สำหรับ analytical views ที่ยอมรับ lag
- Cache key รวม environment/company/allowed scope hash/report/filter/schema version พร้อม TTL 30–60s และ asOf
- Materialized Views เฉพาะ aggregations ที่วัดแล้วหนัก เช่น daily supplier price/stock value; refresh job แยกจาก HTTP ไม่ refreshทุกrequest
- Concurrent refresh ต้องมี unique key/grain ที่รองรับและ job mutex; late/reversed transactions invalidation/rebuild affected dates ไม่ freezeยอดผิดถาวร
- Index แนะนำใน Dictionary เป็น candidate ต้อง EXPLAIN ANALYZE กับข้อมูลใกล้จริงก่อนเลือก composite order/GIN trigram/partition
- Partition Ledger/Audit เมื่อปริมาณเหมาะสม ไม่ทำก่อนจำเป็น; อย่า partition แล้วทำ global UUID/FK unique ที่ PostgreSQL บังคับไม่ได้โดยไม่เปลี่ยน key design
- Retention Audit >=5ปี ตามบรีพ; token/session/idempotency/raw device payload มีอายุต่างกัน จัด retention matrix ก่อนใช้งานจริง; ห้ามลบ source evidence ที่ธุรกรรมยังอ้างอิง

## 5. ข้อเสนอเริ่มต้นและจุดที่ต้องยืนยัน

สิ่งต่อไปนี้เป็นรายละเอียดออกแบบที่ยังไม่ใช่คำยืนยันลูกค้า ใช้เป็น default สำหรับ review ได้ แต่ต้องล็อกก่อน migration/production ที่เกี่ยวข้อง ไม่บล็อกการออกแบบโดเมนอื่น

| เรื่อง | ข้อเสนอในแบบนี้ | ต้องยืนยันก่อน |
|---|---|---|
| ต้นทุนสต็อก | specific receipt/lot cost layers; physical FEFO/FIFO แยกจาก accounting cost | W: ต้องการ weighted average/FIFO valuation หรือ lot-specific จริง |
| VAT/ค่าขนส่ง/ส่วนลด | เก็บแยกและปันส่วน deterministic; recoverable VAT แยกออก inventory value | P totals และ W valuation |
| หน่วยซื้อที่น้ำหนักแปรผัน | order_qty กับ measured kg แยกชัด สินค้าแต่ละตัวตั้ง FIXED/VARIABLE_WEIGHT | P import master; W weighing |
| แบ่งแพ็กหลายรอบ | fractional order_qty ตาม precision ที่อนุญาต หรือรับทั้งแพ็กแล้ว split lot ภายใน Receipt | W เมื่อรับถุงเดียวหลายครั้ง |
| วัตถุดิบเบิกออกแล้วกลับคืน | warehouse→custody เมื่อเบิก, consume/return/process ปิดยอดภายหลัง | O: ผู้ใช้ปิดใช้จริงรายวันหรือจังหวะใด |
| ต้นทุนของเสียจากแปรรูป | แสดงแยก waste expense หรือกระจายสู่ usable output ตาม policy | O ก่อน complete processing |
| Yield | usable output/gross input before process ×100; unused return เป็นอีก metric | O หากต้องการ yield ต่อ input หลังหักส่วนคืนให้เป็น metric เพิ่ม |
| ตรวจนับขณะทำงาน | scope freeze baseline; ถ้าต้องนับพร้อมธุรกรรมต้องทำ movement reconciliation เพิ่ม | O ก่อน Stock Count |
| Multicurrency | THB baseline เก็บ currency และไม่รวมต่างสกุล; ไม่มี FX valuation จนเพิ่ม policy | P หากซื้อสกุลอื่น |
| Day-only expiry | แปลงวันเป็นเวลา expiry ใน Asia/Bangkok ตามจุดตัดที่กำหนด | W ก่อนพิมพ์ label |
| ทศนิยมชั่ง/จำนวน | DB6 decimal; precision per unit และเครื่องชั่งจริงอาจละเอียดน้อยกว่า | W hardware certification |
| เสียหายหลัง confirmation แต่ก่อน warehouse | terminal resolution ลด ready ไม่เปิด outstanding เอง; replacement ต้องอนุมัติแก้ PO/reopen | W ข้อแตกต่างจริง |
| Approval delegation | ฐานรุ่นแรก role/scope+quorum ไม่มีการมอบอำนาจชั่วคราวโดยอัตโนมัติ | P ถ้ามีผู้อนุมัติสำรองตามเวลา |
| Legacy completeness | UNKNOWN warehouse status ถือ pending review; ไม่ปลอมว่าเข้าคลัง/ยังไม่เข้า | P/W cutover |

กฎที่ยืนยันแล้วไม่ต้องถามซ้ำ: สำนักงานใหญ่สร้างอัตโนมัติและลบ/ปิดไม่ได้, คลังหลักลบไม่ได้, PO/สินค้า/Supplier เป็นของระบบเรา, Delivery Confirmation ไม่เพิ่มสต็อก, Phase 1 รายงานและ Dashboard ใช้ฐานเดียวกัน, UAT/Production แยกกัน

## 6. ความครอบคลุมบรีพเดิมหลัง Phase 1

| BR | การรองรับและสิ่งที่เปลี่ยน |
|---|---|
| BR-01 Master | catalog/org/security ของเรา + external mappings แทน ERP-owned PK |
| BR-02 PO | Purchasing ครบวงจร+revision/approval แทน webhook-only |
| BR-03 รับสินค้า | Phase1 Delivery; W Warehouse Receipt+Weighing/OCR/Variance |
| BR-04 Lot/Label | lots/packages/barcodes/genealogy/templates/print attempts |
| BR-05 คลัง/Location | warehouse/location/accounts/ledger/transfer/expiry |
| BR-06 Count/Adjustment | freeze snapshot+approved adjustment |
| BR-07 Mobile Withdrawal | request/issue/FEFO/permissions; scanอ่านก่อนทำรายการ |
| BR-08 Processing/Return | multiple inputs/outputs, yield, waste, custody return/expiry |
| BR-09 Claim/Price | typed source claims/settlements/supplier returns + stage price history |
| BR-10 Traceability | stable document lines, receipt sources, lot genealogy, immutable ledger |
| BR-11 Reports/Dashboard | views และนิยามด้านบนตาม readiness ของแต่ละ phase |
| BR-12 Settings/Permissions | versioned settings+approval, scopes, UI flags, Audit |
| BR-13 Integration | optional adapter/outbox/mapping/export ไม่มี direct ERP table writes |
| BR-14 Language/Branch | locale/translation tables, scope, immutable labels snapshot ตามเอกสาร |

ไม่มี customer/sales/POS/HR tables ใน catalog เพราะผู้ใช้เลือก HOTPOTMAN ตามแผน Phase1 และงานต่อเนื่อง ไม่ได้เลือก Backend กลางทุกธุรกิจ
