# Prompt สำหรับสร้าง HOTPOTMAN Backend Foundation

> วิธีใช้: คัดลอกข้อความตั้งแต่หัวข้อ “บทบาทและคำสั่งปฏิบัติงาน” จนจบไปใช้ใน Codex ภายในโฟลเดอร์ Backend ที่ต้องการสร้าง เอกสารนี้เป็น Prompt สำหรับงานในอนาคต การจัดทำไฟล์นี้ไม่ใช่การเริ่มสร้างหรือ Deploy Backend
>
> ขอบเขต: สร้างฐาน Backend ที่รันและทดสอบได้จริง พร้อมรองรับ Phase 1 ของ HOTPOTMAN ไม่ใช่สั่งสร้าง ERP/POS ทุกโมดูล หรือรับรองว่า Phase 1 ทั้งหมดเสร็จภายใน 7 วัน

## 1. บทบาทและคำสั่งปฏิบัติงาน

คุณคือ Senior Backend Architect + Backend Engineer + DevOps Engineer รับผิดชอบสร้าง Backend Foundation ใหม่ให้รันบน Docker ในเครื่อง Development และพร้อมนำไป Deploy บน DigitalOcean ภายหลัง โดยไม่ต้องเปลี่ยนกรอบสถาปัตยกรรมหลัก

ให้ลงมือสร้าง ติดตั้ง dependencies สร้าง migration/seed รัน Docker ทดสอบ API แก้ไขข้อผิดพลาด และตรวจ lint/test/build จนผ่านในขอบเขตที่กำหนด ห้ามหยุดเพียงสร้างโครงไฟล์หรือบอกวิธีรัน

- เริ่มจาก Modular Monolith หนึ่ง repository แบ่ง domain boundaries ชัดเจน ไม่สร้าง Microservices หลายโปรเจคตั้งแต่แรก
- ตรวจสภาพแวดล้อมและไฟล์เดิมก่อน ห้ามลบหรือเขียนทับงานเดิมโดยไม่จำเป็น
- ใช้วิจารณญาณเลือกแนวทางที่เหมาะสมสำหรับรายละเอียดทั่วไปและบันทึกเหตุผล ไม่หยุดถามเรื่องเล็กน้อย
- หากพบความขัดแย้งที่เปลี่ยนขอบเขตธุรกิจ ทำลายข้อมูล หรือจำเป็นต้องใช้สิทธิ์ที่ไม่มี ให้แจ้งจุดนั้นชัดเจนและทำส่วนอิสระต่อ
- ห้าม Deploy Production เปิดบริการ Public ส่ง PO/ข้อความจริง หรือเรียกบริการภายนอกที่มีค่าใช้จ่ายโดยอาศัย Prompt นี้เป็นคำอนุญาต
- ไม่อ้างว่าทดสอบแล้วหากไม่ได้รันจริง ไม่สร้างข้อมูลตัวอย่างให้ดูเหมือนธุรกรรมจริง
- ไม่เปิดเผยรหัสผ่าน Token หรือ Secret ใน tool output, log, README หรือคำตอบสุดท้าย

## 2. ขอบเขตที่จะ implement จริงในงานนี้

สร้างฟังก์ชันใช้งานจริงและมี API/Swagger/test สำหรับ:

1. Auth: login, refresh rotation, logout, me
2. Users: สร้าง ดูรายการ/รายละเอียด แก้ข้อมูล และเปิด/ปิดบัญชีตามสิทธิ์
3. Company membership และสิทธิ์เข้าถึงบริษัท/สาขา
4. Company: สร้างบริษัทพร้อมสำนักงานใหญ่และคลังหลักแบบ atomic พร้อมดู/แก้ข้อมูล
5. Branch: สร้างพร้อมคลังหลัก ดู/แก้ข้อมูล ปิดสาขาทั่วไปตามเงื่อนไข และป้องกันสำนักงานใหญ่
6. Warehouse master: ดู/สร้าง/แก้ข้อมูลคลังเพิ่มเติมและป้องกันคลังหลัก ยังไม่มี Stock Movement
7. Roles/Permissions: รายการสิทธิ์ จัดการ Role และการมอบหมายแบบมีขอบเขตบริษัท/สาขา
8. Products: CRUD จริง รวม Soft Delete, pagination, search, sort และ active filter
9. Reports ตัวอย่างที่อ่านข้อมูลจริงจากโมดูลที่สร้างแล้ว เช่น Product Summary ด้วย parameterized SQL/View
10. Infrastructure: PostgreSQL, Valkey, BullMQ, NATS JetStream, transactional outbox, inbox/deduplication, storage, logging, audit, health, config
11. Docker, migration, development seed, tests และเอกสารประกอบครบ

โมดูล Purchasing, Supplier, Delivery Confirmation, Inventory, Sales, POS, Accounting, HR, CRM, E-commerce และ Integrations ให้จัด domain contracts/documentation ที่ชัดเจน ไม่จำเป็นต้องสร้าง business logic ของทุกโมดูลในงาน Foundation นี้ ห้ามสร้าง endpoint ที่คืน success ปลอมแทน placeholder

Warehouse master ต้องใช้งานจริง เพราะจำเป็นต่อ invariant บริษัท/สำนักงานใหญ่/คลังหลัก ส่วน Warehouse Receipt และสต็อกจริงยังไม่ implement

## 3. บริบทธุรกิจและกฎที่ต้องรักษา

HOTPOTMAN เป็นเจ้าของสินค้า Supplier และ PO เอง ไม่ต้องพึ่ง ERP Webhook เพื่อเปิด PO หรือ Sync Master เพื่อเริ่มทำงาน

### 3.1 บริษัท สำนักงานใหญ่ และคลังหลัก — implement และทดสอบในงานนี้

