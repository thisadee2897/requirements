# AppWeighing

**แผนพัฒนา Android Full Application เชื่อมต่อ TRCloud ระยะเวลา 15 วัน**

## 1. ข้อมูลโครงการ

- **โครงการ:** AppWeighing
- **แนวทาง:** พัฒนา Native Android Application และ SUNFORD Integration API ใหม่ทั้งหมด
- **วันเริ่มพัฒนา:** วันจันทร์ที่ 7 กันยายน 2026 (พ.ศ. 2569)
- **วันส่งมอบเวอร์ชัน UAT:** วันจันทร์ที่ 21 กันยายน 2026 (พ.ศ. 2569)
- **วันทำงาน:** วันจันทร์ถึงวันเสาร์ หยุดเฉพาะวันอาทิตย์
- **ระยะเวลาโครงการ:** 15 วันตามปฏิทิน
- **จำนวนวันพัฒนาจริง:** 13 วันทำการ
- **ทีมพัฒนา:** Developer A และ Developer B
- **กำลังพัฒนารวม:** 2 Developers x 13 วัน = 26 Developer-Days
- **ผลลัพธ์ปลายทางของแผน:** APK/AAB เวอร์ชัน UAT, Integration API, ผลทดสอบ และเอกสารส่งมอบสำหรับให้ลูกค้าทดสอบ

แผนนี้ใช้ขอบเขตจากเอกสาร Requirements ของ Full Application โดยยึดวันเริ่ม วันสิ้นสุด และวันหยุดที่ผู้ว่าจ้างยืนยันล่าสุดเป็นข้อมูลหลักเมื่อข้อความเดิมไม่ตรงกัน

เอกสารไฟล์นี้รวมทั้งแผนพัฒนาระยะเวลา 15 วัน, แบบฟอร์มชื่อแอปและสี RGB รวมถึง **TRCloud API Contract v1 จำนวน 6 Endpoints ในหัวข้อ 14** โดย TRCloud ต้องทำ Endpoint, Field, Validation, Error Code และ Idempotency ตาม Contract ที่ SUNFORD กำหนด

## 2. ปฏิทินการทำงาน

| วันทำการ | วันที่ | เป้าหมายหลัก |
|---:|---|---|
| วันที่ 1-5 | จันทร์ 7 - ศุกร์ 11 กันยายน 2026 | วางระบบ, Login/Branch, Search SKU, Item Detail และเริ่ม Weighing |
| วันที่ 6-10 | เสาร์ 12 - พฤหัสบดี 17 กันยายน 2026 | Weighing Result, SN/QR Code, Label, Scan Receive, Stock Transfer, Waste/Yield และการป้องกันข้อมูลสูญหาย |
| วันที่ 11-13 | ศุกร์ 18 - จันทร์ 21 กันยายน 2026 | Retry, Security, Integration Test, UAT, แก้ไข และส่งมอบ |

วันที่นับเป็นวันพัฒนามีดังนี้:

1. วันจันทร์ที่ 7 กันยายน 2026
2. วันอังคารที่ 8 กันยายน 2026
3. วันพุธที่ 9 กันยายน 2026
4. วันพฤหัสบดีที่ 10 กันยายน 2026
5. วันศุกร์ที่ 11 กันยายน 2026
6. วันเสาร์ที่ 12 กันยายน 2026
7. วันจันทร์ที่ 14 กันยายน 2026
8. วันอังคารที่ 15 กันยายน 2026
9. วันพุธที่ 16 กันยายน 2026
10. วันพฤหัสบดีที่ 17 กันยายน 2026
11. วันศุกร์ที่ 18 กันยายน 2026
12. วันเสาร์ที่ 19 กันยายน 2026
13. วันจันทร์ที่ 21 กันยายน 2026

