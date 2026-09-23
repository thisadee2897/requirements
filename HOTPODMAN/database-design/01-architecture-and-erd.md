# 01 — Architecture และ ER Diagram

## 1. โครงสร้างฐานข้อมูล

PostgreSQL กลางหนึ่งฐานต่อ environment, schema แยกโดเมนใน Modular Monolith เดียว UAT และ Production แยกฐาน/credential/storage โดยเด็ดขาด Domain module เป็นเจ้าของการเขียนตารางของตน และเรียก application service ของอีกโมดูลเมื่อจำเป็นต้องทำ transaction ร่วมกัน

ชื่อฐานแนะนำ `hotpotman` (ชื่อ environment ใช้แยก instance/database configuration); schema ตาม catalog ไม่ใช้ `public` รวมทุกตาราง Prisma เป็น CRUD adapter ไม่เป็นขอบเขตสิทธิ์หรือกฎธุรกิจเพียงชั้นเดียว

| Schema | เจ้าของข้อมูล | เฟสเริ่ม |
|---|---|---|
| org | บริษัท สาขา คลัง Location จุดใช้งาน | F; Location/จุดใช้งาน W |
| security | User, Membership, Scope, Role, Permission, Session | F |
| platform | ทะเบียนเอกสาร ไฟล์ Setting Approval Audit | F/P |
| catalog | สินค้า หน่วย Supplier ราคาและรายการซื้อแต่ละสาขา | F/P |
| purchasing | PO/revision/line/ส่งเอกสาร/นัดส่ง/ปิดค้าง ราคา Claim | P; Claim O |
| delivery | ยืนยันส่งมอบ ปัญหา จำนวนยอมรับ และข้อมูลพร้อมเข้าคลัง | P |
| devices | Agent, Scale, Weighing, Printer และ Label | W |
| receiving | Warehouse Receipt, แบ่ง Lot, ข้อแตกต่างตอนชั่ง, OCR | W |
| inventory | Lot, Package, Account, Ledger, Balance, Count, Transfer, Return | W/O |
| withdrawal | ขอเบิก จ่ายออก เข้า custody และปิดใช้จริง | O |
| processing | แปรรูป Input/Output/Yield และการจัดสรรผล | O |
| integration | Mapping, Import, Outbox, Inbox, Idempotency, ส่งบัญชี | F/P/R |
| notification | กฎ เหตุการณ์แจ้งเตือน และประวัติส่ง | R |
| reporting | View/Materialized View, Export Jobs, refresh metadata | P/W/O/R ตาม source |

F = Foundation; P = จัดซื้อ/ยืนยันส่งมอบ Phase 1; W = ชั่งรับเข้าคลัง; O = งานคลังและแปรรูปต่อเนื่อง; R = รายงาน/เชื่อมต่อขั้นขยาย ลำดับนี้เป็น dependency ของ schema ไม่ได้เลื่อนรายงาน PO ที่ต้องมีใน Phase 1 ไปท้ายโครงการ

## 2. เส้นทางข้อมูลหลัก

- PurchaseOrder มี stable line identity และ immutable issued revisions ทำให้เอกสารส่งมอบอ้างรุ่นที่ถูกต้อง
- Delivery Confirmation เก็บสิ่งที่พบจริง ส่วน acceptance ledger เก็บจำนวนที่ “ยอมรับแล้ว” แยกจากข้อเท็จจริงและปัญหา
- Warehouse Receipt ใช้ส่วนที่ยอมรับแต่ยังไม่ถูกนำเข้าคลัง ชั่งน้ำหนักจริง แล้วเพิ่ม stock ledger เท่านั้น
- Lot ไม่มี `current_warehouse_id` เพราะ Lot เดียวอยู่หลายคลัง/Location ได้ ยอดปัจจุบันอยู่ stock account/balance
- Package/Barcode เป็นตัวระบุ physical trace; สแกนไม่ตัดสต็อกจนยืนยันธุรกรรม
- เบิกออกเข้า custody account ก่อน เพื่อรับคืนหรือส่งแปรรูปได้โดยไม่ตัดซ้ำ; สิ้นสุดการใช้จึงออก external consumption
- Document registry และ DocumentLine registry เป็น FK กลางสำหรับธุรกรรม/ไฟล์/Approval/Audit ไม่ใช้คู่ `type+id` ลอย ๆ เป็นหลักฐานสต็อก

## 3. ER Diagram