- สร้าง Company แล้วต้องมีสำนักงานใหญ่หนึ่งแห่งและคลังหลักของสำนักงานใหญ่อัตโนมัติ
- ทั้งสามรายการ รวม Audit/Outbox ของการสร้าง ต้องบันทึกใน Transaction เดียว สำเร็จทั้งหมดหรือไม่เหลือข้อมูลค้างบางส่วน
- บริษัทต้องมีสำนักงานใหญ่หนึ่งแห่งเสมอ สำนักงานใหญ่ลบไม่ได้ ปิดใช้งานไม่ได้ ย้ายบริษัทไม่ได้ และถอดสถานะสำนักงานใหญ่เพื่อหลบกฎไม่ได้
- ทุกสาขามีคลังหลักหนึ่งแห่งเสมอ ลบไม่ได้ และปิดไม่ได้ขณะสาขายัง active
- ผู้มีสิทธิ์แก้ชื่อ ที่อยู่ และข้อมูลติดต่อสำนักงานใหญ่ได้โดยคงรหัสและตัวตนเดิม
- สร้างซ้ำจาก double-click/network retry ต้องไม่สร้างสำนักงานใหญ่หรือคลังหลักซ้ำ
- Company ที่มีสำนักงานใหญ่ห้ามลบแบบ Cascade; ไม่เปิด destructive company-delete endpoint ในงานนี้
- สำหรับสาขาทั่วไปและคลังเพิ่มเติม ให้ปิดใช้งานตามสิทธิ์และเก็บประวัติ ห้ามลบข้อมูลที่มีธุรกรรมอ้างอิง
- บังคับทั้ง service/API และ database constraints/trigger ตามความเหมาะสม Unique index อย่างเดียวรับรองได้เพียง “ไม่เกินหนึ่ง” จึงต้องมีข้อควบคุม “ต้องมีหนึ่งเสมอ” ด้วย เช่น deferred constraint trigger ที่ตรวจตอน commit
- runtime database user ไม่ใช้ superuser และไม่ใช่เจ้าของ migration ที่มีสิทธิ์ถอด constraints; แยก migration credential/role

### 3.2 ยืนยันส่งมอบไม่ใช่รับเข้าคลัง — จัด domain contract ในงานนี้

Phase 1 ของธุรกิจเป็น:

**PO → ตรวจสินค้าที่ Supplier ส่ง → ยืนยันจำนวน/หลักฐาน/ปัญหา → พร้อมรอชั่งรับเข้าคลัง**

เฟสถัดไปเป็น:

**รายการส่งมอบที่ผ่านยืนยัน → ชั่งน้ำหนักจริง → Warehouse Receipt → Stock Movement**

ข้อกำหนดที่ต้องระบุในเอกสารและ public contracts:

- Delivery Confirmation ไม่สร้าง Stock Movement ไม่เพิ่มสต็อก และไม่ทำให้เบิกสินค้าได้
- แยกจำนวนในใบส่งของ จำนวนพบจริง จำนวนที่ยอมรับยืนยัน และจำนวนมีปัญหา/ปฏิเสธ/รอตรวจ
- สั่ง 10 ส่งจริงและยืนยัน 8: ค้างส่งมอบ 2, รอรับเข้าคลัง 8, สต็อกเพิ่มจากขั้นตอนนี้ 0
- หากพบจริง 8 แต่เสียหาย 1: ยอมรับ 7, มีปัญหา 1, ค้างส่งมอบ 3 จนแก้ปัญหาหรืออนุมัติปิดค้าง
- น้ำหนักบนเอกสาร Supplier ไม่ใช่น้ำหนักชั่งจริงจากคลัง
- แยกสถานะ PO/อนุมัติ, การส่ง PO ให้ Supplier, Supplier ตอบรับ, ยืนยันส่งมอบ และรับเข้าคลัง
- รายการร่าง รอตรวจ มีปัญหา ยกเลิก หรือข้อมูลหน่วยไม่ครบ ห้ามถูกใช้เป็นจำนวนพร้อมรับเข้าคลัง
- Warehouse Receipt ในอนาคตอ้างอิง confirmation line/version ถาวร รองรับหลายรอบและป้องกันใช้ยอดเดิมซ้ำ
- การแก้/ย้อน confirmation ที่ถูกใช้ปลายทางแล้วต้องตรวจยอดที่ใช้และแก้ปลายทางตามลำดับ ไม่แก้สต็อกอัตโนมัติจากการแก้ confirmation
- รายการส่งมอบเดิมตอนย้ายระบบต้องแยกเคยเข้าคลังแล้ว/ยังไม่เข้า/ยังไม่ทราบ ห้ามสร้างคิวรอชั่งซ้ำ

### 3.3 PO roadmap — ยังไม่ implement ทั้งวงจรในงาน Foundation

เตรียมเอกสารแยก PurchaseOrder, PurchaseOrderLine, Revision, Approval, DispatchLog, DeliverySchedule, DeliveryConfirmation, DeliveryIssue และ Close/Reopen Outstanding ให้ครอบคลุม:

- ร่าง/คัดลอก เลขเอกสารไม่ซ้ำ ส่วนลด ภาษี การปัดเศษ และ snapshot ข้อมูลเอกสาร
- อนุมัติตามวงเงิน/ลำดับ ป้องกันอนุมัติตนเอง ออก/พิมพ์/บันทึกหลักฐานส่ง
- แก้เป็นรุ่น อนุมัติใหม่ ระงับ ยกเลิก ส่งหลายรอบ ปิด/เปิดค้าง และ Audit
- `ค้างส่งมอบ = จำนวนสั่งรุ่นที่มีผล - จำนวนยอมรับยืนยันสุทธิ - จำนวนปิดค้างสุทธิ`
- ลดจำนวนสั่งต่ำกว่ายอดที่มีผลแล้วไม่ได้ และการยืนยันส่วนเกินต้องแก้ PO/อนุมัติก่อน
- ไม่ผูกเหตุการณ์ delivery.confirmed ให้เพิ่มสต็อกโดยตรง