> การคำนวณข้างต้นนับวันจันทร์ถึงวันเสาร์และหยุดเฉพาะวันอาทิตย์ที่ 13 และ 20 กันยายน 2026 วันหยุดนักขัตฤกษ์หรือวันหยุดบริษัทอื่นภายในช่วงนี้ให้นับเป็นวันทำงานตามแผน หากเกิดการรอ API, Credential, อุปกรณ์ หรือการยืนยันงาน ให้บันทึกเป็น Blocker และประเมินผลกระทบต่อวันส่งมอบทันที

## 3. ขอบเขตหลักภายในระยะเวลาโครงการ 15 วัน

1. Native Android Application
2. Login, User Profile, Permission, Company และ Branch
3. Search SKU และ Item Detail จาก TRCloud
4. การรับน้ำหนักจากเครื่องชั่งที่ SUNFORD เลือกและเชื่อมต่อ
5. Create Weighing Record
6. Record ID, SN, QR Code และ Barcode ที่ Encode ค่า SN
7. Label Preview, Print และ Reprint ขนาด `6 × 4 cm` โดยแสดงเฉพาะชื่อสินค้า, วันที่–เวลาบันทึก, QR Code และ Barcode
8. Scan QR Code หรือกรอก SN เพื่อรับสินค้าเข้าและโอน Stock มายังสาขาที่สแกน
9. Create Waste Weighing Record
10. Net Yield Weight และ Yield Percentage
11. SUNFORD Integration API สำหรับเชื่อมต่อ TRCloud
12. Local Database, Transaction State, Network Error Handling และ Retry
13. Idempotency, Permission, Audit Log และ Error Mapping
14. Integration Test กับอุปกรณ์จริง
15. UAT, แก้ไขข้อผิดพลาดสำคัญ และส่ง APK/AAB เวอร์ชัน UAT

แอปพลิเคชันต้องเชื่อมต่ออินเทอร์เน็ตและเข้าถึง SUNFORD Integration API ได้ตลอดการใช้งาน ฟังก์ชันทั้งหมดเปิดใช้งานเมื่อเชื่อมต่อระบบสำเร็จเท่านั้น

## 4. เงื่อนไขเริ่มงานและการส่งมอบข้อมูลระหว่างพัฒนา

ข้อมูลในหัวข้อ 4.1 และ Technical Contact ของ TRCloud ต้องพร้อมเมื่อเริ่มงานวันจันทร์ที่ 7 กันยายน 2026 ส่วน TRCloud API ให้ส่งมอบเป็นช่วงตามหัวข้อ 4.3 ระหว่างการพัฒนา โดยการสรุป UI เป็นงานของวันที่ 1-3 และไม่ต้องรอ UI ฉบับสมบูรณ์ก่อนเริ่มวันที่ 1

### 4.1 ข้อมูลและการตัดสินใจ

- ยืนยันขอบเขต Full Application และ User Flow หลัก
- รวบรวมหน้าจอ, Wireframe หรือ Brand Reference ที่มีอยู่เพื่อใช้เริ่มออกแบบ โดยการสรุป UI เป็นงานของวันที่ 1-3
- ชื่อแอปที่ยืนยันแล้วคือ `AppWeighing`
- ทางบริษัทกำหนดและส่งรหัสสี RGB สำหรับ Theme ของแอป
- ส่ง App Icon, Logo หรือแนวทาง Splash Screen ถ้ามี; หากยังไม่มีให้ใช้ Placeholder และยืนยันแบบภายในวันที่ 1-3
- ยืนยันบริษัท, สาขา, ผู้ใช้งาน และ Permission ที่ต้องรองรับ
- ยืนยันให้ใช้ Field Mapping ตาม TRCloud API Contract v1 ในหัวข้อ 14; การเปลี่ยนแปลงต้องได้รับอนุมัติจาก SUNFORD
- ใช้กฎ Record ID, SN, QR Code และ Barcode ตาม TRCloud API Contract v1 ในหัวข้อ 14 โดย QR Code และ Barcode ต้อง Encode ค่า SN เดียวกัน
- ใช้สูตร Yield, หน่วย `KG`, จำนวนทศนิยม และหลักการปัดเศษตาม TRCloud API Contract v1 ในหัวข้อ 14
- ยืนยันเกณฑ์ UAT และชื่อผู้รับผิดชอบอนุมัติผล