แผนภาพแบ่งกลุ่มเพื่ออ่านง่าย แสดงเฉพาะความสัมพันธ์แกนหลักและ PK/FK สำคัญ ไม่รวมทุกคอลัมน์หรือ every composite key ดู Data Dictionary/กฎประกอบสำหรับการบังคับบริษัทเดียวกัน ตารางข้างขวา `o{` คือศูนย์หรือหลายแถว; `||` คือหนึ่งแถว; `o|` คือไม่มีก็ได้แต่ถ้ามีต้องหนึ่งแถว

<!-- GENERATED_DIAGRAMS -->

### ที่อยู่และรหัสพื้นที่

[เปิดแผนภาพ SVG](erd/10-addresses.svg) · [Mermaid source](erd/10-addresses.mmd)

```mermaid
erDiagram
    geoProvinces["geo.provinces"] {
        uuid id PK
    }
    geoDistricts["geo.districts"] {
        uuid id PK
        uuid province_id FK
    }
    geoSubdistricts["geo.subdistricts"] {
        uuid id PK
        uuid district_id FK
    }
    geoPostalCodes["geo.postal_codes"] {
        uuid id PK
    }
    geoSubdistrictPostalCodes["geo.subdistrict_postal_codes"] {
        uuid id PK
        uuid subdistrict_id FK
        uuid postal_code_id FK
    }
    orgCompanies["org.companies"] {
        uuid id PK
        uuid province_id FK
        uuid district_id FK
        uuid subdistrict_id FK
        uuid postal_code_id FK
    }
    orgBranches["org.branches"] {
        uuid id PK
        uuid company_id FK
        uuid province_id FK
        uuid district_id FK
        uuid subdistrict_id FK
        uuid postal_code_id FK
    }
    catalogSupplierAddresses["catalog.supplier_addresses"] {
        uuid id PK
        uuid company_id FK
        uuid province_id FK
        uuid district_id FK
        uuid subdistrict_id FK
        uuid postal_code_id FK
    }
    geoProvinces ||..o{ geoDistricts : "province_id"
    geoDistricts ||..o{ geoSubdistricts : "district_id"
    geoSubdistricts ||..o{ geoSubdistrictPostalCodes : "subdistrict_id"
    geoPostalCodes ||..o{ geoSubdistrictPostalCodes : "postal_code_id"
    geoProvinces ||..o{ orgCompanies : "province_id"
    geoDistricts ||..o{ orgCompanies : "district_id"
    geoSubdistricts ||..o{ orgCompanies : "subdistrict_id"
    geoPostalCodes ||..o{ orgCompanies : "postal_code_id"
    orgCompanies ||..o{ orgBranches : "company_id"
    geoProvinces ||..o{ orgBranches : "province_id"
    geoDistricts ||..o{ orgBranches : "district_id"
    geoSubdistricts ||..o{ orgBranches : "subdistrict_id"
    geoPostalCodes ||..o{ orgBranches : "postal_code_id"
    orgCompanies ||..o{ catalogSupplierAddresses : "company_id"
    geoProvinces ||..o{ catalogSupplierAddresses : "province_id"
    geoDistricts ||..o{ catalogSupplierAddresses : "district_id"
    geoSubdistricts ||..o{ catalogSupplierAddresses : "subdistrict_id"
    geoPostalCodes ||..o{ catalogSupplierAddresses : "postal_code_id"
```

### องค์กร สมาชิก และสิทธิ์

[เปิดแผนภาพ SVG](erd/01-organization-access.svg) · [Mermaid source](erd/01-organization-access.mmd)