## 4. Technology Stack และการเลือกเวอร์ชัน

ใช้ Node.js LTS, TypeScript strict, NestJS, PostgreSQL, Prisma ORM, Valkey, BullMQ, NATS JetStream, pnpm, Docker Compose, OpenAPI/Swagger, Argon2id, JWT และ Pino

- ตรวจเวอร์ชันที่รองรับร่วมกันจากเอกสารทางการ ณ วันลงมือ โดยเฉพาะ Prisma configuration/client generation และ NATS driver/JetStream API อย่าเดา API จากคนละ major version
- Pin major/minor ที่เลือกอย่างชัดเจน ใช้ pnpm-lock.yaml และ frozen lockfile ใน CI/build ไม่ใช้ image tag `latest`
- ระบุ packageManager และเวอร์ชัน runtime ใน repository
- ไม่ใช้ AdonisJS, SQLite แทนฐานทดสอบ, MongoDB/Firebase เป็น Main Backend หรือ Supabase client แทน API layer
- Frontend เรียก API เท่านั้น ไม่เชื่อม PostgreSQL โดยตรง

## 5. สถาปัตยกรรมและขอบเขตโมดูล

ใช้เส้นทาง Controller → Application Service → Domain/Repository Port → Data Adapter

- Controller รับ/ส่ง HTTP และเรียก application use case ไม่มี business logic หรือ Prisma call
- โมดูลเรียกกันผ่าน public application interface ไม่ import internal repository/service ของอีกโมดูลโดยตรง
- Prisma generated types ไม่รั่วไปเป็น public domain/API contract
- เพื่อให้กฎบริษัท/สำนักงานใหญ่/คลัง atomic ใช้ Organization aggregate/application service เดียวดูแล transaction boundary ของ Company, Branch และ Warehouse master ได้ ไม่ต้องบังคับแยกด้วย Event
- การเรียก synchronous ภายใน monolith ไม่ต้องผ่าน NATS ทุกครั้ง
- แยก domain event ออกจาก integration event และแยก notification/report/integration job ออกจาก event broadcast
- ใช้ architecture/lint rule ตรวจ forbidden imports สำหรับ boundaries สำคัญ
- ไม่สร้าง interface ซ้อนหลายชั้นโดยไม่มี consumer หรือเหตุผลรองรับ

โครงสร้างตัวอย่าง ปรับได้โดยรักษาหลักการ:

```text
src/
  main.ts
  worker.ts
  config/
  common/{decorators,guards,filters,interceptors,pipes,dto,context}/
  infrastructure/{database,cache,queue,messaging,outbox,storage,logger}/
  modules/
    auth/
    users/
    organizations/       # Company, Branch, Warehouse master และ invariants
    access-control/      # Membership, Roles, Permissions
    products/
    reports/
    audit/
    health/
    purchasing/          # domain contract/README เท่านั้นในงานนี้
    suppliers/
    inventory/
    sales/
    pos/
    accounting/
    hr/
    crm/
    ecommerce/
    notifications/
    integrations/
prisma/{schema.prisma,migrations,seed.ts}
test/
docs/
scripts/
```

## 6. PostgreSQL, Prisma และความแม่นยำ

- UUID เป็น primary key ของ business entities; UTC/timestamptz และ ISO 8601 สำหรับเวลา ใช้ Asia/Bangkok เป็น business timezone
- เงินและจำนวนที่ต้องการ precision ใช้ PostgreSQL numeric/Prisma Decimal พร้อม documented precision/scale ไม่คำนวณเงินด้วย JS Number
- API รับ/ส่ง decimal เป็น string และ validation precision/range ชัดเจน
- Prisma สำหรับ CRUD, relation, migration, transactions; Reports ใช้ parameterized SQL/View/Materialized View ผ่าน report data access แยกได้
- ห้ามต่อ user input เป็น SQL รวมถึง dynamic ORDER BY ต้องใช้ allowlist/static mapping
- Migration SQL ใช้สำหรับ partial index, constraints, triggers และ Views ที่ Prisma schema อธิบายไม่ครบ ห้ามปล่อยให้ schema migration ภายหลังลบกฎเหล่านี้โดยไม่รู้ตัว
- ใช้ Foreign Key และ composite tenant keys ตามความจำเป็นเพื่อห้ามผูก Branch/Warehouse/Product กับ Company ที่ไม่ตรงกัน
- Product `(companyId, code)` unique รวมรายการ soft-deleted ตามนโยบายเริ่มต้น เก็บรหัสไว้ไม่ reuse เงียบ ๆ
- Index ตาม query จริง เช่น membership scope, product company/code, company/deletedAt/createdAt, barcode และ FK ที่ใช้ join อธิบายเหตุผล ไม่ index ทุกคอลัมน์
- Repository scoped helper เป็นจุดรวม `companyId`/soft-delete ไม่กระจายเงื่อนไขตาม controller และทดสอบว่า find/update/delete ไม่หลุด scope
- กำหนด connection limit, timeout และ transaction timeout ให้เหมาะกับจำนวน API/worker instances
- Retry เฉพาะ transient transaction errors แบบ bounded และปลอดภัยต่อ idempotency ไม่ retry ทุก error

### Read/write routing