#### แบบฟอร์มข้อมูลชื่อแอปและ Theme ที่ทางบริษัทต้องส่งให้ทีมพัฒนา

| รายการ | ข้อมูลที่ทางบริษัทกำหนด |
|---|---|
| ชื่อแอปภาษาไทย | `AppWeighing` |
| ชื่อแอปภาษาอังกฤษ | `AppWeighing` |
| สีหลักของแอป (Primary) | `R: ___, G: ___, B: ___` |
| สีรองของแอป (Secondary) | `R: ___, G: ___, B: ___` |
| สีเน้นหรือสีของปุ่มหลัก (Accent/Action) | `R: ___, G: ___, B: ___` |
| สีพื้นหลังหลัก (Background) | `R: ___, G: ___, B: ___` |
| สีตัวอักษรหลัก (Primary Text) | `R: ___, G: ___, B: ___` |

ทางบริษัทต้องส่งค่า RGB เป็นตัวเลขตั้งแต่ 0-255 ให้ครบทั้ง Red, Green และ Blue พร้อมตัวอย่าง Logo หรือ Brand Guideline ถ้ามี ทีมพัฒนาจะใช้ค่าที่ได้รับเป็น Theme ตั้งต้นของแอปตั้งแต่วันที่ 1 และการเปลี่ยนชื่อหรือสีหลักภายหลังอาจกระทบงาน UI, App Icon, Splash Screen และรอบทดสอบ

#### 4.1.1 Deadline ข้อมูลที่ทางบริษัทต้องส่งให้ SUNFORD

กำหนดเวลาทั้งหมดใช้เขตเวลา `Asia/Bangkok` และถือว่าส่งครบเมื่อ SUNFORD ได้รับข้อมูลที่เปิดใช้งานหรือทดสอบได้จริง ไม่ใช่เพียงข้อความแจ้งว่าจะส่งภายหลัง

| Deadline | ผู้รับผิดชอบ | ข้อมูลที่ต้องส่ง | เกณฑ์ว่าส่งครบ |
|---|---|---|---|
| จันทร์ 7 กันยายน 2026 เวลา 09:00 น. | ทางบริษัท | ยืนยันชื่อ `AppWeighing`, ค่า RGB ทั้ง 5 รายการ, Logo/App Icon/Brand Reference ถ้ามี และชื่อผู้มีอำนาจยืนยันงาน | ชื่อแอปตรงกับ `AppWeighing`, ค่า RGB ครบ `R/G/B` ช่วง 0-255 และไฟล์ Brand เปิดใช้งานได้ |
| จันทร์ 7 กันยายน 2026 เวลา 12:00 น. | ทางบริษัท | รายชื่อบริษัทและสาขาที่ใช้จริง, สาขาต้นทาง/สาขารับสำหรับ Test, รายชื่อกลุ่มผู้ใช้ และ Permission ที่แต่ละกลุ่มต้องมี | มีรายการ Company/Branch/User Role ที่ตรวจสอบ Mapping กับข้อมูล TRCloud ได้ |
| อังคาร 8 กันยายน 2026 เวลา 12:00 น. | ทางบริษัท | SKU และชื่อสินค้าตัวอย่างสำหรับ UAT, ตัวอย่าง Flow ย้ายสาขา และผลลัพธ์ที่คาดหวัง | มี SKU อย่างน้อย 1 รายการ และมี Source/Receiving Branch คนละสาขาสำหรับทดสอบครบ Flow |
| ศุกร์ 18 กันยายน 2026 เวลา 12:00 น. | ทางบริษัท/ผู้ดูแลจุด UAT | รายชื่อผู้ทดสอบ UAT, ผู้มีอำนาจยืนยันผล, ช่องทางติดต่อ, ยืนยันช่วงทดสอบวันที่ 21 กันยายน และเตรียมอุปกรณ์ Android ที่มีกล้องพร้อมเครือข่ายอินเทอร์เน็ต | ระบุ Tester, Approver และช่วงเวลาที่พร้อมทดสอบ พร้อมยืนยันว่าอุปกรณ์และเครือข่าย ณ จุด UAT ใช้งานได้ |
| จันทร์ 21 กันยายน 2026 ภายในเวลา 16:00 น. | ทางบริษัท | ผล UAT, รายการ Pass/Fail และหลักฐานหรือหมายเหตุจากผู้ทดสอบ | ผู้มีอำนาจยืนยันผล UAT และแยก Defect ออกจาก Change Request ชัดเจน |