```mermaid
erDiagram
    orgCompanies["org.companies"] {
        uuid id PK
    }
    orgBranches["org.branches"] {
        uuid id PK
        uuid company_id FK
    }
    orgWarehouses["org.warehouses"] {
        uuid id PK
        uuid company_id FK
        uuid branch_id FK
    }
    securityUsers["security.users"] {
        uuid id PK
    }
    securityMemberships["security.memberships"] {
        uuid id PK
        uuid company_id FK
        uuid user_id FK
    }
    securityAccessScopes["security.access_scopes"] {
        uuid id PK
        uuid company_id FK
        uuid branch_id FK
        uuid warehouse_id FK
    }
    securityMembershipScopes["security.membership_scopes"] {
        uuid id PK
        uuid company_id FK
        uuid membership_id FK
        uuid scope_id FK
    }
    securityRoles["security.roles"] {
        uuid id PK
        uuid company_id FK
    }
    securityPermissions["security.permissions"] {
        uuid id PK
    }
    securityRoleAssignments["security.role_assignments"] {
        uuid id PK
        uuid company_id FK
        uuid membership_scope_id FK
        uuid role_id FK
    }
    securityRolePermissions["security.role_permissions"] {
        uuid id PK
        uuid company_id FK
        uuid role_id FK
        uuid permission_id FK
    }
    orgCompanies ||..o{ orgBranches : "company_id"
    orgCompanies ||..o{ orgWarehouses : "company_id"
    orgBranches ||..o| orgWarehouses : "branch_id"
    orgCompanies ||..o{ securityMemberships : "company_id"
    securityUsers ||..o| securityMemberships : "user_id"
    orgCompanies ||..o{ securityAccessScopes : "company_id"
    orgBranches o|..o{ securityAccessScopes : "branch_id"
    orgWarehouses o|..o{ securityAccessScopes : "warehouse_id"
    orgCompanies ||..o{ securityMembershipScopes : "company_id"
    securityMemberships ||..o{ securityMembershipScopes : "membership_id"
    securityAccessScopes ||..o{ securityMembershipScopes : "scope_id"
    orgCompanies ||..o{ securityRoles : "company_id"
    orgCompanies ||..o{ securityRoleAssignments : "company_id"
    securityMembershipScopes ||..o{ securityRoleAssignments : "membership_scope_id"
    securityRoles ||..o{ securityRoleAssignments : "role_id"
    orgCompanies ||..o{ securityRolePermissions : "company_id"
    securityRoles ||..o{ securityRolePermissions : "role_id"
    securityPermissions ||..o{ securityRolePermissions : "permission_id"
```

### สินค้า หน่วย Supplier และราคา

[เปิดแผนภาพ SVG](erd/02-catalog.svg) · [Mermaid source](erd/02-catalog.mmd)

```mermaid
erDiagram
    orgBranches["org.branches"] {
        uuid id PK
    }
    catalogProducts["catalog.products"] {
        uuid id PK
        uuid category_id FK
        uuid stock_unit_id FK
    }
    catalogCategories["catalog.categories"] {
        uuid id PK
        uuid parent_id FK
    }
    catalogUnits["catalog.units"] {
        uuid id PK
    }
    catalogProductUnits["catalog.product_units"] {
        uuid id PK
        uuid product_id FK
        uuid unit_id FK
    }
    catalogSuppliers["catalog.suppliers"] {
        uuid id PK
        uuid internal_branch_id FK
    }
    catalogSupplierProducts["catalog.supplier_products"] {
        uuid id PK
        uuid supplier_id FK
        uuid product_id FK
        uuid product_unit_id FK
    }
    catalogSupplierPrices["catalog.supplier_prices"] {
        uuid id PK
        uuid supplier_product_id FK
    }
    catalogBranchProducts["catalog.branch_products"] {
        uuid id PK
        uuid product_id FK
        uuid branch_id FK
    }
    catalogBranchSupplierProducts["catalog.branch_supplier_products"] {
        uuid id PK
        uuid branch_id FK
        uuid supplier_product_id FK
    }
    catalogCategories o|..o{ catalogProducts : "category_id"
    catalogUnits ||..o{ catalogProducts : "stock_unit_id"
    catalogProducts ||..o{ catalogProductUnits : "product_id"
    catalogUnits ||..o{ catalogProductUnits : "unit_id"
    orgBranches o|..o{ catalogSuppliers : "internal_branch_id"
    catalogSuppliers ||..o{ catalogSupplierProducts : "supplier_id"
    catalogProducts ||..o{ catalogSupplierProducts : "product_id"
    catalogProductUnits ||..o{ catalogSupplierProducts : "product_unit_id"
    catalogSupplierProducts ||..o{ catalogSupplierPrices : "supplier_product_id"
    catalogProducts ||..o{ catalogBranchProducts : "product_id"
    orgBranches ||..o{ catalogBranchProducts : "branch_id"
    orgBranches ||..o{ catalogBranchSupplierProducts : "branch_id"
    catalogSupplierProducts ||..o{ catalogBranchSupplierProducts : "supplier_product_id"
```

### PO ที่มีรุ่นและการอนุมัติ

[เปิดแผนภาพ SVG](erd/03-purchasing.svg) · [Mermaid source](erd/03-purchasing.mmd)