- `DATABASE_WRITE_URL` ถ้ามีเป็น primary; fallback ไป `DATABASE_URL`
- `DATABASE_READ_URL` สำหรับ report connection; ถ้าไม่มีให้ใช้ write URL
- CRUD, auth, permission checks, invariant checks และข้อมูลที่ต้องอ่านทันทีหลังเขียน ใช้ primary
- Reports ที่ใช้ replica/cache ต้องแสดง generatedAt/asOf และอธิบายความล่าช้า ไม่ใช้ replica อนุมัติหรือคำนวณยอดคงเหลือเพื่อทำธุรกรรม
- ใช้ฐานเดียวใน local; ไม่ต้อง provision replica จริงในงานนี้

## 7. Multi-company, Membership และ Authorization

สร้าง User, Company, Branch, Warehouse, CompanyMembership, BranchMembership หรือ scope equivalent, Role, Permission, UserRole/RoleAssignment, RolePermission

- User เป็นตัวตนกลาง แยก active membership ของแต่ละบริษัทและขอบเขตสาขา
- Role assignment ระบุ company/scope ไม่ทำให้ role ของบริษัท A ใช้ใน B ได้
- รองรับ company-wide role และ branch-scoped role โดยมี semantics ที่เขียนชัด ไม่ใช้ branchId null แบบกำกวม
- เลือก company context ผ่าน `X-Company-Id` สำหรับ API ที่มี tenant scope แล้วตรวจ membership ทุกครั้ง; BranchId ต้องอยู่บริษัทนั้นและผู้ใช้เข้าถึงได้
- ห้ามเชื่อ companyId/userId/role/permission ที่ client ส่งมา และห้ามใช้ requestId เป็นข้อมูล authorization
- Role/permission mutation ป้องกัน privilege escalation และการปิด/ถอดผู้ดูแลคนสุดท้าย
- `SUPER_ADMIN` ของ demo ให้หมายถึงผู้ดูแลภายใน demo company ไม่ให้ข้ามทุกบริษัทโดยอัตโนมัติ
- การสร้างบริษัทใหม่เป็น explicit bootstrap/platform capability หรือกฎ provision ที่มีหลักฐาน ไม่อนุญาตให้ user ทุกคนสร้าง tenant เองโดยปริยาย
- ป้องกัน mass assignment; DTO แยกแก้ profile, membership และสิทธิ์
- `@Permissions('product.create')`, JwtAuthGuard และ PermissionsGuard ต้องใช้กับ endpoint จริง รวม report/export/file operations
- ข้อมูล tenant scope ต้องติดไปกับ jobs/events และตรวจ scope ตอน worker ประมวลผลด้วย

## 8. Authentication และ Sessions

Endpoints:

- POST `/api/v1/auth/login`
- POST `/api/v1/auth/refresh`
- POST `/api/v1/auth/logout`
- GET `/api/v1/auth/me`

ข้อกำหนด:

- Login ด้วย username หรือ email กำหนด normalization/case-insensitive uniqueness ให้ชัด ใช้ Argon2id ไม่คืน passwordHash
- Login failure ใช้ข้อความทั่วไป Rate limit login/refresh แยกจาก traffic ปกติ และไม่ทำให้ user enumeration ง่าย
- Access JWT อายุสั้น ตรวจ algorithm allowlist, issuer, audience, expiry และ session/user status ตามนโยบาย
- Refresh JWT มี jti/sessionId/familyId และ secret แยกจาก access; เก็บเฉพาะ hash/token verifier ใน DB ไม่เก็บ plaintext
- Rotation ต้อง atomic: token เดิมใช้ได้ครั้งเดียว สร้าง token ใหม่และ mark consumed พร้อมกัน พร้อมตรวจ simultaneous refresh
- Reuse token ที่ consumed/revoked ให้ revoke token family ตามนโยบายและบันทึก Audit; document ว่า frontend ต้อง serialize refresh เพื่อหลีกเลี่ยง concurrent-refresh race
- Session รองรับหลาย device ตั้งแต่ schema; logout revoke session ที่ระบุ ไม่ล้าง session อื่นโดยไม่ตั้งใจ
- กำหนดผลของ logout ต่อ access token ให้ชัด แนะนำตรวจ session revocation จาก primary สำหรับ protected API เพื่อยกเลิกได้ทันทีในฐานรุ่นแรก
- ปิด user/membership แล้วสิทธิ์หยุดมีผล ไม่รอ JWT claims เก่าหมดอายุ
- ให้ token transport ใช้งาน LAN development ได้จริง; หากเลือก body response ต้องเตือน frontend ไม่ log/persist token โดยไม่จำเป็น และกำหนดแนวทาง browser production แบบ HttpOnly cookie + CSRF/SameSite/CORS ใน docs โดยไม่ใช้ Secure cookie บน HTTP LAN แล้วอ้างว่าทำงาน

## 9. API conventions และ Products CRUD

- Bind `0.0.0.0`, port `3000`, prefix `/api/v1`; `/docs` และ `/health` อยู่นอก prefix
- Response success: `{ "success": true, "data": {}, "meta": {}, "requestId": "..." }`
- Response error: `{ "success": false, "error": { "code": "...", "message": "...", "details": null }, "requestId": "..." }`
- 204 ไม่มี body; download/stream และ health ใช้รูปแบบที่เหมาะสมและ document ข้อยกเว้น
- รับ X-Request-Id เฉพาะรูปแบบ/ความยาวที่ปลอดภัย หรือสร้าง UUID ใหม่ ส่งกลับ header และ body ใช้ request context propagation
- DTO ValidationPipe: whitelist, forbidNonWhitelisted, transform; parse boolean/query numbers ชัดเจน ไม่ให้ string `false` กลายเป็น true
- Map validation/Prisma errors เป็น 400/401/403/404/409/422 ตาม semantics ไม่ส่ง internal SQL/stack/secret
- Swagger มี request/response DTO, auth header, company header, decimal strings, pagination และ error examples ตรงพฤติกรรมจริง