หากข้อมูลรอบใดส่งไม่ครบ SUNFORD เริ่มหรือเดินงานส่วนที่ไม่ติดข้อจำกัดด้วย Placeholder/Mock ได้ แต่ Milestone ที่อาศัยข้อมูลนั้นไม่ถือว่าผ่าน และผลกระทบต่อกำหนดส่งต้องบันทึกเป็น Blocker

### 4.2 ระบบและสิทธิ์เข้าถึง

- SUNFORD ส่งไฟล์เอกสารฉบับนี้ให้ TRCloud และให้ใช้ API Contract v1 ในหัวข้อ 14 เป็นข้อกำหนดหลัก
- TRCloud แต่งตั้ง Technical Contact สำหรับประสานงานระหว่าง Development, Integration Test และ UAT
- TRCloud ยืนยันรับ Contract v1 และกำหนดส่งมอบ Endpoint ตามหัวข้อ 4.3
- TRCloud จัดเตรียม Sandbox Base URL, Credential และ Test User ตามรอบที่ Endpoint พร้อม
- TRCloud จัดเตรียม Test Data สำหรับ Company, Branch, User, Item และ Source Record
- TRCloud ส่ง OpenAPI 3.1 และ API Collection ที่ตรงกับ Contract
- TRCloud แจ้ง Rate Limit, Maintenance Policy และช่องทางแจ้ง Incident
- Production Base URL และ Production Credential ต้องพร้อมก่อน Production Release แต่ไม่จำเป็นต้องพร้อมก่อนเริ่มวันที่ 1

### 4.3 กำหนดส่งมอบ API จาก TRCloud

กำหนดเวลาทั้งหมดใช้เขตเวลา `Asia/Bangkok` Endpoint จะถือว่าส่งมอบเมื่อเรียกบน Sandbox ได้จริง, Request/Response ตรง Contract, Error เป็น JSON และมี Test Data สำหรับพิสูจน์ Flow