```mermaid
erDiagram
    platformDocuments["platform.documents"] {
        uuid id PK
        uuid reverses_document_id FK
    }
    platformDocumentLines["platform.document_lines"] {
        uuid id PK
        uuid document_id FK
    }
    purchasingPurchaseOrders["purchasing.purchase_orders"] {
        uuid id PK
        uuid document_id FK
    }
    purchasingPoLines["purchasing.po_lines"] {
        uuid id PK
        uuid document_line_id FK
        uuid po_id FK
    }
    purchasingPoRevisions["purchasing.po_revisions"] {
        uuid id PK
        uuid po_id FK
        uuid approval_request_id FK
    }
    purchasingPoRevisionLines["purchasing.po_revision_lines"] {
        uuid id PK
        uuid revision_id FK
        uuid po_line_id FK
    }
    purchasingPoCharges["purchasing.po_charges"] {
        uuid id PK
        uuid revision_id FK
    }
    platformApprovalRequests["platform.approval_requests"] {
        uuid id PK
        uuid document_id FK
    }
    platformApprovalDecisions["platform.approval_decisions"] {
        uuid id PK
        uuid request_id FK
    }
    purchasingPoClosures["purchasing.po_closures"] {
        uuid id PK
        uuid po_line_id FK
        uuid document_id FK
        uuid reopens_id FK
    }
    purchasingPoDispatches["purchasing.po_dispatches"] {
        uuid id PK
        uuid revision_id FK
    }
    purchasingDeliverySchedules["purchasing.delivery_schedules"] {
        uuid id PK
        uuid po_line_id FK
        uuid supersedes_id FK
    }
    platformDocuments ||..o{ platformDocumentLines : "document_id"
    platformDocuments ||..o| purchasingPurchaseOrders : "document_id"
    platformDocumentLines ||..o| purchasingPoLines : "document_line_id"
    purchasingPurchaseOrders ||..o{ purchasingPoLines : "po_id"
    purchasingPurchaseOrders ||..o{ purchasingPoRevisions : "po_id"
    platformApprovalRequests o|..o{ purchasingPoRevisions : "approval_request_id"
    purchasingPoRevisions ||..o{ purchasingPoRevisionLines : "revision_id"
    purchasingPoLines ||..o{ purchasingPoRevisionLines : "po_line_id"
    purchasingPoRevisions ||..o{ purchasingPoCharges : "revision_id"
    platformDocuments ||..o{ platformApprovalRequests : "document_id"
    platformApprovalRequests ||..o{ platformApprovalDecisions : "request_id"
    purchasingPoLines ||..o{ purchasingPoClosures : "po_line_id"
    platformDocuments ||..o{ purchasingPoClosures : "document_id"
    platformApprovalRequests ||..o{ purchasingPoClosures : "approval_request_id"
    purchasingPoRevisions ||..o{ purchasingPoDispatches : "revision_id"
    purchasingPoLines ||..o{ purchasingDeliverySchedules : "po_line_id"
```

### การยืนยันส่งมอบและปัญหา

[เปิดแผนภาพ SVG](erd/04-delivery.svg) · [Mermaid source](erd/04-delivery.mmd)

```mermaid
erDiagram
    purchasingPurchaseOrders["purchasing.purchase_orders"] {
        uuid id PK
    }
    purchasingPoRevisionLines["purchasing.po_revision_lines"] {
        uuid id PK
    }
    deliveryConfirmations["delivery.confirmations"] {
        uuid id PK
        uuid po_id FK
    }
    deliveryConfirmationLines["delivery.confirmation_lines"] {
        uuid id PK
        uuid confirmation_id FK
        uuid po_revision_line_id FK
    }
    deliveryIssues["delivery.issues"] {
        uuid id PK
        uuid confirmation_line_id FK
    }
    deliveryAcceptanceEntries["delivery.acceptance_entries"] {
        uuid id PK
        uuid confirmation_line_id FK
        uuid issue_id FK
        uuid reverses_id FK
    }
    deliveryIssueActions["delivery.issue_actions"] {
        uuid id PK
        uuid issue_id FK
        uuid acceptance_entry_id FK
    }
    deliveryLineProgress["delivery.line_progress"] {
        uuid id PK
        uuid confirmation_line_id FK
    }
    deliveryTerminalResolutions["delivery.terminal_resolutions"] {
        uuid id PK
        uuid confirmation_line_id FK
        uuid reverses_id FK
    }
    receivingReceiptLines["receiving.receipt_lines"] {
        uuid id PK
        uuid confirmation_line_id FK
    }
    purchasingPurchaseOrders ||..o{ deliveryConfirmations : "po_id"
    deliveryConfirmations ||..o{ deliveryConfirmationLines : "confirmation_id"
    purchasingPoRevisionLines ||..o{ deliveryConfirmationLines : "po_revision_line_id"
    deliveryConfirmationLines ||..o{ deliveryIssues : "confirmation_line_id"
    deliveryConfirmationLines ||..o{ deliveryAcceptanceEntries : "confirmation_line_id"
    deliveryIssues o|..o{ deliveryAcceptanceEntries : "issue_id"
    deliveryIssues ||..o{ deliveryIssueActions : "issue_id"
    deliveryAcceptanceEntries o|..o{ deliveryIssueActions : "acceptance_entry_id"
    deliveryConfirmationLines ||..o| deliveryLineProgress : "confirmation_line_id"
    deliveryConfirmationLines ||..o{ deliveryTerminalResolutions : "confirmation_line_id"
    deliveryConfirmationLines ||..o{ receivingReceiptLines : "confirmation_line_id"
```

