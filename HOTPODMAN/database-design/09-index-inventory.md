# 09 — บัญชี PK / Unique / Index รายตาราง

สถานะ: ข้อกำหนดออกแบบ ไม่ใช่ผลตรวจ Index ใน PostgreSQL จริง ยังไม่มี migration หรือ EXPLAIN ANALYZE

ทุกตารางมี PK(id) เป็น UUID; U หมายถึง Unique และ I หมายถึง Index ที่ระบุในแบบ ตาราง tenant ต้องเพิ่ม UNIQUE(company_id,id) สำหรับ composite FK ด้วย แม้ไม่ได้พิมพ์ซ้ำในช่อง Candidate ด้านล่าง

Unique/PK สร้างดัชนีรองรับเมื่อสร้าง constraint จริง แต่ FK ไม่สร้าง index ฝั่งลูกอัตโนมัติ ห้ามสรุปว่ามี FK แล้ว query จะเร็ว ส่วน FK ที่ยังไม่มีดัชนีตรงรูปแบบ query ต้องประเมินจาก workload ไม่เพิ่มทุกคอลัมน์โดยอัตโนมัติ

ค่าด้านล่างเป็น notation ไม่ใช่ SQL ที่รันได้; NULLS NOT DISTINCT, partial predicates, expression indexes และคอลัมน์ซ้ำใน composite ต้องลง migration และตรวจชื่อ/ชนิด/ลำดับจริง