| Deadline | สิ่งที่ TRCloud ต้องส่งมอบ | หลักฐานที่ SUNFORD ใช้ตรวจรับ |
|---|---|---|
| วันที่ 1 - จันทร์ 7 กันยายน 2026 เวลา 12:00 น. | หนังสือ/ข้อความยืนยัน Contract v1, Technical Contact, Sandbox Base URL, วิธี Authentication, Credential และ Test User | SUNFORD Login/เชื่อม Sandbox ได้ และมีผู้รับผิดชอบตอบประเด็น Contract |
| วันที่ 2 - อังคาร 8 กันยายน 2026 เวลา 17:00 น. | API 1 - Login พร้อม User Profile, Permission, Company และ Branch | ทดสอบ Success/Invalid Credential/No Permission และตรวจ JSON Type ผ่าน |
| วันที่ 3 - พุธ 9 กันยายน 2026 เวลา 17:00 น. | API 2 - Search SKU และ API 3 - Get Item by Item ID | ค้น SKU ตัวอย่างและเปิด Item Detail ได้ โดย Response และ JSON Type ตรง Contract |
| วันที่ 5 - ศุกร์ 11 กันยายน 2026 เวลา 17:00 น. | API 4 - Create Weighing Record พร้อมรับ Record ID/SN จากแอปและเพิ่ม Stock ตามน้ำหนัก | ทดสอบ Create, Duplicate และ Idempotency พร้อมตรวจยอดสาขาต้นทาง |
| วันที่ 7 - จันทร์ 14 กันยายน 2026 เวลา 17:00 น. | API 5 - Receive by SN พร้อมสร้าง Receipt และย้าย Stock เข้าสาขาที่ Login | ทดสอบต่างสาขาสำเร็จ, สาขาเดิมถูกปฏิเสธ, Retry ไม่ย้าย Stock ซ้ำ |
| วันที่ 9 - พุธ 16 กันยายน 2026 เวลา 17:00 น. | API 6 - Create Waste Weighing Record พร้อม Transaction ID, Yield และ Finalize SN | ทดสอบสูตร, Branch Permission, Stock Weight และป้องกันการทำซ้ำ |
| วันที่ 11 - ศุกร์ 18 กันยายน 2026 เวลา 12:00 น. | ตรึง Contract ของทั้ง 6 APIs พร้อม OpenAPI 3.1, API Collection, Error Code และ Test Data ฉบับ Integration Test | Schema/Collection ตรงเอกสารและรัน Integration Test ได้ครบ 6 เส้น |
| วันที่ 12 - เสาร์ 19 กันยายน 2026 เวลา 17:00 น. | แก้ Blocker/Critical จาก Integration Test และเตรียมข้อมูล UAT | Retest รายการที่แก้ผ่านและไม่มี Blocker ที่ทำให้ Flow หลักหยุด |
| วันที่ 13 - จันทร์ 21 กันยายน 2026 เวลา 09:00-17:00 น. | Technical Contact พร้อมสนับสนุน UAT, ตรวจ Transaction จริง และแก้ Blocker | UAT Trace จาก Android ถึง TRCloud ได้ด้วย Request/Reference ID |
| ก่อน Production Release อย่างน้อย 2 วันทำงาน | Production Base URL, Production Credential, Rate Limit/Maintenance Policy และผู้ติดต่อ Incident | Production Connectivity/Permission Test ผ่าน โดยไม่ใช้ข้อมูล Secret ในเอกสารหรือ Source Code |

ถ้า TRCloud ส่งรายการใดหลัง Deadline SUNFORD จะเดินงานส่วนที่ไม่ติดข้อจำกัดด้วย Mock Server ตาม Contract v1 แต่ Milestone ที่เกี่ยวข้องจะไม่ถือว่าผ่านจนกว่าจะทดสอบกับ TRCloud Sandbox สำเร็จ เวลาที่ล่าช้าต้องบันทึกเป็น Blocker พร้อม Owner และผลกระทบต่อกำหนดส่ง

### 4.4 อุปกรณ์ที่ SUNFORD รับผิดชอบ

- SUNFORD เป็นผู้เลือก จัดเตรียม และเชื่อมต่อเครื่องชั่ง รวมถึง Protocol, SDK หรือ Driver ที่ใช้
- SUNFORD เป็นผู้เลือก จัดเตรียม และเชื่อมต่อเครื่องพิมพ์ฉลาก รวมถึงคำสั่งพิมพ์, SDK หรือ Driver ที่ใช้
- กำหนด Label Template ขนาด `6 × 4 cm`; แสดงเฉพาะชื่อสินค้า, วันที่–เวลาบันทึก, QR Code และ Barcode โดย SUNFORD รับผิดชอบ Layout และการตั้งค่าตามสื่อฉลากจริง