### ชั่งรับเข้าคลังและฉลาก

[เปิดแผนภาพ SVG](erd/05-receiving.svg) · [Mermaid source](erd/05-receiving.mmd)

```mermaid
erDiagram
    deliveryConfirmations["delivery.confirmations"] {
        uuid id PK
    }
    deliveryConfirmationLines["delivery.confirmation_lines"] {
        uuid id PK
        uuid confirmation_id FK
    }
    receivingReceipts["receiving.receipts"] {
        uuid id PK
        uuid confirmation_id FK
    }
    receivingReceiptLines["receiving.receipt_lines"] {
        uuid id PK
        uuid receipt_id FK
        uuid confirmation_line_id FK
    }
    receivingReceiptLots["receiving.receipt_lots"] {
        uuid id PK
        uuid receipt_line_id FK
        uuid lot_id FK
        uuid package_id FK
    }
    receivingReceiptWeighings["receiving.receipt_weighings"] {
        uuid id PK
        uuid receipt_line_id FK
        uuid weighing_id FK
    }
    devicesWeighings["devices.weighings"] {
        uuid id PK
        uuid device_id FK
    }
    devicesDevices["devices.devices"] {
        uuid id PK
    }
    inventoryLots["inventory.lots"] {
        uuid id PK
    }
    inventoryPackages["inventory.packages"] {
        uuid id PK
        uuid lot_id FK
        uuid parent_package_id FK
    }
    orgLocations["org.locations"] {
        uuid id PK
        uuid parent_id FK
    }
    devicesPrintJobs["devices.print_jobs"] {
        uuid id PK
        uuid printer_id FK
        uuid package_id FK
        uuid lot_id FK
    }
    devicesPrintAttempts["devices.print_attempts"] {
        uuid id PK
        uuid print_job_id FK
    }
    deliveryConfirmations ||..o{ deliveryConfirmationLines : "confirmation_id"
    deliveryConfirmations ||..o{ receivingReceipts : "confirmation_id"
    receivingReceipts ||..o{ receivingReceiptLines : "receipt_id"
    deliveryConfirmationLines ||..o{ receivingReceiptLines : "confirmation_line_id"
    receivingReceiptLines ||..o{ receivingReceiptLots : "receipt_line_id"
    inventoryLots ||..o{ receivingReceiptLots : "lot_id"
    inventoryPackages o|..o{ receivingReceiptLots : "package_id"
    orgLocations ||..o{ receivingReceiptLots : "location_id"
    receivingReceiptLines ||..o{ receivingReceiptWeighings : "receipt_line_id"
    devicesWeighings ||..o| receivingReceiptWeighings : "weighing_id"
    devicesDevices o|..o{ devicesWeighings : "device_id"
    inventoryLots ||..o{ inventoryPackages : "lot_id"
    devicesDevices ||..o{ devicesPrintJobs : "printer_id"
    inventoryPackages o|..o{ devicesPrintJobs : "package_id"
    inventoryLots o|..o{ devicesPrintJobs : "lot_id"
    devicesPrintJobs ||..o{ devicesPrintAttempts : "print_job_id"
```

### Ledger ต้นทุน และยอดคงเหลือ

[เปิดแผนภาพ SVG](erd/06-ledger.svg) · [Mermaid source](erd/06-ledger.mmd)