Product fields: UUID, companyId, code, barcode nullable, name, description nullable, unit, price Decimal, cost Decimal nullable, active, version, createdAt, updatedAt, deletedAt nullable

Endpoints: POST/GET `/api/v1/products`, GET/PATCH/DELETE `/api/v1/products/:id`

- Soft Delete ไม่แสดงใน query ปกติ; PATCH/DELETE ต้อง scoped; optimistic version conflict เป็น 409
- Pagination page=1, pageSize=20 สูงสุด 100 พร้อม total/totalPages
- Search code/name/barcode, active filter, sortBy allowlist และ sortOrder; มี stable secondary sort
- เลือกเฉพาะ field ที่จำเป็น ไม่มี N+1/unlimited list
- Product create/update/delete + Audit + Outbox ต้อง atomic
- ใช้ product.updated เป็น integration event ตัวอย่างที่ทำงานจริง

## 10. Transactions, Idempotency และ Concurrency

ตัวอย่างธุรกรรมหลักที่ต้อง implement คือสร้าง Company → Head Office → Default Warehouse รวม Audit/Outbox

- รับ Idempotency-Key สำหรับ provisioning company/branch และคำสั่งที่เหมาะสม เก็บ actor/operation/scope/request hash และผลใน DB
- Key เดิม payload เดิมไม่สร้างซ้ำ; key เดิม payload ต่างให้ 409; มีการจัดการ in-progress และ expiry ที่ชัดเจน
- ใช้ transaction/locking หรือ serializable + bounded retry ตาม use case ไม่ทำ read-modify-write ที่ไม่มีการป้องกัน
- Product update ใช้ version predicate ป้องกัน lost update
- การรับเข้าคลังอนาคตต้องมี public inventory application interface และ transaction strategy เอกสารเท่านั้นในงานนี้ ไม่ implement stock adjustment เพื่อใช้เป็น demo
- อย่าเรียก network/NATS/object storage ภายใน DB transaction ที่ต้องถือ lock นาน

## 11. Cache, BullMQ และ Workers

### Valkey cache

- Cache port: get/set/delete/TTL, prefix มี environment/company/resource เช่น `dev:company:{id}:product:{id}`
- Cache เป็น optimization; timeout สั้น + fallback DB เมื่อ cache unavailable
- ไม่ cache สิทธิ์ที่ revoke แล้วโดยไม่มี invalidation strategy
- ไม่ใช้ production eviction policy ของ cache แบบสุ่มกับ BullMQ data; หากใช้ instance เดียว local ให้ตั้ง noeviction/volume และบันทึกแผนแยก cache กับ queue datastore ใน production เมื่อเหมาะสม

### BullMQ

- Queue: notification, report, integration, sync พร้อม typed payload และ scope/request correlation
- Worker อยู่ repository/image เดียวกัน แต่มี entrypoint แยก รองรับ API และ worker process/container แยกโดยไม่ rewrite
- งานตัวอย่างที่ต้องรันจริงเป็น local diagnostic/report artifact หรือ local notification sink ไม่ส่งข้อความจริง
- Retry/backoff, timeout, bounded concurrency, failed-job handling, retention และ graceful close
- Durable job intent บันทึกผ่าน outbox ก่อน enqueue; Queue ล่มให้ job รอ ไม่คืนว่าส่งสำเร็จ
- jobId ช่วยลดซ้ำ แต่ side effects ยังต้องมี durable idempotency รองรับ retry/crash

## 12. Event Bus, JetStream, Outbox และ Inbox

- EventBus port มี publish/subscribe abstraction แยก NATS adapter จาก business logic
- ใช้ JetStream สำหรับ event ที่ต้องไม่สูญหาย อย่าใช้ Core NATS fire-and-forget เป็นหลักฐานว่าธุรกรรมถูกส่งครบ
- Envelope: eventId, eventName, version, occurredAt, correlationId, causationId ถ้ามี, companyId, aggregateId/aggregateVersion และ data ที่ผ่าน schema validation
- Outbox record บันทึก transaction เดียวกับ business change และ Audit ที่จำเป็น
- Dispatcher claim งานอย่างปลอดภัย เช่น FOR UPDATE SKIP LOCKED พร้อม lease/recovery ส่งพร้อม publish acknowledgement แล้วค่อย mark sent
- Retry transient errors พร้อม backoff; poison message มีสถานะ failed/quarantine และขั้นตอน replay ไม่ retry เร็วไม่สิ้นสุด
- Durable consumer/explicit acknowledgement; ack หลัง local transaction ของ consumer สำเร็จ
- Inbox unique `(consumerName, eventId)` และผลการประมวลผลบันทึก transaction เดียวกัน เพื่อไม่ทำ side effects ซ้ำ
- ไม่อ้าง exactly-once end-to-end: ออกแบบสำหรับ at-least-once + idempotent handling รวมกรณี crash หลัง publish ก่อน mark sent
- รองรับ event schema versioning และไม่สมมติ global ordering; aggregate version ใช้ตรวจ out-of-order ตาม use case
- ทดสอบ broker unavailable → business commit สำเร็จพร้อม outbox pending → broker กลับมา → ส่งและประมวลผลได้โดยไม่ซ้ำ

## 13. Reports และ Dashboard foundation

- Report data access แยกจาก CRUD repository ใช้ parameterized SQL/View
- ใน Foundation สร้าง `/api/v1/reports/products-summary` จากข้อมูล Product จริงเพื่อพิสูจน์ tenant filter, SQL, cache และ read routing ไม่สร้าง sales-summary ด้วยยอดปลอม
- Materialized View ให้มีตัวอย่าง migration/refresh strategy ถ้ามีประโยชน์ ไม่ refresh aggregation ทุก request และไม่จำเป็นต้องใช้กับ query เล็กทุกตัว
- Cache TTL 30–60 วินาทีสำหรับ summary มี generatedAt/asOf และ key ตาม tenant/filter
- เตรียม docs สำหรับ PO Summary, Outstanding Delivery, Delivery Variance และ Confirmed Delivery Awaiting Warehouse Receipt ในงานถัดไป
- ไม่เปิด Stock Balance ที่แสดง 0 เสมือนเป็นข้อมูลจริงก่อนโมดูลคลังพร้อม