รุ่นหรือ Protocol ของเครื่องชั่ง รุ่นหรือ Driver ของเครื่องพิมพ์ และรายละเอียดวัสดุฉลากไม่ใช่ข้อมูลที่ต้องรอจากลูกค้าหรือ TRCloud การตัดสินใจและการจัดเตรียมส่วนนี้เป็นความรับผิดชอบของ SUNFORD หากข้อมูลหรืออุปกรณ์ภายในทีมยังไม่พร้อม สามารถพัฒนาด้วย Mock ได้เฉพาะส่วนที่ไม่ติดข้อจำกัด แต่ไม่สามารถปิดผลตรวจรับของฟังก์ชันที่ต้องใช้อุปกรณ์จริงได้

### 4.5 อุปกรณ์และสภาพแวดล้อม ณ จุดใช้งาน/UAT

- อุปกรณ์ Android ที่มีกล้องใช้งานได้ เป็นความรับผิดชอบของทางบริษัทหรือผู้ดูแลจุดใช้งาน/UAT
- เครือข่ายอินเทอร์เน็ตของอุปกรณ์ Android ณ จุดใช้งาน/UAT เป็นความรับผิดชอบของทางบริษัทหรือผู้ดูแลสถานที่
- รายการทั้งสองไม่ใช่อุปกรณ์หรือบริการที่ SUNFORD ต้องจัดหา โดยต้องพร้อมภายในวันศุกร์ที่ 18 กันยายน 2026 เวลา 12:00 น. เพื่อใช้ UAT วันที่ 21 กันยายน

## 5. การแบ่งหน้าที่ทีมพัฒนา

### Developer A - Android Application และอุปกรณ์

- โครงสร้าง Native Android Application
- UI, Navigation และ User Flow
- Login, Branch, Search SKU และ Item Detail ฝั่งแอป
- การเชื่อมต่อเครื่องชั่งและเครื่องพิมพ์
- QR Code Scan, Label Preview และ Print
- Local Database, Transaction State, Network Error และ Retry UI
- Android Device Test, APK/AAB และคู่มือผู้ใช้

### Developer B - Backend, TRCloud Integration และความปลอดภัย

- SUNFORD Integration API
- กำหนดและดูแล `TRCloud API Contract v1`
- สร้าง Mock Server ให้ตรงกับ Contract ระหว่างรอ TRCloud
- TRCloud Authentication และ API Adapter
- Field Mapping และ Error Mapping
- Create/Receive Weighing Record และ Stock Transfer
- Create Waste Weighing Record และ Yield Result
- Record ID, SN, Idempotency และ Transaction Status
- Permission, Audit Log, Secret Management และ API Security
- Integration Test, Deployment Configuration และเอกสาร API

### งานร่วมกัน

- ล็อก Scope และ Acceptance Criteria
- ออกแบบ API Contract ระหว่าง Android กับ Integration API
- Code Review และ Merge งานเข้าชุดทดสอบทุกวัน
- ทดสอบ End-to-End กับ TRCloud และอุปกรณ์จริง
- แก้ไข Defect, Regression Test, UAT และส่งมอบ

## 6. รูปแบบการทำงานประจำวัน

- **09:00 น.:** Daily Stand-up, ตรวจ Blocker และยืนยันเป้าหมายของวัน
- **ช่วงเช้า:** พัฒนางานตาม Owner และทดสอบระดับ Unit/Component
- **13:00 น.:** ทบทวน API Contract, Field Mapping และประเด็นที่กระทบงานข้ามทีม
- **16:00 น.:** รวม Build, ทดสอบ Integration และ Review Code
- **ก่อนจบวัน:** อัปเดตผลสำเร็จ, Defect, Blocker, หลักฐานทดสอบ และเป้าหมายวันถัดไป

งานของแต่ละวันถือว่าเสร็จเมื่อ Code Review ผ่าน, รวมเข้าชุดทดสอบได้, ไม่มี Credential อยู่ใน Source Code, มีผลทดสอบตาม Acceptance Criteria และไม่มี Blocker ที่ไม่ได้ระบุผู้รับผิดชอบ