```mermaid
erDiagram
    platformDocuments["platform.documents"] {
        uuid id PK
        uuid reverses_document_id FK
    }
    platformDocumentLines["platform.document_lines"] {
        uuid id PK
        uuid document_id FK
    }
    inventoryLots["inventory.lots"] {
        uuid id PK
        uuid origin_document_line_id FK
    }
    inventoryPackages["inventory.packages"] {
        uuid id PK
        uuid lot_id FK
        uuid parent_package_id FK
    }
    orgLocations["org.locations"] {
        uuid id PK
        uuid parent_id FK
    }
    inventoryStockAccounts["inventory.stock_accounts"] {
        uuid id PK
        uuid lot_id FK
        uuid package_id FK
        uuid location_id FK
    }
    inventoryPostings["inventory.postings"] {
        uuid id PK
        uuid document_id FK
        uuid reverses_posting_id FK
    }
    inventoryLedgerEntries["inventory.ledger_entries"] {
        uuid id PK
        uuid posting_id FK
        uuid account_id FK
        uuid document_line_id FK
    }
    inventoryBalances["inventory.balances"] {
        uuid id PK
        uuid account_id FK
        uuid last_entry_id FK
    }
    inventoryReservations["inventory.reservations"] {
        uuid id PK
        uuid document_line_id FK
        uuid account_id FK
    }
    inventoryCostLayers["inventory.cost_layers"] {
        uuid id PK
        uuid lot_id FK
        uuid source_line_id FK
    }
    inventoryCostAllocations["inventory.cost_allocations"] {
        uuid id PK
        uuid layer_id FK
        uuid ledger_entry_id FK
    }
    platformDocuments ||..o{ platformDocumentLines : "document_id"
    platformDocumentLines ||..o{ inventoryLots : "origin_document_line_id"
    inventoryLots ||..o{ inventoryPackages : "lot_id"
    inventoryLots o|..o{ inventoryStockAccounts : "lot_id"
    inventoryPackages o|..o{ inventoryStockAccounts : "package_id"
    orgLocations o|..o{ inventoryStockAccounts : "location_id"
    platformDocumentLines o|..o{ inventoryStockAccounts : "custody_document_line_id"
    platformDocuments ||..o{ inventoryPostings : "document_id"
    inventoryPostings ||..o{ inventoryLedgerEntries : "posting_id"
    inventoryStockAccounts ||..o{ inventoryLedgerEntries : "account_id"
    platformDocumentLines ||..o{ inventoryLedgerEntries : "document_line_id"
    inventoryStockAccounts ||..o| inventoryBalances : "account_id"
    inventoryLedgerEntries o|..o{ inventoryBalances : "last_entry_id"
    platformDocumentLines ||..o{ inventoryReservations : "document_line_id"
    inventoryStockAccounts ||..o{ inventoryReservations : "account_id"
    inventoryLots ||..o{ inventoryCostLayers : "lot_id"
    platformDocumentLines ||..o{ inventoryCostLayers : "source_line_id"
    inventoryCostLayers ||..o{ inventoryCostAllocations : "layer_id"
    inventoryLedgerEntries ||..o{ inventoryCostAllocations : "ledger_entry_id"
```

### โอน ตรวจนับ และเบิก

[เปิดแผนภาพ SVG](erd/07-operations.svg) · [Mermaid source](erd/07-operations.mmd)