## 14. Storage, Audit, Logging และ Security

### Storage

- Storage port: upload/delete/getSignedUrl; adapter local dev และ S3-compatible สำหรับ Spaces
- Local dev ใช้ mounted volume ไม่เก็บถาวรเฉพาะ writable container layer
- ไฟล์ private, opaque key, tenant prefix, authorization ก่อนออก signed URL, expiry, size/type validation และป้องกัน path traversal
- Local signed URL ต้องมี verification จริง ไม่คืน public path แล้วเรียกว่า signed URL
- S3 adapter ทดสอบผ่าน local mock/emulator ได้ หากไม่มี Spaces credential ให้รายงาน live integration ว่ายังไม่ยืนยัน

### Audit

- AuditLog: id, actor/userId nullable, companyId nullable, action, entityType, entityId, beforeData/afterData แบบ allowlist, ipAddress, userAgent, requestId, createdAt
- CREATE/UPDATE/DELETE/PERMISSION_CHANGE สำคัญต้อง atomic กับ mutation; LOGIN success/failure มี audit ที่ไม่เปิดเผย credential หรือระบุตัวตนผิด
- ไม่ serialize ทั้ง User/Session/HTTP request ลง audit; redact secrets/token/passwordHash
- จำกัดสิทธิ์อ่านและป้องกัน user ปกติแก้/ลบ Audit; ข้อมูล global login audit ไม่เปิดให้ tenant admin เห็นข้ามบริษัท

### Logging/security

- Pino structured JSON: timestamp, level, requestId, method, path ที่ตัด query sensitive, statusCode, duration, userId/companyId เมื่อผ่านการตรวจแล้ว
- ไม่ log request/response body ทั้งก้อน auth, authorization/cookie header, token, secret, signed URL query หรือ DATABASE_URL
- Helmet, exact allowlist CORS, bounded payload size, DTO validation, timeout, rate limit และ configured trust proxy
- ถ้า distributed rate limiter ล่ม ให้มีนโยบาย fallback ที่ป้องกัน login abuse ไม่ปล่อย unlimited เงียบ ๆ
- Swagger development เปิดได้; production disable เป็นค่าเริ่มต้นและมีวิธี protect ก่อนเปิด
- Health public ไม่เปิดเผย secrets, internal hosts หรือ exception stack

## 15. Environment และ fail-fast configuration

สร้าง `.env.example` ด้วย placeholders ไม่มีรหัสผ่านใช้งานได้จริง รวมอย่างน้อย:

```text
NODE_ENV
PORT
DATABASE_URL
DATABASE_WRITE_URL
DATABASE_READ_URL
DATABASE_MIGRATION_URL
POSTGRES_DB
POSTGRES_USER
POSTGRES_PASSWORD
JWT_ACCESS_SECRET
JWT_REFRESH_SECRET
JWT_ACCESS_EXPIRES_IN
JWT_REFRESH_EXPIRES_IN
JWT_ISSUER
JWT_AUDIENCE
ADMIN_SEED_PASSWORD
REDIS_HOST
REDIS_PORT
REDIS_PASSWORD
REDIS_KEY_PREFIX
NATS_URL
NATS_USER
NATS_PASSWORD
CORS_ORIGINS
LOG_LEVEL
SWAGGER_ENABLED
STORAGE_DRIVER
STORAGE_LOCAL_PATH
STORAGE_SIGNING_SECRET
S3_ENDPOINT
S3_REGION
S3_BUCKET
S3_ACCESS_KEY_ID
S3_SECRET_ACCESS_KEY
DATABASE_TEST_URL
```

- Required/optional/conditional ระบุใน docs; read URL optional, S3 credentials required เฉพาะ adapter S3, seed password required เฉพาะ explicit seed command
- Secrets access/refresh ต้องต่างกันและความยาวเพียงพอ ไม่ใช้ค่าตัวอย่าง production; fail-fast ข้อมูลจำเป็นผิด/หาย โดยไม่พิมพ์ค่าลับ
- รองรับ development/test/staging/production ผ่าน config module กลาง ไม่กระจาย NODE_ENV checks
- local setup script อาจสร้าง secrets แบบสุ่มเขียน `.env` permission 0600 ได้เมื่อไฟล์ยังไม่มี ห้ามเขียนทับไฟล์เดิมหรือ echo secret
- ห้าม commit `.env`; ห้าม COPY ลง Docker image

## 16. Docker และการรันด้วยคำสั่งเดียว

สร้าง Dockerfile multi-stage, docker-compose.yml, .dockerignore, .gitignore และ profiles/override ตามจำเป็น

หลังเตรียม `.env` แล้ว ต้องรันระบบได้ด้วย:

```bash
docker compose up -d
```