| ตาราง | PK | Unique / Index ที่ออกแบบไว้ | FK ที่ต้องตรวจแผน query ฝั่งลูก |
|---|---|---|---|
| `geo.provinces` | `id UUID` | U(official_code) | ไม่มี |
| `geo.districts` | `id UUID` | U(official_code); U(province_id,id) | province_id |
| `geo.subdistricts` | `id UUID` | U(official_code); U(district_id,id) | district_id |
| `geo.postal_codes` | `id UUID` | U(code) | ไม่มี |
| `geo.subdistrict_postal_codes` | `id UUID` | U(subdistrict_id,postal_code_id); I(postal_code_id) | subdistrict_id, postal_code_id |
| `org.companies` | `id UUID` | U(code) | province_id, district_id, subdistrict_id, postal_code_id |
| `org.branches` | `id UUID` | U(company_id,code); partial U(company_id) WHERE is_head_office | company_id, province_id, district_id, subdistrict_id, postal_code_id |
| `org.warehouses` | `id UUID` | U(company_id,branch_id,code); partial U(company_id,branch_id) WHERE is_default | company_id, branch_id |
| `org.locations` | `id UUID` | U(company_id,warehouse_id,code); I(company_id,parent_id) | company_id, warehouse_id, parent_id |
| `org.usage_points` | `id UUID` | U(company_id,branch_id,code) | company_id, branch_id |
| `security.users` | `id UUID` | U(lower(username)); U(lower(email)) | ไม่มี |
| `security.memberships` | `id UUID` | U(company_id,user_id) | company_id, user_id |
| `security.access_scopes` | `id UUID` | U NULLS NOT DISTINCT(company_id,kind,branch_id,warehouse_id) | company_id, branch_id, warehouse_id |
| `security.membership_scopes` | `id UUID` | U(company_id,membership_id,scope_id) | company_id, membership_id, scope_id |
| `security.roles` | `id UUID` | U(company_id,code) | company_id |
| `security.permissions` | `id UUID` | U(code) | ไม่มี |
| `security.role_permissions` | `id UUID` | U(company_id,role_id,permission_id) | company_id, role_id, permission_id |
| `security.role_assignments` | `id UUID` | U(company_id,membership_scope_id,role_id) | company_id, membership_scope_id, role_id |
| `security.sessions` | `id UUID` | I(user_id,revoked_at); U(family_id) | user_id |
| `security.refresh_tokens` | `id UUID` | U(jti); U(token_hash); I(session_id) | session_id, replaced_by_id |
| `platform.documents` | `id UUID` | U(company_id,branch_id,kind,document_no); I(company_id,kind,status,created_at) | company_id, branch_id, created_by, confirmed_by, reverses_document_id |
| `platform.document_lines` | `id UUID` | U(company_id,document_id,line_no) | company_id, document_id |
| `platform.number_sequences` | `id UUID` | U(company_id,branch_id,kind,fiscal_year) | company_id, branch_id |
| `platform.files` | `id UUID` | U(company_id,object_key); I(company_id,created_at) | company_id, uploaded_by |
| `platform.document_files` | `id UUID` | U NULLS NOT DISTINCT(company_id,document_id,line_id,file_id,purpose) | company_id, document_id, line_id, file_id |
| `platform.approval_policies` | `id UUID` | U(company_id,code,revision) | company_id, scope_id |
| `platform.approval_policy_steps` | `id UUID` | U(company_id,policy_id,step_no) | company_id, policy_id, role_id |
| `platform.approval_requests` | `id UUID` | I(company_id,document_id,status) | company_id, document_id, policy_id, requested_by |
| `platform.approval_decisions` | `id UUID` | U(company_id,request_id,step_no,decided_by) | company_id, request_id, decided_by |
| `platform.setting_definitions` | `id UUID` | U(key) | ไม่มี |
| `platform.setting_versions` | `id UUID` | U(company_id,definition_id,scope_id,revision); no overlapping active periods | company_id, definition_id, scope_id, approval_document_id, changed_by |
| `platform.ui_features` | `id UUID` | U(code) | parent_id, permission_id |
| `platform.feature_overrides` | `id UUID` | U(company_id,feature_id,scope_id) | company_id, feature_id, scope_id |
| `platform.audit_events` | `id UUID` | I(company_id,occurred_at); I(company_id,document_id,occurred_at) | company_id, actor_id, document_id |
| `security.auth_events` | `id UUID` | I(user_id,occurred_at) | user_id |
| `catalog.units` | `id UUID` | U(company_id,code) | company_id |
| `catalog.categories` | `id UUID` | U(company_id,code) | company_id, parent_id |
| `catalog.products` | `id UUID` | U(company_id,code); I(company_id,barcode); I(company_id,deleted_at,created_at) | company_id, category_id, stock_unit_id |
| `catalog.product_units` | `id UUID` | U(company_id,product_id,code,valid_from) | company_id, product_id, unit_id |
| `catalog.product_barcodes` | `id UUID` | U(company_id,code) | company_id, product_id, product_unit_id |
| `catalog.product_translations` | `id UUID` | U(company_id,product_id,locale) | company_id, product_id |
| `catalog.branch_products` | `id UUID` | U(company_id,product_id,branch_id) | company_id, product_id, branch_id |
| `catalog.suppliers` | `id UUID` | U(company_id,code) | company_id, internal_branch_id |
| `catalog.supplier_contacts` | `id UUID` | I(company_id,supplier_id) | company_id, supplier_id |
| `catalog.supplier_addresses` | `id UUID` | partial U(company_id,supplier_id,kind) WHERE is_default | company_id, supplier_id, province_id, district_id, subdistrict_id, postal_code_id |
| `catalog.supplier_products` | `id UUID` | U(company_id,supplier_id,product_id,product_unit_id) | company_id, supplier_id, product_id, product_unit_id |
| `catalog.supplier_prices` | `id UUID` | I(company_id,supplier_product_id,valid_from); no overlapping active ranges | company_id, supplier_product_id |
| `catalog.branch_supplier_products` | `id UUID` | U(company_id,branch_id,supplier_product_id) | company_id, branch_id, supplier_product_id |
| `purchasing.purchase_orders` | `id UUID` | U(company_id,document_id); I(company_id,supplier_id) | company_id, document_id, supplier_id, warehouse_id |
| `purchasing.po_lines` | `id UUID` | U(company_id,document_line_id) | company_id, document_line_id, po_id, product_id |
| `purchasing.po_revisions` | `id UUID` | U(company_id,po_id,revision_no) | company_id, po_id, approval_request_id |
| `purchasing.po_revision_lines` | `id UUID` | U(company_id,revision_id,po_line_id) | company_id, revision_id, po_line_id, supplier_product_id, product_unit_id |
| `purchasing.po_charges` | `id UUID` | I(company_id,revision_id) | company_id, revision_id |
| `purchasing.po_dispatches` | `id UUID` | I(company_id,revision_id,created_at) | company_id, revision_id, sent_by, evidence_file_id |
| `purchasing.delivery_schedules` | `id UUID` | I(company_id,promised_at) | company_id, po_line_id, supersedes_id |
| `purchasing.po_closures` | `id UUID` | I(company_id,po_line_id) | company_id, po_line_id, document_id, reopens_id, approval_request_id |
| `purchasing.po_line_progress` | `id UUID` | U(company_id,po_line_id) | company_id, po_line_id |
| `delivery.confirmations` | `id UUID` | U(company_id,document_id); I(company_id,po_id,arrived_at) | company_id, document_id, po_id, po_revision_id, checked_by |
| `delivery.confirmation_lines` | `id UUID` | U(company_id,document_line_id) | company_id, document_line_id, confirmation_id, po_revision_line_id |
| `delivery.issues` | `id UUID` | I(company_id,status,created_at) | company_id, confirmation_line_id, assigned_to, evidence_file_id |
| `delivery.acceptance_entries` | `id UUID` | I(company_id,confirmation_line_id); U(company_id,id) | company_id, confirmation_line_id, issue_id, reverses_id, confirmed_by |
| `delivery.issue_actions` | `id UUID` | I(company_id,issue_id) | company_id, issue_id, acceptance_entry_id, closure_id, actor_id |
| `delivery.line_progress` | `id UUID` | U(company_id,confirmation_line_id) | company_id, confirmation_line_id |
| `delivery.terminal_resolutions` | `id UUID` | I(company_id,confirmation_line_id) | company_id, confirmation_line_id, document_id, approval_request_id, reverses_id |
| `devices.agents` | `id UUID` | U(company_id,name) | company_id, branch_id |
| `devices.devices` | `id UUID` | U(company_id,serial_no) | company_id, agent_id, warehouse_id |
| `devices.weighings` | `id UUID` | partial U(company_id,device_id,agent_event_id) WHERE device_id IS NOT NULL | company_id, device_id, operator_id, override_approval_request_id |
| `receiving.receipts` | `id UUID` | U(company_id,document_id) | company_id, document_id, warehouse_id, confirmation_id |
| `receiving.receipt_lines` | `id UUID` | U(company_id,document_line_id) | company_id, document_line_id, receipt_id, confirmation_line_id, product_id |
| `receiving.receipt_weighings` | `id UUID` | U(company_id,weighing_id) | company_id, receipt_line_id, weighing_id |
| `receiving.receipt_lots` | `id UUID` | I(company_id,receipt_line_id) | company_id, receipt_line_id, lot_id, package_id, location_id |
| `receiving.variances` | `id UUID` | I(company_id,status) | company_id, receipt_line_id, unit_id, approval_request_id |
| `receiving.ocr_runs` | `id UUID` | I(company_id,document_id) | company_id, document_id, file_id, reviewed_by |
| `inventory.lots` | `id UUID` | U(company_id,lot_code); I(company_id,product_id,expires_at) | company_id, product_id, supplier_id, origin_document_line_id |
| `inventory.packages` | `id UUID` | U(company_id,package_code) | company_id, lot_id, parent_package_id |
| `inventory.barcodes` | `id UUID` | U(code) | company_id, lot_id, package_id |
| `inventory.lot_genealogy` | `id UUID` | U(company_id,parent_lot_id,child_lot_id,document_id) | company_id, parent_lot_id, child_lot_id, document_id |
| `inventory.stock_accounts` | `id UUID` | U NULLS NOT DISTINCT(company_id,product_id,lot_id,package_id,kind,location_id,custody_document_line_id,stock_status) | company_id, product_id, lot_id, package_id, location_id, custody_document_line_id |
| `inventory.postings` | `id UUID` | U(company_id,document_id,action); U(company_id,reverses_posting_id) | company_id, document_id, reverses_posting_id, created_by |
| `inventory.ledger_entries` | `id UUID` | U(company_id,posting_id,entry_no); I(company_id,account_id,created_at) | company_id, posting_id, account_id, document_line_id |
| `inventory.balances` | `id UUID` | U(company_id,account_id) | company_id, account_id, last_entry_id |
| `inventory.reservations` | `id UUID` | I(company_id,account_id,status); U(company_id,document_line_id,account_id) | company_id, document_line_id, account_id |
| `inventory.cost_layers` | `id UUID` | U(company_id,source_line_id,lot_id) | company_id, lot_id, source_line_id |
| `inventory.cost_allocations` | `id UUID` | U(company_id,layer_id,ledger_entry_id) | company_id, layer_id, ledger_entry_id |
| `inventory.opening_lines` | `id UUID` | U(company_id,document_line_id) | company_id, document_line_id, account_id, import_row_id |
| `inventory.status_changes` | `id UUID` | U(company_id,document_line_id) | company_id, document_line_id, from_account_id, to_account_id, approval_request_id |
| `inventory.cost_adjustment_lines` | `id UUID` | U(company_id,document_line_id) | company_id, document_line_id, account_id, cost_layer_id, approval_request_id |
| `inventory.repack_lines` | `id UUID` | U(company_id,document_line_id) | company_id, document_line_id, from_account_id, to_account_id |
| `inventory.transfers` | `id UUID` | U(company_id,document_id) | company_id, document_id, from_warehouse_id, to_warehouse_id, approval_request_id |
| `inventory.transfer_lines` | `id UUID` | U(company_id,document_line_id) | company_id, document_line_id, transfer_id, from_account_id, transit_account_id |
| `inventory.transfer_receipts` | `id UUID` | U(company_id,document_line_id) | company_id, document_line_id, transfer_line_id, to_account_id |
| `inventory.count_sessions` | `id UUID` | U(company_id,document_id) | company_id, document_id, warehouse_id |
| `inventory.count_scope_locks` | `id UUID` | partial U(company_id,warehouse_id) WHERE active | company_id, warehouse_id, session_id |
| `inventory.count_lines` | `id UUID` | U(company_id,session_id,account_id); U(company_id,document_line_id) | company_id, document_line_id, session_id, account_id, counted_by, weighing_id |
| `inventory.adjustment_lines` | `id UUID` | U(company_id,document_line_id); partial U(company_id,count_line_id) WHERE count_line_id IS NOT NULL | company_id, document_line_id, account_id, count_line_id, approval_request_id |
| `withdrawal.requests` | `id UUID` | U(company_id,document_id) | company_id, document_id, warehouse_id, usage_point_id, approval_request_id |
| `withdrawal.request_lines` | `id UUID` | U(company_id,document_line_id) | company_id, document_line_id, request_id, product_id |
| `withdrawal.issue_lines` | `id UUID` | U(company_id,document_line_id) | company_id, document_line_id, request_line_id, source_account_id, custody_account_id, weighing_id |
| `withdrawal.consumptions` | `id UUID` | U(company_id,document_line_id) | company_id, document_line_id, issue_line_id |
| `inventory.return_lines` | `id UUID` | U(company_id,document_line_id) | company_id, document_line_id, issue_line_id, from_account_id, to_account_id, weighing_id |
| `processing.process_definitions` | `id UUID` | U(company_id,code,revision) | company_id, yield_basis_unit_id |
| `processing.jobs` | `id UUID` | U(company_id,document_id) | company_id, document_id, definition_id, warehouse_id, approval_request_id |
| `processing.inputs` | `id UUID` | U(company_id,document_line_id) | company_id, document_line_id, job_id, issue_line_id, custody_account_id, weighing_id |
| `processing.outputs` | `id UUID` | U(company_id,document_line_id) | company_id, document_line_id, job_id, product_id, lot_id, package_id, to_account_id, weighing_id |
| `inventory.waste_lines` | `id UUID` | U(company_id,document_line_id) | company_id, document_line_id, account_id, process_input_id, approval_request_id, weighing_id |
| `processing.input_dispositions` | `id UUID` | I(company_id,input_id) | company_id, input_id, output_id, return_line_id, waste_line_id |
| `purchasing.claims` | `id UUID` | U(company_id,document_id) | company_id, document_id, supplier_id, approval_request_id |
| `purchasing.claim_lines` | `id UUID` | U(company_id,document_line_id) | company_id, document_line_id, claim_id, delivery_issue_id, receipt_variance_id |
| `purchasing.claim_settlements` | `id UUID` | I(company_id,claim_line_id) | company_id, claim_line_id, unit_id, replacement_confirmation_line_id, credit_note_file_id |
| `purchasing.supplier_return_lines` | `id UUID` | U(company_id,document_line_id) | company_id, document_line_id, claim_line_id, source_account_id |
| `purchasing.price_observations` | `id UUID` | U(company_id,source_line_id,source_stage,source_version); I(company_id,product_id,supplier_id,observed_at) | company_id, source_line_id, product_id, supplier_id, unit_id, normalized_unit_id, supersedes_id, reverses_id |
| `devices.label_templates` | `id UUID` | U(company_id,code,revision,locale) | company_id |
| `devices.print_jobs` | `id UUID` | I(company_id,status,created_at) | company_id, template_id, printer_id, package_id, lot_id, requested_by, reprint_of_id |
| `devices.print_attempts` | `id UUID` | U(company_id,print_job_id,attempt_no); U(company_id,agent_event_id) | company_id, print_job_id |
| `integration.connections` | `id UUID` | U(company_id,code) | company_id |
| `integration.external_mappings` | `id UUID` | U(company_id,connection_id,entity_kind,external_id) | company_id, connection_id |
| `integration.import_batches` | `id UUID` | U(company_id,kind,checksum) | company_id, document_id, source_file_id, validated_by |
| `integration.import_rows` | `id UUID` | U(company_id,batch_id,row_no); I(company_id,batch_id,status) | company_id, batch_id |
| `integration.idempotency_keys` | `id UUID` | U(company_id,actor_id,operation,key) | company_id, actor_id, result_document_id |
| `security.provision_requests` | `id UUID` | U(actor_id,idempotency_key) | actor_id, result_company_id |
| `integration.outbox_events` | `id UUID` | U(event_id); partial I(next_attempt_at) WHERE status IN (PENDING,RETRY) | company_id |
| `integration.inbox_events` | `id UUID` | U(company_id,consumer_name,event_id) | company_id |
| `integration.deliveries` | `id UUID` | U(company_id,connection_id,outbox_event_id) | company_id, connection_id, outbox_event_id, document_id |
| `notification.rules` | `id UUID` | U(company_id,scope_id,code) | company_id, scope_id |
| `notification.notifications` | `id UUID` | U(company_id,recipient_id,dedupe_key) | company_id, recipient_id, outbox_event_id, rule_id, document_id |
| `notification.attempts` | `id UUID` | U(company_id,notification_id,channel,attempt_no) | company_id, notification_id |
| `reporting.export_jobs` | `id UUID` | I(company_id,requested_by,created_at) | company_id, requested_by, output_file_id |
| `reporting.refresh_runs` | `id UUID` | I(company_id,view_name,started_at) | company_id |