```mermaid
erDiagram
    inventoryStockAccounts["inventory.stock_accounts"] {
        uuid id PK
    }
    inventoryTransfers["inventory.transfers"] {
        uuid id PK
    }
    inventoryTransferLines["inventory.transfer_lines"] {
        uuid id PK
        uuid transfer_id FK
        uuid from_account_id FK
        uuid transit_account_id FK
    }
    inventoryTransferReceipts["inventory.transfer_receipts"] {
        uuid id PK
        uuid transfer_line_id FK
        uuid to_account_id FK
    }
    inventoryCountSessions["inventory.count_sessions"] {
        uuid id PK
    }
    inventoryCountLines["inventory.count_lines"] {
        uuid id PK
        uuid session_id FK
        uuid account_id FK
    }
    inventoryAdjustmentLines["inventory.adjustment_lines"] {
        uuid id PK
        uuid account_id FK
        uuid count_line_id FK
    }
    withdrawalRequests["withdrawal.requests"] {
        uuid id PK
    }
    withdrawalRequestLines["withdrawal.request_lines"] {
        uuid id PK
        uuid request_id FK
    }
    withdrawalIssueLines["withdrawal.issue_lines"] {
        uuid id PK
        uuid request_line_id FK
        uuid source_account_id FK
        uuid custody_account_id FK
    }
    withdrawalConsumptions["withdrawal.consumptions"] {
        uuid id PK
        uuid issue_line_id FK
    }
    inventoryReturnLines["inventory.return_lines"] {
        uuid id PK
        uuid issue_line_id FK
        uuid from_account_id FK
        uuid to_account_id FK
    }
    inventoryTransfers ||..o{ inventoryTransferLines : "transfer_id"
    inventoryStockAccounts ||..o{ inventoryTransferLines : "from_account_id"
    inventoryStockAccounts ||..o{ inventoryTransferLines : "transit_account_id"
    inventoryTransferLines ||..o{ inventoryTransferReceipts : "transfer_line_id"
    inventoryStockAccounts ||..o{ inventoryTransferReceipts : "to_account_id"
    inventoryCountSessions ||..o{ inventoryCountLines : "session_id"
    inventoryStockAccounts ||..o{ inventoryCountLines : "account_id"
    inventoryStockAccounts ||..o{ inventoryAdjustmentLines : "account_id"
    inventoryCountLines o|..o| inventoryAdjustmentLines : "count_line_id"
    withdrawalRequests ||..o{ withdrawalRequestLines : "request_id"
    withdrawalRequestLines ||..o{ withdrawalIssueLines : "request_line_id"
    inventoryStockAccounts ||..o{ withdrawalIssueLines : "source_account_id"
    inventoryStockAccounts ||..o{ withdrawalIssueLines : "custody_account_id"
    withdrawalIssueLines ||..o{ withdrawalConsumptions : "issue_line_id"
    withdrawalIssueLines ||..o{ inventoryReturnLines : "issue_line_id"
    inventoryStockAccounts ||..o{ inventoryReturnLines : "from_account_id"
    inventoryStockAccounts ||..o{ inventoryReturnLines : "to_account_id"
```

### แปรรูป คืน Trace และ Claim

[เปิดแผนภาพ SVG](erd/08-processing-claims.svg) · [Mermaid source](erd/08-processing-claims.mmd)

```mermaid
erDiagram
    withdrawalIssueLines["withdrawal.issue_lines"] {
        uuid id PK
    }
    processingJobs["processing.jobs"] {
        uuid id PK
    }
    processingInputs["processing.inputs"] {
        uuid id PK
        uuid job_id FK
        uuid issue_line_id FK
    }
    processingOutputs["processing.outputs"] {
        uuid id PK
        uuid job_id FK
        uuid lot_id FK
    }
    processingInputDispositions["processing.input_dispositions"] {
        uuid id PK
        uuid input_id FK
        uuid output_id FK
        uuid return_line_id FK
    }
    inventoryReturnLines["inventory.return_lines"] {
        uuid id PK
        uuid issue_line_id FK
    }
    inventoryWasteLines["inventory.waste_lines"] {
        uuid id PK
        uuid process_input_id FK
    }
    inventoryLots["inventory.lots"] {
        uuid id PK
    }
    inventoryLotGenealogy["inventory.lot_genealogy"] {
        uuid id PK
        uuid parent_lot_id FK
        uuid child_lot_id FK
    }
    deliveryIssues["delivery.issues"] {
        uuid id PK
    }
    receivingVariances["receiving.variances"] {
        uuid id PK
    }
    purchasingClaims["purchasing.claims"] {
        uuid id PK
    }
    purchasingClaimLines["purchasing.claim_lines"] {
        uuid id PK
        uuid claim_id FK
        uuid delivery_issue_id FK
        uuid receipt_variance_id FK
    }
    purchasingClaimSettlements["purchasing.claim_settlements"] {
        uuid id PK
        uuid claim_line_id FK
    }
    purchasingSupplierReturnLines["purchasing.supplier_return_lines"] {
        uuid id PK
        uuid claim_line_id FK
    }
    processingJobs ||..o{ processingInputs : "job_id"
    withdrawalIssueLines ||..o{ processingInputs : "issue_line_id"
    processingJobs ||..o{ processingOutputs : "job_id"
    inventoryLots ||..o{ processingOutputs : "lot_id"
    processingInputs ||..o{ processingInputDispositions : "input_id"
    processingOutputs o|..o{ processingInputDispositions : "output_id"
    inventoryReturnLines o|..o{ processingInputDispositions : "return_line_id"
    inventoryWasteLines o|..o{ processingInputDispositions : "waste_line_id"
    withdrawalIssueLines ||..o{ inventoryReturnLines : "issue_line_id"
    processingInputs o|..o{ inventoryWasteLines : "process_input_id"
    inventoryLots ||..o{ inventoryLotGenealogy : "parent_lot_id"
    inventoryLots ||..o{ inventoryLotGenealogy : "child_lot_id"
    purchasingClaims ||..o{ purchasingClaimLines : "claim_id"
    deliveryIssues o|..o{ purchasingClaimLines : "delivery_issue_id"
    receivingVariances o|..o{ purchasingClaimLines : "receipt_variance_id"
    purchasingClaimLines ||..o{ purchasingClaimSettlements : "claim_line_id"
    purchasingClaimLines ||..o{ purchasingSupplierReturnLines : "claim_line_id"
```