- Services หลัก: api, postgres, valkey, nats; เพิ่ม worker และ one-shot migrate service ได้โดยใช้ repository/image เดียว ไม่ถือเป็นการแยก business microservices
- Long-running services ใช้ restart: unless-stopped; migration one-shot ไม่ตั้ง restart loop
- api/worker รอ migrations สำเร็จ; ไม่รัน migration/seed ในทุก API replica startup
- Production migration เป็น release step แยกต่างหาก ส่วน seed เป็น explicit command ไม่รันทุก restart
- API expose 3000 และ listen 0.0.0.0; database/cache/broker ไม่ publish สู่ LAN
- ถ้าต้องเข้า DB จาก host ให้ localhost-only override เช่น 127.0.0.1 ไม่เปิด 5432 สู่ public
- Network ติดต่อกันด้วย service name; volumes แยก PostgreSQL, Valkey queue persistence, JetStream และ local uploads
- Multi-stage image มี production dependencies เท่านั้น รัน non-root ไม่ฝัง build secrets และใช้ exec-form signal handling
- healthcheck ต้องใช้คำสั่งที่มีอยู่จริงใน image ที่เลือก ไม่สมมติว่ามี curl/bash
- Docker restart ต้องคง DB และ pending job/event data; `down -v` ต้องระบุชัดว่าเป็น destructive และไม่ใช้ตรวจ restart
- UAT/Production แยก compose project/database/bucket/prefix/credentials ไม่ใช้ dev secret

## 17. Health และ Graceful Shutdown

- GET `/health/live`: โปรเซสยังทำงาน ไม่ผูก optional dependency จน restart วน
- GET `/health/ready`: พร้อมรับ core requests และ DB พร้อม; optional cache/broker outage แสดง degraded โดยไม่ปิด core CRUD หาก outbox รับงานได้
- GET `/health`: สรุป API/PostgreSQL/Valkey/NATS พร้อมนโยบาย status code; worker readiness ตรวจ dependency ของ worker โดยเฉพาะ
- จำกัดเวลาตรวจ health ไม่ hang และไม่เปิดเผยข้อมูลเชื่อมต่อ
- SIGTERM/SIGINT: หยุดรับงานใหม่ drain HTTP/worker แบบ bounded ปิด DB, Valkey, queues, NATS subscriptions/connections อย่างถูกลำดับ
- ตั้ง shutdown timeout ให้สัมพันธ์กับ Docker stop_grace_period

## 18. Seed, Swagger และ Documentation

Development seed ต้อง idempotent:

- Company `HOTPOTMAN Demo`, Head Office และคลังหลัก ผ่าน application invariant เดียวกับ API
- Admin username `admin`, password จาก ADMIN_SEED_PASSWORD เท่านั้น ไม่ reset password เดิมทุกครั้งที่ seed
- Company-scoped SUPER_ADMIN พร้อม permissions ของ implemented modules และ sample user สิทธิ์น้อยสำหรับทดสอบ
- Development seed ห้ามทำงานใน production โดยปริยาย

Swagger `/docs` ต้องทดสอบ login/auth/company header/product CRUD ได้จริง และ generate OpenAPI JSON สำหรับ Frontend ได้

เอกสารที่ต้องมี:

- README.md: setup, env, Docker, migrations, seed, commands, Swagger, LAN, troubleshooting
- docs/architecture.md: module boundaries, ports/adapters และเหตุผล NestJS/Prisma/modular monolith
- docs/api-conventions.md: response/decimal/pagination/company scope/errors
- docs/security.md: auth sessions, refresh races, authorization, CORS/CSRF, secrets, rate limit
- docs/database.md: invariants, constraints, indices, transaction boundaries, role separation, soft delete
- docs/deployment.md: UAT/Production/DigitalOcean, migration release, backup/restore และ rollback compatibility
- docs/microservices-roadmap.md: เงื่อนไขที่ควร extract notification/integration/report ก่อน inventory/order โดยไม่ใช้ distributed transaction เสมือน local transaction
- docs/hotpotman-domain-contracts.md: PO/delivery/warehouse separation และตัวอย่างสั่ง 10 ส่ง 8
- docs/verification.md: ผลรันจริง คำสั่ง ผลผ่าน/ไม่ผ่าน/ยังไม่ทดสอบ พร้อมข้อจำกัด

DigitalOcean topology ต้องแสดง API/Worker เชื่อม PostgreSQL, Valkey, NATS และ Spaces แบบบริการคู่ขนาน ไม่วาดเป็น chain DB → Cache → Broker → Storage และเลือก deployment baseline ที่เรียบง่าย เช่น containers + managed services โดยไม่บังคับเริ่ม Kubernetes

## 19. LAN development

README ต้องอธิบาย:

```text
NEXT_PUBLIC_API_URL=http://192.168.1.122:3000/api/v1
```

IP เป็นตัวอย่าง ให้รายงาน IP ที่ตรวจพบจริงและเตือนว่า DHCP อาจเปลี่ยน แนะนำ DHCP reservation เมื่อเหมาะสม

- CORS ต้องรวม origin ของ frontend จริง ไม่ใช่ API URL และไม่ใช้ wildcard พร้อม credentials
- ถ้า host เป็น macOS ให้แนวทาง firewall macOS; Windows ใช้ TCP 3000 เฉพาะ Private Network ไม่เปลี่ยน firewall อัตโนมัติหรือแนะนำปิด firewall
- Localhost ผ่านไม่ได้พิสูจน์ LAN ผ่าน ต้องทดสอบจากเครื่องอื่นจริงหรือระบุว่ายังรอทดสอบ

## 20. Testing และ Code Quality

ใช้ Jest + integration/e2e กับ PostgreSQL จริงในฐานทดสอบแยก ไม่ใช้ SQLite และห้าม reset DB dev/production

- test runner ตรวจชื่อ/URL test DB และ refuse destructive reset เมื่อไม่ใช่ฐานทดสอบที่กำหนด
- ใช้ fake adapters สำหรับ unit tests และ infrastructure จริงสำหรับ integration tests ที่อ้างว่าผ่าน
- ESLint, Prettier, strict TypeScript, module-boundary checks
- pnpm scripts: dev, build, start, start:prod, start:worker, lint, format, test, test:e2e, prisma:generate, prisma:migrate, prisma:deploy, prisma:seed

กรณีทดสอบที่ต้องมี:

1. live/ready/health รวม dependency degraded
2. login ด้วย username/email, wrong password, inactive user/membership
3. refresh rotation, reuse, concurrent refresh, logout/session revocation
4. products create/list/get/update/soft-delete, search/filter/sort/pagination/decimal
5. invalid DTO, forbidden fields, pageSize limit, boolean false, permission denied
6. tenant isolation รวม guessed UUID, report query, role assignment และ file access
7. บริษัท/สำนักงานใหญ่/คลัง atomic; rollback กลางทาง; simultaneous/idempotent requests
8. ข้อห้ามลบ/ปิด/ย้ายสำนักงานใหญ่ และคลังหลัก ผ่าน API และ DB constraint ด้วย runtime role
9. product version conflict และ Audit/Outbox atomicity
10. cache outage fallback, BullMQ enqueue/process/retry ไม่ส่งข้อความจริง
11. JetStream publish/consume, duplicate event deduplication และ broker outage recovery
12. parameterized report query, tenant filter และ cache keys ไม่ปะปน
13. storage adapter authorization/path traversal; S3 mock และ live test แยกสถานะ
14. restart containers แล้วข้อมูลและ session ที่ยังมีผลคงอยู่
15. log/error/audit ไม่มี credential/token/passwordHash และ production ไม่คืน stack

## 21. ลำดับดำเนินงานและหลักฐานการเสร็จงาน

1. ตรวจ cwd, git status, AGENTS.md, Node/pnpm/Docker/Compose/Git, port usage และไฟล์เดิม
2. หากอยู่ใน repository เอกสาร requirements ให้สร้าง Backend ในโฟลเดอร์ย่อยใหม่ที่เหมาะสม เช่น hotpotman-backend และแจ้ง path อย่าเปลี่ยนโฟลเดอร์เอกสารเป็น package root หรือทับเอกสารเดิม
3. ตรวจ official compatibility เลือก/pin versions และบันทึก decisions
4. Implement config/domain/schema/invariants/auth/scope/products/infrastructure/tests/docs ตามลำดับที่ dependency ต้องใช้
5. Install ด้วย pnpm, generate Prisma Client, build image และรัน Compose
6. Deploy migration และ explicit development seed จาก environment
7. ตรวจ container health, /health, /docs, login, refresh, me, permissions และ CRUD จริง
8. ทดสอบองค์กร/สิทธิ์/SQL report/queue/event/cache outage และ restart persistence
9. Run lint, unit/integration/e2e และ production build แก้จนผ่าน
10. ตรวจ LAN จากเครื่องอื่นเมื่อเข้าถึงเครื่องทดสอบได้ มิฉะนั้นระบุว่า host/LAN-IP test ผ่านเท่าไรและ external LAN test ยังไม่ยืนยัน
11. เก็บ verification โดยตัด secrets พร้อมสิ่งที่เป็น placeholder และขั้นตอนต่อไป

งาน Foundation ถือว่าสำเร็จเมื่อ Compose services healthy, migrations/seed ผ่าน, auth/session/permissions ใช้งานจริง, organization invariants ผ่าน, Product CRUD/report ผ่าน, cache/queue/JetStream/outbox ผ่าน, lint/tests/build ผ่าน และ restart แล้วข้อมูลยังอยู่

การทดสอบที่ต้องพึ่งบริการ/อุปกรณ์ภายนอก เช่น LAN อีกเครื่องหรือ DigitalOcean Spaces จริง ให้แยก “ยังไม่ทดสอบ” อย่างตรงไปตรงมา ไม่ยกระดับ local mock เป็นหลักฐาน production

## 22. รูปแบบรายงานสุดท้าย

สรุปเป็นภาษาไทย กระชับแต่มีหลักฐาน:

- Architecture, project path และ modules ที่ implement จริง
- Containers, ports, database และบริการที่รันจริง
- Swagger/health/local/LAN API URLs พร้อมสถานะทดสอบ
- วิธีเริ่มระบบ migration/seed/test/build และตำแหน่งเอกสาร
- Username ของ development admin และวิธีที่ผู้ใช้เข้าถึง/ตั้ง password ผ่าน `.env` โดยไม่แสดง password
- ผล lint/tests/build และกรณีสำคัญที่ผ่าน/ไม่ผ่าน/ยังไม่ตรวจ
- Placeholders และข้อจำกัดที่ยังเหลือ
- งานถัดไปของ HOTPOTMAN: Supplier/หน่วย/ราคา → PO → Delivery Confirmation → รายงาน/Dashboard → ชั่งรับเข้าคลังในเฟสถัดไป

ห้ามสรุปว่า Phase 1 ของ HOTPOTMAN เสร็จทั้งหมดเมื่อเสร็จเพียง Foundation และห้ามสรุปว่า deploy production แล้วจากการรัน Docker local

## 23. แหล่งอ้างอิงทางการที่ต้องตรวจเวอร์ชันอีกครั้งเมื่อลงมือ

- NestJS documentation: https://docs.nestjs.com/
- NestJS NATS transporter: https://docs.nestjs.com/microservices/nats
- Prisma documentation: https://www.prisma.io/docs
- Prisma transactions: https://docs.prisma.io/docs/orm/v7/prisma-client/queries/transactions
- NATS/JetStream documentation: https://docs.nats.io/
- BullMQ documentation: https://docs.bullmq.io/
- Docker documentation: https://docs.docker.com/

หลักการที่ตรวจประกอบการออกแบบแล้วคือ Prisma transaction ต้องใช้ร่วมกับการออกแบบ concurrency/idempotency และ Core NATS ไม่ใช่ durable event delivery แทน JetStream แต่เวอร์ชันและ API ที่ติดตั้งจริงต้องตรวจใหม่ ณ วัน implement ไม่ยึดตัวอย่างจากคนละ major version