## งานที่ต้องทำก่อนยืนยันเป้าหมาย GET 25 รายการ / 50 ms

- หน้า products เรียง created_at DESC, id DESC: ประเมิน partial B-tree (company_id,created_at DESC,id DESC) WHERE deleted_at IS NULL; active filter ต้องวัดก่อนเลือกเพิ่ม active ใน key ไม่สร้างคู่ซ้ำโดยไม่มีเหตุผล
- หน้า suppliers: ประเมินรูปแบบเดียวกับ products เมื่อ query มี deleted_at IS NULL และเรียงด้วย created_at/id
- หน้า PO: กรองบริษัท/สาขา/ชนิด/สถานะผ่าน platform.documents แล้ว join purchase_orders; ต้อง EXPLAIN ทั้ง query และตรวจว่ารายการจำกัด 25 header ก่อนโหลดรายละเอียด ห้ามสรุปจาก index บน po_id เพียงตัวเดียว
- ค้นหา contains ชื่อสินค้า: B-tree ทั่วไปไม่พอสำหรับทุก pattern; ประเมิน trigram/รูปแบบค้นหาจากข้อมูลภาษาไทยและ selectivity จริง
- FK ที่ใช้ join/filter หรือเช็ค parent deletion บ่อย: ตรวจ leftmost columns ของดัชนีที่มีอยู่ก่อนเพิ่ม composite index; ดัชนีเริ่ม company_id ใช้เมื่อ query มีขอบเขตบริษัท ไม่เทียบเท่า index UUID เดี่ยวสำหรับงานข้ามบริษัท
- ทดสอบ authorization, RLS, count totals, sort/filter และ deep pagination พร้อม EXPLAIN (ANALYZE, BUFFERS) ใน UAT ข้อมูลใกล้จริง; p95 Backend response <50 ms เป็นเป้าหมายที่ยังไม่พิสูจน์
- ก่อน Production ตรวจ pg_indexes/pg_constraint จริงและเก็บ DDL + query plan; รายงานดัชนีซ้ำ/ไม่ถูกใช้และผลกระทบต่อการเขียนด้วย

อ้างอิง: [PostgreSQL constraints](https://www.postgresql.org/docs/18/ddl-constraints.html)