### เอกสาร ไฟล์ Audit และระบบเบื้องหลัง

[เปิดแผนภาพ SVG](erd/09-platform.svg) · [Mermaid source](erd/09-platform.mmd)

```mermaid
erDiagram
    platformDocuments["platform.documents"] {
        uuid id PK
        uuid reverses_document_id FK
    }
    platformDocumentLines["platform.document_lines"] {
        uuid id PK
        uuid document_id FK
    }
    platformFiles["platform.files"] {
        uuid id PK
    }
    platformDocumentFiles["platform.document_files"] {
        uuid id PK
        uuid document_id FK
        uuid line_id FK
        uuid file_id FK
    }
    platformAuditEvents["platform.audit_events"] {
        uuid id PK
        uuid document_id FK
    }
    integrationOutboxEvents["integration.outbox_events"] {
        uuid id PK
    }
    integrationInboxEvents["integration.inbox_events"] {
        uuid id PK
    }
    integrationConnections["integration.connections"] {
        uuid id PK
    }
    integrationDeliveries["integration.deliveries"] {
        uuid id PK
        uuid connection_id FK
        uuid outbox_event_id FK
        uuid document_id FK
    }
    reportingExportJobs["reporting.export_jobs"] {
        uuid id PK
        uuid output_file_id FK
    }
    notificationNotifications["notification.notifications"] {
        uuid id PK
        uuid outbox_event_id FK
        uuid document_id FK
    }
    notificationAttempts["notification.attempts"] {
        uuid id PK
        uuid notification_id FK
    }
    platformDocuments ||..o{ platformDocumentLines : "document_id"
    platformDocuments ||..o{ platformDocumentFiles : "document_id"
    platformDocumentLines o|..o{ platformDocumentFiles : "line_id"
    platformFiles ||..o{ platformDocumentFiles : "file_id"
    platformDocuments o|..o{ platformAuditEvents : "document_id"
    integrationConnections ||..o{ integrationDeliveries : "connection_id"
    integrationOutboxEvents ||..o{ integrationDeliveries : "outbox_event_id"
    platformDocuments ||..o{ integrationDeliveries : "document_id"
    platformFiles o|..o{ reportingExportJobs : "output_file_id"
    integrationOutboxEvents o|..o{ notificationNotifications : "outbox_event_id"
    platformDocuments o|..o{ notificationNotifications : "document_id"
    notificationNotifications ||..o{ notificationAttempts : "notification_id"
```

<!-- END_GENERATED_DIAGRAMS -->

## 4. สิ่งที่ตั้งใจไม่ออกแบบเป็นระบบเต็ม

- POS โต๊ะ บิล การรับเงิน โปรโมชั่น สมาชิก CRM/HR และ Marketplace sales ไม่อยู่ใน HOTPOTMAN บรีพนี้
- ไม่ทำ General Ledger/AP/Payment engine; เก็บข้อมูล/ไฟล์อ้างอิงเพื่อส่งให้บัญชีผ่าน Integration
- ไม่ทำ Production Planning/BOM scheduling; Process Definition ใช้บันทึกงานและเกณฑ์ Yield เท่านั้น
- ไม่แยกฐานต่อบริษัทและไม่ใช้ database-per-branch; isolation ผ่าน composite FK, checked scope และแนวทาง RLS ที่กำหนดใน 03
- ไม่ออกแบบ distributed transaction ระหว่าง Microservices ในเฟสนี้ การ extract ภายหลังต้องมี migration plan และ local invariant ownership ใหม่
