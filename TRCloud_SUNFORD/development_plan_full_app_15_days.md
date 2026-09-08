# BaruScan

**แผนพัฒนา Android Full Application เชื่อมต่อ TRCloud ระยะเวลา 15 วัน**

## 1. ข้อมูลโครงการ

- **โครงการ:** BaruScan
- **แนวทาง:** พัฒนา Native Android Application และ SUNFORD Integration API ใหม่ทั้งหมด
- **วันเริ่มพัฒนา:** วันพุธที่ 9 กันยายน 2026 (พ.ศ. 2569)
- **วันส่งมอบเวอร์ชัน UAT:** วันพุธที่ 23 กันยายน 2026 (พ.ศ. 2569)
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
| วันที่ 1-5 | พุธ 9 - จันทร์ 14 กันยายน 2026 | วางระบบ, Login/Branch, Search SKU, Item Detail และเริ่ม Weighing |
| วันที่ 6-10 | อังคาร 15 - เสาร์ 19 กันยายน 2026 | Weighing Result, SN/QR Code, Label, Scan Receive, Stock Transfer, Waste/Yield และการป้องกันข้อมูลสูญหาย |
| วันที่ 11-13 | จันทร์ 21 - พุธ 23 กันยายน 2026 | Retry, Security, Integration Test, UAT, แก้ไข และส่งมอบ |

วันที่นับเป็นวันพัฒนามีดังนี้:

1. วันพุธที่ 9 กันยายน 2026
2. วันพฤหัสบดีที่ 10 กันยายน 2026
3. วันศุกร์ที่ 11 กันยายน 2026
4. วันเสาร์ที่ 12 กันยายน 2026
5. วันจันทร์ที่ 14 กันยายน 2026
6. วันอังคารที่ 15 กันยายน 2026
7. วันพุธที่ 16 กันยายน 2026
8. วันพฤหัสบดีที่ 17 กันยายน 2026
9. วันศุกร์ที่ 18 กันยายน 2026
10. วันเสาร์ที่ 19 กันยายน 2026
11. วันจันทร์ที่ 21 กันยายน 2026
12. วันอังคารที่ 22 กันยายน 2026
13. วันพุธที่ 23 กันยายน 2026

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

ข้อมูลในหัวข้อ 4.1 และ Technical Contact ของ TRCloud ต้องพร้อมเมื่อเริ่มงานวันพุธที่ 9 กันยายน 2026 ส่วน TRCloud API ให้ส่งมอบเป็นช่วงตามหัวข้อ 4.3 ระหว่างการพัฒนา โดยการสรุป UI เป็นงานของวันที่ 1-3 และไม่ต้องรอ UI ฉบับสมบูรณ์ก่อนเริ่มวันที่ 1

### 4.1 ข้อมูลและการตัดสินใจ

- ยืนยันขอบเขต Full Application และ User Flow หลัก
- รวบรวมหน้าจอ, Wireframe หรือ Brand Reference ที่มีอยู่เพื่อใช้เริ่มออกแบบ โดยการสรุป UI เป็นงานของวันที่ 1-3
- ชื่อแอปที่ยืนยันแล้วคือ `BaruScan`
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
| ชื่อแอปภาษาไทย | `BaruScan` |
| ชื่อแอปภาษาอังกฤษ | `BaruScan` |
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
| พุธ 9 กันยายน 2026 เวลา 09:00 น. | ทางบริษัท | ยืนยันชื่อ `BaruScan`, ค่า RGB ทั้ง 5 รายการ, Logo/App Icon/Brand Reference ถ้ามี และชื่อผู้มีอำนาจยืนยันงาน | ชื่อแอปตรงกับ `BaruScan`, ค่า RGB ครบ `R/G/B` ช่วง 0-255 และไฟล์ Brand เปิดใช้งานได้ |
| พุธ 9 กันยายน 2026 เวลา 12:00 น. | ทางบริษัท | รายชื่อบริษัทและสาขาที่ใช้จริง, สาขาต้นทาง/สาขารับสำหรับ Test, รายชื่อกลุ่มผู้ใช้ และ Permission ที่แต่ละกลุ่มต้องมี | มีรายการ Company/Branch/User Role ที่ตรวจสอบ Mapping กับข้อมูล TRCloud ได้ |
| พฤหัสบดี 10 กันยายน 2026 เวลา 12:00 น. | ทางบริษัท | SKU และชื่อสินค้าตัวอย่างสำหรับ UAT, ตัวอย่าง Flow ย้ายสาขา และผลลัพธ์ที่คาดหวัง | มี SKU อย่างน้อย 1 รายการ และมี Source/Receiving Branch คนละสาขาสำหรับทดสอบครบ Flow |
| จันทร์ 21 กันยายน 2026 เวลา 12:00 น. | ทางบริษัท/ผู้ดูแลจุด UAT | รายชื่อผู้ทดสอบ UAT, ผู้มีอำนาจยืนยันผล, ช่องทางติดต่อ, ยืนยันช่วงทดสอบวันที่ 23 กันยายน และเตรียมอุปกรณ์ Android ที่มีกล้องพร้อมเครือข่ายอินเทอร์เน็ต | ระบุ Tester, Approver และช่วงเวลาที่พร้อมทดสอบ พร้อมยืนยันว่าอุปกรณ์และเครือข่าย ณ จุด UAT ใช้งานได้ |
| พุธ 23 กันยายน 2026 ภายในเวลา 16:00 น. | ทางบริษัท | ผล UAT, รายการ Pass/Fail และหลักฐานหรือหมายเหตุจากผู้ทดสอบ | ผู้มีอำนาจยืนยันผล UAT และแยก Defect ออกจาก Change Request ชัดเจน |

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
| วันที่ 1 - พุธ 9 กันยายน 2026 เวลา 12:00 น. | หนังสือ/ข้อความยืนยัน Contract v1, Technical Contact, Sandbox Base URL, วิธี Authentication, Credential และ Test User | SUNFORD Login/เชื่อม Sandbox ได้ และมีผู้รับผิดชอบตอบประเด็น Contract |
| วันที่ 2 - พฤหัสบดี 10 กันยายน 2026 เวลา 17:00 น. | API 1 - Login พร้อม User Profile, Permission, Company และ Branch | ทดสอบ Success/Invalid Credential/No Permission และตรวจ JSON Type ผ่าน |
| วันที่ 3 - ศุกร์ 11 กันยายน 2026 เวลา 17:00 น. | API 2 - Search SKU และ API 3 - Get Item by Item ID | ค้น SKU ตัวอย่างและเปิด Item Detail ได้ โดย Response และ JSON Type ตรง Contract |
| วันที่ 5 - จันทร์ 14 กันยายน 2026 เวลา 17:00 น. | API 4 - Create Weighing Record พร้อมรับ Record ID/SN จากแอปและเพิ่ม Stock ตามน้ำหนัก | ทดสอบ Create, Duplicate และ Idempotency พร้อมตรวจยอดสาขาต้นทาง |
| วันที่ 7 - พุธ 16 กันยายน 2026 เวลา 17:00 น. | API 5 - Receive by SN พร้อมสร้าง Receipt และย้าย Stock เข้าสาขาที่ Login | ทดสอบต่างสาขาสำเร็จ, สาขาเดิมถูกปฏิเสธ, Retry ไม่ย้าย Stock ซ้ำ |
| วันที่ 9 - ศุกร์ 18 กันยายน 2026 เวลา 17:00 น. | API 6 - Create Waste Weighing Record พร้อม Transaction ID, Yield และ Finalize SN | ทดสอบสูตร, Branch Permission, Stock Weight และป้องกันการทำซ้ำ |
| วันที่ 11 - จันทร์ 21 กันยายน 2026 เวลา 12:00 น. | ตรึง Contract ของทั้ง 6 APIs พร้อม OpenAPI 3.1, API Collection, Error Code และ Test Data ฉบับ Integration Test | Schema/Collection ตรงเอกสารและรัน Integration Test ได้ครบ 6 เส้น |
| วันที่ 12 - อังคาร 22 กันยายน 2026 เวลา 17:00 น. | แก้ Blocker/Critical จาก Integration Test และเตรียมข้อมูล UAT | Retest รายการที่แก้ผ่านและไม่มี Blocker ที่ทำให้ Flow หลักหยุด |
| วันที่ 13 - พุธ 23 กันยายน 2026 เวลา 09:00-17:00 น. | Technical Contact พร้อมสนับสนุน UAT, ตรวจ Transaction จริง และแก้ Blocker | UAT Trace จาก Android ถึง TRCloud ได้ด้วย Request/Reference ID |
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
- รายการทั้งสองไม่ใช่อุปกรณ์หรือบริการที่ SUNFORD ต้องจัดหา โดยต้องพร้อมภายในวันจันทร์ที่ 21 กันยายน 2026 เวลา 12:00 น. เพื่อใช้ UAT วันที่ 23 กันยายน

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

## 7. แผนพัฒนารายวัน

## วันที่ 1 - พุธที่ 9 กันยายน 2026

### เป้าหมาย

เริ่มโครงการ, ล็อก Technical Baseline และสร้างโครงระบบ Android กับ Integration API ให้พร้อมพัฒนาคู่ขนาน

### Developer A

- สร้างโครง Native Android Application
- แยก Environment สำหรับ Development และ UAT
- วางโครง Navigation ของหน้าจอทั้งหมด
- ตั้งชื่อแอปเป็น `BaruScan`
- สร้าง Theme, Typography, Color และ Component พื้นฐานจากรหัสสี RGB ที่ทางบริษัทส่งมอบ
- สร้างโครงหน้าจอ Login, Branch, Search, Weighing, Label, Scan Receive, Waste/Yield, History และ Transaction Status
- เตรียมสถานะ Loading, Empty, Success, Error และ Retry

### Developer B

- สร้างโครง SUNFORD Integration API
- แยก Configuration สำหรับ Development และ UAT
- วางระบบ Secret Management เพื่อไม่เก็บ TRCloud Credential ในแอป
- สร้าง Health Check, Logging Structure และ Correlation ID
- สรุป API Contract รุ่นแรกระหว่าง Android App กับ Integration API
- ส่งและตรึง TRCloud API Contract v1 พร้อม Endpoint, Authentication, Field Mapping และ Error Code ที่ TRCloud ต้องทำตาม
- สร้าง Mock Server ตาม Contract เพื่อไม่ให้ Android ต้องรอ Endpoint จริง

### งานร่วมและการตรวจรับประจำวัน

- ทบทวน Scope และ Flow ตั้งแต่ Login ถึง Waste/Yield Result
- ล็อกกฎที่กระทบโครงสร้างข้อมูล: Branch, Weight Unit, Record ID, SN, QR Code และ Yield
- ให้ TRCloud ยืนยันรับ Contract v1, Technical Contact และกำหนดส่งมอบ Sandbox
- สร้างรายการ Test Scenario และ Traceability ระหว่าง Requirement กับ Test Case
- Android App เปิดได้และเปลี่ยนหน้า Skeleton ได้
- Integration API เริ่มระบบและตอบ Health Check ได้
- API Contract v1, Mock Server และรายการประเด็นค้างได้รับการบันทึกชัดเจน

### ผลลัพธ์สิ้นวัน

- Android และ Integration API Foundation
- Navigation Skeleton
- TRCloud API Contract v1 และ Mock Server รุ่นแรก
- Technical Decision Log และ Test Scenario ชุดแรก

## วันที่ 2 - พฤหัสบดีที่ 10 กันยายน 2026

### เป้าหมาย

ทำ Login, Session, User Profile, Permission, Company และ Branch ให้เชื่อมต่อกันได้

### Developer A

- พัฒนาหน้า Login และ Validation
- จัดการ Loading, Login Failed, Session Expired และ No Permission
- จัดเก็บ Session Token ในพื้นที่ปลอดภัยของ Android
- พัฒนาหน้าเลือก Company/Branch สำหรับผู้ใช้หลายสาขา
- แสดง Company/Branch ปัจจุบันในบริบทของแอป
- พัฒนา Logout และล้าง Session ในเครื่อง

### Developer B

- พัฒนา SUNFORD App Endpoint สำหรับ Login และจัดการ Logout ใน Session ของแอป
- เชื่อม TRCloud Authentication ตาม Contract v1 หรือ Mock Server ระหว่างรอ Sandbox
- แปลง User Profile, Permission, Company และ Branch ที่ได้รับจาก TRCloud Login API ให้ Android ใช้งาน
- ตรวจสอบสิทธิ์ทุกคำขอด้วย User, Company และ Branch Context
- กำหนดอายุ Session และรูปแบบตอบกลับเมื่อ Session หมดอายุ
- ปิดบัง Token, Credential และข้อมูลอ่อนไหวใน Log

### งานร่วมและการตรวจรับประจำวัน

- ทดสอบ Login สำเร็จและไม่สำเร็จ
- ทดสอบผู้ใช้ 1 สาขาและหลายสาขา
- ทดสอบผู้ใช้ไม่มีสิทธิ์เข้าถึงสาขา
- ทดสอบ Session หมดอายุและกลับไปหน้า Login
- ยืนยันว่า Android App ไม่เก็บ TRCloud API Key โดยตรง

### ผลลัพธ์สิ้นวัน

- Flow Login ถึงเลือกสาขาทำงานบนชุดทดสอบ
- Permission Context พร้อมใช้กับทุก Transaction
- ผลทดสอบ Authentication และ Session

## วันที่ 3 - ศุกร์ที่ 11 กันยายน 2026

### เป้าหมาย

ทำ Search SKU และ Item Detail พร้อมปิด Milestone โครงระบบและ UI หลัก

### Developer A

- พัฒนาหน้า Search SKU ด้วย SKU Code และชื่อสินค้า
- รองรับ Search Result, Empty Result, Error และ Retry
- พัฒนาหน้า Item Detail
- แสดง Item ID, SKU, Product Name และ Unit
- เชื่อมผลการเลือกสินค้าเข้าสู่ Weighing Flow
- เตรียม Cache Model สำหรับข้อมูลสินค้าและ Local Record ที่จำเป็น

### Developer B

- พัฒนา SUNFORD App Endpoint สำหรับ Search SKU
- พัฒนา SUNFORD App Endpoint สำหรับ Item Detail ด้วย `item_id`
- เชื่อม TRCloud Search และ Item API ตาม Contract v1
- แปลงข้อมูล TRCloud เป็น Response Model กลางของแอป
- จัดการ Timeout, Not Found, Invalid Data และ TRCloud Unavailable
- เพิ่ม Permission และ Branch Validation ในคำขอค้นหา

### งานร่วมและการตรวจรับประจำวัน

- ทดสอบค้นหาด้วย SKU Code และชื่อสินค้า
- ทดสอบกรณีไม่พบสินค้าและข้อมูลสินค้าไม่ครบ
- ทดสอบการเปิด Item Detail จากผลค้นหา
- ตรวจว่า Error Message ฝั่ง Android สอดคล้องกับ Error Code จาก API
- Review Milestone 1: App/API Foundation, Login/Branch, Search SKU และ Item Detail

### ผลลัพธ์สิ้นวัน

- ผู้ใช้ Login, เลือกสาขา, ค้นหา SKU และดู Item Detail ได้
- Milestone 1 ผ่านการทดสอบร่วม

## วันที่ 4 - เสาร์ที่ 12 กันยายน 2026

### เป้าหมาย

สร้างหน้า Weighing/Inbound และ Contract สำหรับ Create Weighing Record

### Developer A

- พัฒนาหน้า Create Weighing Record
- แสดงสินค้าที่เลือก, SKU, Weight, Unit และ Remark
- สร้าง Validation สำหรับข้อมูลบังคับและน้ำหนักมากกว่า 0
- สร้าง Interface กลางสำหรับรับน้ำหนักจากเครื่องชั่ง
- ทำ Mock Scale Input เพื่อให้พัฒนาต่อได้ก่อนต่ออุปกรณ์จริง
- แสดงสถานะความนิ่งของน้ำหนักและสถานะการเชื่อมต่ออุปกรณ์
- สร้าง Local Database Entity และ Generator สำหรับ Client Record ID, Record ID และ SN

### Developer B

- กำหนด Request/Response ของ Create Weighing Record
- ตรวจและรับ Client Record ID/Idempotency Key ที่ Android App สร้าง
- ออกแบบ Transaction Status: PENDING, SENDING, SUCCESS, RETRYING, FAILED และ CONFLICT
- พัฒนา SUNFORD App Endpoint รับรายการ Weighing จาก Android
- ตรวจ User, Company, Source Branch, Item, Unit และ Weight
- เตรียม Adapter สำหรับส่ง Create Weighing Record ไป TRCloud ตาม Contract v1

### งานร่วมและการตรวจรับประจำวัน

- ทดสอบ Validation ของ Item, Branch, Weight และ Unit
- ทดสอบสร้าง Client Record ID ไม่ซ้ำ
- ตรวจ Field Mapping จากหน้าจอถึง Request ของ TRCloud
- ตรวจว่า Submit ซ้ำด้วย Idempotency Key เดิมไม่สร้างคำขอใหม่

### ผลลัพธ์สิ้นวัน

- Weighing Form พร้อม Validation
- Create Weighing API Contract และ Transaction Model

## วันที่ 5 - จันทร์ที่ 14 กันยายน 2026

### เป้าหมาย

เชื่อมเครื่องชั่งจริงและทำ Create Weighing Record ให้ส่งถึง TRCloud ได้

### Developer A

- เชื่อมต่อเครื่องชั่งตามรุ่นและ Protocol ที่ SUNFORD เลือก
- อ่านค่าน้ำหนัก, หน่วย และสถานะความนิ่ง
- จัดการ Disconnect, Invalid Data, Timeout และ Reconnect
- ป้องกันการบันทึกขณะน้ำหนักไม่พร้อมตามกฎที่ยืนยัน
- แสดงค่าน้ำหนักแบบ Real-time โดยไม่ทำให้ UI ค้าง
- รองรับการกรอกน้ำหนักด้วยตนเองเฉพาะเมื่อ Business Rule อนุญาต
- เมื่อค่าน้ำหนักพร้อม ให้แอปสร้าง Record ID/SN, สร้าง QR Code จากค่า SN, บันทึกสถานะรายการภายในเครื่อง และส่งข้อมูลผ่าน Integration API

### Developer B

- เชื่อม Create Weighing Record กับ TRCloud Test Environment
- ส่ง Client Record ID, Record ID, SN, Item, Weight, Unit และ Date-Time ตาม Mapping โดยให้ระบบอ้างอิง Company/Source Branch จาก Session และระบุผู้สร้างจาก Access Token
- ส่ง Record ID และ SN ที่แอปสร้างไปยัง TRCloud และรับผลยืนยันการบันทึก
- ตรวจว่า TRCloud เก็บค่า Record ID/SN ตาม Request โดยไม่สร้างใหม่หรือเปลี่ยนค่า
- ตรวจว่า TRCloud บันทึก SN พร้อมน้ำหนักสุทธิและรวมยอด Stock ของสาขาต้นทางตามน้ำหนัก
- บันทึก Request/Response Status โดยไม่เก็บข้อมูลอ่อนไหว
- จัดการ Error Code และ Timeout จาก TRCloud
- เพิ่ม Audit Log สำหรับการสร้างรายการ

### งานร่วมและการตรวจรับประจำวัน

- ทดสอบน้ำหนักปกติ, ศูนย์, ติดลบ, ไม่เสถียร และหน่วยไม่ตรง
- ทดสอบ Create Weighing Record สำเร็จและไม่สำเร็จ
- ตรวจรายการบน TRCloud เทียบกับข้อมูลที่แอปส่ง
- ตรวจว่า Record ID/SN ที่แอปสร้างถูกผูกกับ Client Record ID และข้อมูล Local ที่ถูกต้อง

### ผลลัพธ์สิ้นวัน

- รับน้ำหนักจากเครื่องชั่งจริงได้
- Create Weighing Record ถึง TRCloud ได้บนชุดทดสอบ
- รายงานผลทดสอบเครื่องชั่งและ Field Mapping

## วันที่ 6 - อังคารที่ 15 กันยายน 2026

### เป้าหมาย

ทำ Weighing Result, การสร้าง Record ID/SN และ QR Code จาก SN ในแอป รวมถึงประวัติรายการรับเข้าให้ครบ

### Developer A

- พัฒนาหน้า Weighing Result
- แสดง Record ID, SN, QR Code, SKU, Weight, Unit, Branch และ Status
- สร้างภาพ QR Code โดย Encode ค่า SN แบบ Plain Text เท่านั้น
- เพิ่ม Copy/Share เฉพาะข้อมูลที่อนุญาต
- พัฒนารายการ Weighing History ขั้นพื้นฐาน
- รองรับเปิดรายละเอียดจากรายการย้อนหลัง

### Developer B

- ตรวจค่าที่แอปสร้างก่อนส่ง และทำให้ TRCloud รับค่าเดิมโดยไม่สร้างรหัสใหม่
- ตรวจความไม่ซ้ำใน Local Database และความสัมพันธ์กับ Source Record
- พัฒนา Weighing History จาก Local Database และเปิด Weighing Record Detail จากรายการที่บันทึกไว้
- บันทึก Print Status และ Transaction Reference ที่จำเป็น
- เพิ่มการตรวจ Duplicate และ Conflict
- สรุป Error Mapping ของ Weighing Flow

### งานร่วมและการตรวจรับประจำวัน

- ทดสอบสร้างรายการหลายครั้งด้วย SKU/Weight เดียวกัน
- ตรวจ Record ID/SN ว่าไม่ซ้ำตามกฎที่ยืนยัน และตรวจว่า QR Code อ่านกลับมาเป็น SN ค่าเดิม
- ทดสอบเปิดรายละเอียดจาก History
- Review Milestone 2: Search, Item Detail, Scale และ Weighing/Inbound

### ผลลัพธ์สิ้นวัน

- Flow รับเข้าครบตั้งแต่เลือกสินค้าถึงแสดง Record ID/SN และ QR Code
- Milestone 2 ผ่านการทดสอบร่วม

## วันที่ 7 - พุธที่ 16 กันยายน 2026

### เป้าหมาย

ทำ Label Preview, Print, Reprint และ QR Code Scan

### Developer A

- พัฒนาหน้า Label Preview
- จัด Label Template ขนาด `6 × 4 cm` ให้แสดงเฉพาะชื่อสินค้า, วันที่–เวลาบันทึก, QR Code และ Barcode
- แสดงวันที่–เวลาบันทึกเป็น `dd/MM/yyyy HH:mm:ss` ตามเขตเวลา `Asia/Bangkok`
- สร้าง QR Code จาก SN แบบ Plain Text และสร้าง Barcode แบบ Code 128 จาก SN ค่าเดียวกัน
- เชื่อมต่อเครื่องพิมพ์ฉลากตามรุ่นและ Protocol ที่ SUNFORD เลือก
- พัฒนา Print, Reprint, Printing, Success และ Print Failed State
- รองรับ Preview, Print และ Reprint จากรายการชั่งเข้าที่บันทึกแล้ว
- พัฒนาการสแกน QR Code ด้วยกล้อง Android และอ่านค่า SN จาก QR Code
- รองรับการกรอก SN ด้วยตนเองในกรณีกล้องสแกนไม่ได้

### Developer B

- สร้าง Label Payload ภายใน SUNFORD Integration API โดยไม่เพิ่ม TRCloud Endpoint
- ตรวจสอบข้อมูลก่อนอนุญาตให้พิมพ์
- บันทึก Print/Reprint Audit Log พร้อม User, Device และ Date-Time
- กำหนดสิทธิ์ Reprint ตาม Permission
- เตรียม Receive API ด้วย SN ที่อ่านจาก QR Code และสาขาปลายทางตาม Contract
- จัดการรูปแบบรหัสไม่ถูกต้องและรายการไม่พบ

### งานร่วมและการตรวจรับประจำวัน

- เทียบฉลากจริงกับแบบที่ยืนยัน
- ทดสอบ Print, Reprint, เครื่องพิมพ์ไม่พร้อม และกระดาษ/การเชื่อมต่อผิดพลาด
- ตรวจว่าฉลากไม่มี SKU, Weight, Branch, Record ID หรือข้อมูลอื่นนอกเหนือจาก 4 รายการที่กำหนด
- สแกน QR Code จากฉลากที่พิมพ์จริงกลับเข้าสู่แอป และตรวจ Barcode ด้วยเครื่องอ่านที่ SUNFORD จัดเตรียม
- ตรวจ Audit Log ของการพิมพ์และพิมพ์ซ้ำ

### ผลลัพธ์สิ้นวัน

- Preview และพิมพ์ฉลากจริงได้
- สแกน QR Code จากฉลากที่พิมพ์และอ่านค่า SN ได้ตรงกับข้อมูลต้นทาง

## วันที่ 8 - พฤหัสบดีที่ 17 กันยายน 2026

### เป้าหมาย

ทำ Scan Receive, โอน Stock เข้าสาขาที่สแกน และหน้า Create Waste Weighing Record

### Developer A

- พัฒนาหน้า Scan QR Code/Receive by SN
- พัฒนาหน้า Weighing Record Detail
- แสดง SKU, Inbound Weight, Unit, Source Branch, Receiving Branch, User และเวลารับจาก Server
- พัฒนาหน้า Create Waste Weighing Record
- รับ Waste Weight จากเครื่องชั่งหรือวิธีที่ SUNFORD กำหนด
- ตรวจ Waste Weight เป็นค่าบวกและไม่เกิน Inbound Weight

### Developer B

- เชื่อม Receive Endpoint กับ TRCloud ตาม Contract v1
- ตรวจ Permission และสาขาปลายทางก่อนรับสินค้าและย้าย Stock
- บังคับให้ Receive และ Stock Transfer สำเร็จก่อนเปิดหน้า Waste/Yield
- พัฒนา Contract สำหรับ Create Waste Weighing Record
- ให้แอปสร้าง Client Waste Record ID, Transaction ID และ Idempotency Key ก่อนส่งคำขอ
- ตรวจ Source Record, Unit, Inbound Weight และ Waste Weight
- เตรียม Adapter สำหรับส่ง Waste Record ไป TRCloud

### งานร่วมและการตรวจรับประจำวัน

- ทดสอบ Receive ด้วย SN ที่ได้จากการสแกน QR Code และจากการกรอกด้วยตนเอง
- ตรวจว่า Stock ตามน้ำหนักของ SN ถูกย้ายมายังสาขาที่สแกนและไม่สามารถย้ายกลับสาขาต้นทาง
- ทดสอบกรณีอินเทอร์เน็ตหรือ TRCloud ไม่พร้อมใช้งานและการแสดงข้อความให้ผู้ใช้ทราบ
- ทดสอบ Not Found, Invalid Code, Wrong Branch และ Source Record ใช้งานต่อไม่ได้
- ทดสอบ Waste Weight เท่ากับ 0, ติดลบ, มากกว่า Inbound และหน่วยไม่ตรง
- ตรวจ Field Mapping ของ Waste Record

### ผลลัพธ์สิ้นวัน

- รับสินค้าเข้าและย้าย Stock มายังสาขาที่สแกนได้
- Waste Weighing Form พร้อม Validation และ API Contract

## วันที่ 9 - ศุกร์ที่ 18 กันยายน 2026

### เป้าหมาย

ทำ Waste/Yield Flow และเชื่อม TRCloud ให้ครบ

### Developer A

- พัฒนาหน้า Yield Result และ Transaction Detail
- แสดง Inbound Weight, Waste Weight, Net Yield Weight และ Yield Percentage
- แสดง Transaction ID, Request Status และ Error Message
- เพิ่มรายการ Waste/Yield History
- รองรับเปิดรายละเอียดรายการย้อนหลัง
- จัดรูปแบบทศนิยมและหน่วยตามกฎที่ยืนยัน

### Developer B

- พัฒนา Create Waste Weighing Record ถึง TRCloud
- คำนวณ `Net Yield Weight = Inbound Weight - Waste Weight`
- คำนวณ `Yield (%) = (Net Yield Weight / Inbound Weight) x 100`
- ใช้หน่วย, จำนวนทศนิยม และหลักการปัดเศษตาม Business Rule ที่ยืนยัน
- ส่ง Transaction ID ที่แอปสร้าง และรับ TRCloud Reference ID/ผลลัพธ์การบันทึกโดยไม่เปลี่ยน Transaction ID
- เพิ่ม Waste/Yield History, Detail และ Audit Log

### งานร่วมและการตรวจรับประจำวัน

- ทดสอบสูตรด้วยค่าปกติ, ศูนย์, ขอบเขตสูงสุด และค่าทศนิยม
- ตรวจผลคำนวณฝั่ง Android, Integration API และ TRCloud ให้ตรงกัน
- ทดสอบสร้าง Waste Record สำเร็จและไม่สำเร็จ
- Review Milestone 3: Label, Scan Receive, Stock Transfer, Waste และ Yield

### ผลลัพธ์สิ้นวัน

- Flow ตั้งแต่สแกนรายการต้นทางถึง Waste/Yield Result ทำงานได้
- Milestone 3 ผ่านการทดสอบร่วม

## วันที่ 10 - เสาร์ที่ 19 กันยายน 2026

### เป้าหมาย

สร้าง Local Database, Transaction State และกลไกป้องกันข้อมูลสูญหายเมื่อการเชื่อมต่อขัดข้อง

### Developer A

- สร้าง Local Database สำหรับข้อมูลที่จำเป็น
- จัดเก็บ Draft, Pending Transaction และ Request Status
- สร้าง Transaction Buffer สำหรับ Weighing และ Waste/Yield
- พัฒนาหน้า Transaction Status
- แสดง Pending, Sending, Success, Retrying, Failed และ Conflict
- เพิ่มคำสั่ง Retry ตามสิทธิ์

### Developer B

- ออกแบบ Request Processor ฝั่ง Integration API ตามความจำเป็น
- กำหนด Timeout, Retry Count และ Exponential Backoff
- รองรับ Idempotency Key ในทุกคำขอสร้างข้อมูล
- ป้องกันรายการซ้ำจากการส่งซ้ำหรือ Network Timeout
- พัฒนาสถานะ Transaction ภายใน Local Database โดยไม่เพิ่ม TRCloud Endpoint
- กำหนดพฤติกรรมเมื่อ Session หมดอายุระหว่างส่งข้อมูล

### งานร่วมและการตรวจรับประจำวัน

- ทดสอบกรณีเครือข่ายขัดข้องระหว่างส่งรายการ
- ทดสอบปิดและเปิดแอปใหม่แล้วสถานะรายการไม่สูญหาย
- ทดสอบเชื่อมต่อกลับมาและ Retry สำเร็จ
- ตรวจว่า Retry ไม่สร้าง Weighing หรือ Waste Record ซ้ำ

### ผลลัพธ์สิ้นวัน

- Local Database, Transaction State และ Retry พื้นฐาน
- หลักฐานทดสอบการขัดข้องและกลับมาเชื่อมต่อใหม่ชุดแรก

## วันที่ 11 - จันทร์ที่ 21 กันยายน 2026

### เป้าหมาย

ทำ Retry, Conflict, Idempotency, Audit Log และ Error Mapping ให้พร้อมใช้งานจริง

### Developer A

- พัฒนาหน้า Error Detail และ Retry Detail
- แสดง Error ที่ผู้ใช้เข้าใจได้โดยไม่เปิดเผยข้อมูลอ่อนไหว
- เพิ่ม Filter ตาม Transaction Status ใน History
- จัดการ Session Expired ระหว่างมีรายการค้าง
- แสดง Conflict และแนวทางให้ผู้ดูแลดำเนินการ
- ป้องกันการกด Submit หรือ Retry ซ้ำระหว่างคำขอกำลังทำงาน

### Developer B

- ทำ Idempotency Store และ Duplicate Detection ให้ครบ
- ทำ Error Mapping ระหว่าง TRCloud, Integration API และ Android
- เพิ่ม Audit Log สำหรับ Create, Retry, Print, Reprint และ Conflict
- เพิ่ม Correlation ID เพื่อค้นหาเหตุการณ์ข้ามระบบ
- กำหนดการเก็บ Log โดยซ่อน Credential และข้อมูลอ่อนไหว
- ทดสอบ Timeout ก่อนและหลัง TRCloud บันทึกข้อมูล

### งานร่วมและการตรวจรับประจำวัน

- ทดสอบกด Submit ซ้ำ, Retry ซ้ำ และส่ง Idempotency Key เดิม
- ทดสอบ Timeout ที่ไม่ทราบผลลัพธ์และการตรวจสอบสถานะย้อนหลัง
- ทดสอบ Conflict, Failed และ Recovery Flow
- ตรวจสอบ Audit Log สามารถตามเหตุการณ์จาก Android ถึง TRCloud ได้

### ผลลัพธ์สิ้นวัน

- Retry และ Duplicate Protection ทำงานตามกฎ
- Error/Audit Trace พร้อมใช้ในการทดสอบและแก้ปัญหา

## วันที่ 12 - อังคารที่ 22 กันยายน 2026

### เป้าหมาย

ปิดงาน Permission, Security, Error State และเตรียม Release Candidate สำหรับ Integration Test

### Developer A

- ตรวจ Permission ของทุกหน้าจอและทุก Action
- ตรวจ Secure Storage, Logout และ Session Cleanup
- ปิด Screen Capture หรือข้อมูลอ่อนไหวตามนโยบายที่ยืนยัน
- ตรวจ Loading, Empty, Success, Error และ Retry ของทุก Flow
- ตรวจ Accessibility พื้นฐานและการแสดงผลบนขนาดหน้าจอที่กำหนด
- แก้ Defect จากการรวมระบบรอบแรก

### Developer B

- ตรวจ Authentication และ Authorization ของทุก Endpoint
- ตรวจ Branch Isolation และป้องกันการเข้าถึงข้อมูลข้ามสาขา
- ตรวจ Input Validation, Rate/Request Control และ HTTPS Configuration
- ตรวจ Secret Management และ Log Redaction
- ตรวจ Database Constraint, Transaction และ Idempotency
- สรุป OpenAPI/API Collection และ Error Code สำหรับชุด UAT

### งานร่วมและการตรวจรับประจำวัน

- ทดสอบ End-to-End ตั้งแต่ Login ถึง Yield Result อย่างน้อย 1 รอบ
- ทดสอบผู้ใช้ถูกสิทธิ์, ผิดสาขา, Session หมดอายุ และ TRCloud ไม่พร้อมใช้งาน
- ทำ Regression Test ของ Login, Search, Weighing, Label, Scan Receive, Stock Transfer, Waste/Yield และ Retry
- Review Milestone 4: Data Protection, Retry, Security, Permission, Audit และ Error Handling

### ผลลัพธ์สิ้นวัน

- Release Candidate 1 สำหรับทดสอบระบบรวม
- API Documentation และ Test Checklist พร้อมใช้
- Milestone 4 ผ่านการทดสอบร่วม

## วันที่ 13 - พุธที่ 23 กันยายน 2026

### เป้าหมาย

ทดสอบระบบรวม, ดำเนินการ UAT, ปิด Defect สำคัญ และส่งมอบเวอร์ชัน UAT

### Developer A

- ติดตั้ง Release Candidate บนอุปกรณ์ Android จริง
- ทดสอบการเชื่อมต่อเครื่องชั่งต่อเนื่องและการ Reconnect
- ทดสอบ Label Preview, Print, Reprint และ Scan ฉลากจริง
- ทดสอบการเชื่อมต่อปกติ, การเชื่อมต่อขัดข้อง, ปิดแอป, เปิดใหม่ และ Retry
- เก็บ Screenshot, Log Reference และผลทดสอบที่จำเป็น
- แก้ไข Defect ฝั่ง Android ที่เป็น Blocker/Critical
- สนับสนุน UAT และบันทึกผล Pass/Fail ของ Android, เครื่องชั่ง, เครื่องพิมพ์ และ User Flow
- ทำ Final Regression และสร้าง APK/AAB เวอร์ชัน UAT
- ตรวจ Version, Environment, Signing Configuration และจัดทำ Release Note/คู่มือผู้ใช้

### Developer B

- เฝ้าตรวจ API Transaction และ TRCloud Response ระหว่างทดสอบ
- เทียบข้อมูล Android, Integration Database และ TRCloud
- ทดสอบ Duplicate, Timeout, Retry, Permission และ Branch Isolation
- ตรวจ Audit Log, Correlation ID และ Error Mapping
- ตรวจ Deployment Configuration ของ UAT
- แก้ไข Defect ฝั่ง API/Integration ที่เป็น Blocker/Critical
- สนับสนุน UAT และตรวจ Transaction จริงใน TRCloud
- ปิด Defect ฝั่ง API/Integration ที่เป็น Blocker/Critical ภายในขอบเขต
- ส่ง OpenAPI/API Collection, Field Mapping, Error Code, Configuration Template และ Runbook

### งานร่วมและการตรวจรับประจำวัน

- รัน Flow จริง: Login -> Branch -> Search SKU -> Item Detail -> Weighing -> SN/QR Code -> Print -> Scan QR -> Receive/Transfer Stock -> Waste -> Yield Result
- รัน Negative Test และ Recovery Test ตาม Checklist
- จัดทำ Defect List พร้อม Severity, Owner และสถานะ
- ให้ผู้รับผิดชอบลูกค้าทดสอบ Acceptance Flow หลักและบันทึกผลพร้อมหลักฐาน
- Retest รายการที่แก้ไขและทำ Final Smoke Test หลัง Build/Deployment
- ยืนยันว่าไม่มี Blocker หรือ Critical Defect ก่อนส่งมอบเวอร์ชัน UAT
- ตรวจ APK/AAB ติดตั้งหรือ Build ได้จาก Source ที่ส่งมอบ

### ผลลัพธ์สิ้นวัน

- APK/AAB เวอร์ชัน UAT และ Source Code
- UAT Integration API และ Configuration Template
- Integration Test Report, UAT Result และ Defect Summary
- หลักฐานทดสอบกับอุปกรณ์จริง
- API Document, Field Mapping, Release Note, คู่มือ และ Runbook
- สรุปสถานะพร้อมเข้าสู่ขั้นตอน Production หลังได้รับอนุมัติ UAT

## 8. Milestone และจุดตรวจรับ

| Milestone | วันที่ตรวจ | ขอบเขตที่ต้องทำงานได้ |
|---|---|---|
| M1 - Foundation | ศุกร์ 11 กันยายน 2026 | App/API Foundation, Login, Company/Branch, Search SKU และ Item Detail |
| M2 - Weighing/Inbound | อังคาร 15 กันยายน 2026 | เครื่องชั่ง, Create Weighing Record, Record ID, SN, QR Code และ History |
| M3 - Receive/Waste/Yield | ศุกร์ 18 กันยายน 2026 | Label Print, Scan Receive, Stock Transfer, Waste Weighing และ Yield Result |
| M4 - Data Protection/Security | อังคาร 22 กันยายน 2026 | Local Database, Transaction State, Retry, Idempotency, Permission, Audit และ Error Mapping |
| M5 - Internal QA/UAT | พุธ 23 กันยายน 2026 | End-to-End Test และ UAT ผ่านกับ Android, TRCloud, เครื่องชั่ง และเครื่องพิมพ์จริง |
| M6 - UAT Delivery | พุธ 23 กันยายน 2026 | Final Regression, APK/AAB, API และเอกสารส่งมอบ |

## 9. Definition of Done

ฟังก์ชันหรือ Milestone จะถือว่าเสร็จเมื่อผ่านเงื่อนไขต่อไปนี้:

- ทำงานตาม Acceptance Criteria ที่ยืนยัน
- Code Review ผ่านและรวมเข้าชุดทดสอบแล้ว
- Build และ Automated Check ที่เกี่ยวข้องผ่าน
- ทดสอบ Happy Path, Validation, Error และ Retry ที่เกี่ยวข้องแล้ว
- ไม่มี Credential, Token หรือข้อมูลอ่อนไหวอยู่ใน Source Code หรือ Log
- มี Permission และ Branch Validation ตามขอบเขต
- Transaction ที่สร้างข้อมูลรองรับ Idempotency และไม่เกิดรายการซ้ำจาก Retry
- มีหลักฐานทดสอบและสามารถอ้างอิง Log ด้วย Correlation ID ได้
- เอกสาร API, Field Mapping หรือคู่มือได้รับการอัปเดตตามงานที่เปลี่ยน
- ไม่มี Blocker หรือ Critical Defect ที่ยังเปิดอยู่สำหรับ Milestone นั้น

## 10. เกณฑ์จัดลำดับ Defect ในช่วง UAT

| ระดับ | ความหมาย | แนวทางภายในแผน 15 วัน |
|---|---|---|
| Blocker | ไม่สามารถทดสอบ Flow หลักต่อได้ หรือข้อมูลเสียหาย | หยุดงานส่วนอื่นเพื่อแก้และ Retest ทันที |
| Critical | ฟังก์ชันหลักผิด, เกิดข้อมูลซ้ำ, Permission ผิด หรือคำนวณผิด | ต้องปิดก่อนส่งมอบเวอร์ชัน UAT |
| Major | ฟังก์ชันใช้งานได้บางส่วนและมีทางเลี่ยง | แก้ตามเวลาที่เหลือและผลกระทบต่อ UAT |
| Minor | ข้อความ, รูปแบบ หรือปัญหาที่ไม่กระทบ Flow หลัก | บันทึกใน Backlog และกำหนดรอบแก้ร่วมกัน |

Change Request, Business Rule ใหม่, อุปกรณ์รุ่นเพิ่ม หรือ Flow ที่ไม่ได้อยู่ใน Scope ที่ล็อกไว้ ไม่ถือเป็น Defect และต้องประเมินผลกระทบต่อแผนแยกต่างหาก

## 11. รายการส่งมอบวันที่ 23 กันยายน 2026

- Android APK เวอร์ชัน UAT
- Android App Bundle เมื่อ Signing Information พร้อม
- Source Code ของ Native Android Application
- Source Code ของ SUNFORD Integration API
- Configuration Template โดยไม่มี Secret จริง
- Database Schema และ Migration ที่เกี่ยวข้อง
- OpenAPI Specification หรือ API Collection
- Field Mapping ระหว่าง Android, Integration API และ TRCloud
- Error Code และ Error Mapping
- Integration Test Report
- UAT Result และ Defect Summary
- Release Note
- คู่มือผู้ใช้แบบย่อ
- Deployment และ Support Runbook

## 12. เงื่อนไขที่ทำให้กำหนดการเปลี่ยน

กำหนดส่งวันพุธที่ 23 กันยายน 2026 ตั้งอยู่บนเงื่อนไขว่าข้อมูล ระบบ และผู้เกี่ยวข้องพร้อมตามแผน หากเกิดเหตุการณ์ต่อไปนี้ ให้บันทึกเป็น Blocker และเลื่อนวันส่งมอบตามผลกระทบจริง:

- TRCloud API หรือ Test Environment ใช้งานไม่ได้
- TRCloud ไม่ยืนยัน Contract หรือส่ง Endpoint/Sandbox ช้ากว่ากำหนดในหัวข้อ 4.3
- สูตร Yield, หน่วย, ทศนิยม หรือหลักการปัดเศษเปลี่ยนระหว่างพัฒนา
- กฎ Record ID/SN หรือรูปแบบข้อมูลใน QR Code เปลี่ยนระหว่างพัฒนา
- เครื่องชั่งหรือเครื่องพิมพ์ที่ SUNFORD รับผิดชอบไม่พร้อม, Test Data ไม่พร้อม หรืออุปกรณ์ Android/กล้อง/เครือข่าย ณ จุด UAT ไม่พร้อม
- ผู้รับผิดชอบ UAT ไม่สามารถทดสอบตามวันที่กำหนด
- มีการเพิ่ม Scope, อุปกรณ์, Protocol, Report หรือ Flow ใหม่
- ระบบภายนอกเปลี่ยน API หรือพฤติกรรมที่กระทบงานที่ทำแล้ว

ทุก Blocker ต้องมีวันที่เริ่ม, Owner, ผลกระทบ, ทางเลือกชั่วคราว และวันที่ปลด Blocker โดยไม่ใช้วันรอเป็นวันพัฒนาที่เสร็จสมบูรณ์

## 13. ขั้นตอนหลังสิ้นสุดแผน 15 วัน

วันที่ 23 กันยายน 2026 เป็นการส่งมอบ **เวอร์ชัน UAT** ไม่ใช่การรับรองว่า Production เปิดใช้งานแล้ว ขั้นตอนถัดไปมีดังนี้:

1. ลูกค้ายืนยันผล UAT และรายการ Defect ที่อยู่ในขอบเขต
2. ทีมแก้ไขรายการหลัง UAT ตามผลทดสอบจริง หากยังมีรายการคงเหลือ
3. ทำ Production Configuration และ Production Smoke Test
4. สร้าง Production APK/AAB ด้วย Signing ที่ยืนยัน
5. ส่ง Google Play Review หรือกระจายแอปตามช่องทางที่ตกลง
6. เปิดใช้งานจริงและติดตามผลช่วงเริ่มต้น

ระยะเวลารออนุมัติ UAT, ระยะเวลาตรวจสอบของ Google และการแก้ไขจาก Scope เพิ่มเติมไม่นับรวมอยู่ในระยะเวลาโครงการ 15 วันนี้

## 14. TRCloud API Contract v1 - 6 Endpoints ตาม Flow ที่ยืนยัน

### 14.1 ขอบเขตและผู้รับผิดชอบ

- **ผู้กำหนด API Contract:** SUNFORD
- **ผู้พัฒนา API:** TRCloud
- **ผู้เรียกใช้ API:** SUNFORD Integration API
- **จำนวน API:** 6 Endpoints เท่านั้น
- **สถานะ:** ใช้เป็นข้อกำหนดสำหรับ Development, Integration Test และ UAT

Android Application ติดต่อ SUNFORD Integration API และไม่เรียก TRCloud โดยตรง ส่วน TRCloud ต้องพัฒนา 6 Endpoints ตามชื่อ Field, Request, Response และ Validation ในหัวข้อนี้

ฟังก์ชันภายใน Android เช่น Local Database, Transaction State, History, Label Preview, Print, Retry UI และ Audit Log ของ SUNFORD ไม่ใช่เหตุผลให้เพิ่ม TRCloud Endpoint นอกเหนือจาก 6 เส้นนี้

Source of Truth สำหรับรายการที่สร้างในแอป:

- Android App สร้าง Client Record ID, Record ID, SN และ Transaction ID ก่อนเรียก API
- แอปต้องเชื่อมต่ออินเทอร์เน็ตและส่งข้อมูลผ่าน SUNFORD Integration API ระหว่างการใช้งาน
- Android App เก็บสถานะรายการที่จำเป็นภายในเครื่องเพื่อป้องกันข้อมูลสูญหายหาก Request ขัดข้อง
- TRCloud ต้องรับและจัดเก็บค่าเดิม ห้ามสร้างใหม่, แทนที่ หรือแก้ไขรหัสที่แอปส่ง
- TRCloud สามารถสร้าง `trcloud_reference_id` เพิ่มเพื่อใช้อ้างอิงภายในได้ แต่ห้ามใช้แทนรหัสของแอป

### 14.2 สรุป API ทั้งหมด

| ลำดับ | Method | Endpoint | Request หลัก | Response หลัก |
|---:|---|---|---|---|
| 1 | POST | `/v1/login` | Username, Password | Access Token, User Profile, Permission |
| 2 | GET | `/v1/items` | SKU Code หรือชื่อสินค้า | SKU Search Results |
| 3 | GET | `/v1/items/{item_id}` | Item ID | Item Detail |
| 4 | POST | `/v1/weighing-records` | Record ID, SN, SKU และ Weight ที่แอปสร้าง | ผลยืนยันการบันทึกและ TRCloud Reference ID |
| 5 | POST | `/v1/weighing-records/receive` | SN; สาขารับอ้างอิงจากสาขาที่ Login | ผลรับสินค้าและ Stock Transfer ตามน้ำหนัก |
| 6 | POST | `/v1/waste-weighing-records` | Transaction ID, Source Record และ Waste Weight ที่แอปสร้าง | ผลยืนยันการบันทึก, TRCloud Reference ID และ Yield |

ห้ามเพิ่ม Endpoint สำหรับ Refresh Token, Logout, User Profile, Company, Branch, History, Transaction Recovery หรือ Health ใน Contract นี้ ข้อมูล User Profile และ Permission ต้องคืนมาพร้อม Login ส่วนการสแกน SN เพื่อรับสินค้าและย้าย Stock ให้ใช้ Receive Endpoint

### 14.3 Base URL และมาตรฐานร่วม

TRCloud ต้องแจ้ง Base URL แยกตาม Environment:

| Environment | Base URL |
|---|---|
| Sandbox/UAT | `{TRCLOUD_SANDBOX_BASE_URL}` |
| Production | `{TRCLOUD_PRODUCTION_BASE_URL}` |

ข้อกำหนดร่วม:

- ใช้ HTTPS และ TLS 1.2 หรือใหม่กว่า
- Request/Response ใช้ `application/json; charset=utf-8`
- ชื่อ Field ใช้ `snake_case`
- Timestamp ใช้ RFC 3339 เช่น `2026-08-31T12:30:00.999+07:00`
- Identifier, Code และค่าที่อาจมีเลขศูนย์นำหน้า เช่น `sku`, `sn`, `record_id`, `user_id` และ `transaction_id` ใช้ JSON `string`
- ค่าน้ำหนักและเปอร์เซ็นต์ เช่น `weight`, `waste_weight`, `net_yield_weight` และ `yield_percentage` ใช้ JSON `number` โดยห้ามใส่เครื่องหมายคำพูด
- จำนวนเต็ม เช่น `expires_in` ใช้ JSON `number` แบบ Integer
- ค่าจริง/เท็จ เช่น `success`, `active` และ `retryable` ใช้ JSON `boolean` คือ `true` หรือ `false` โดยไม่มีเครื่องหมายคำพูด
- รายการข้อมูลใช้ JSON `array` และข้อมูลหนึ่งชุดใช้ JSON `object`
- Field ที่ไม่มีค่าให้ใช้ `null` เฉพาะ Field ที่ Contract ระบุว่า Nullable ห้ามใช้ String ว่างแทน Number หรือ Boolean
- หน่วยน้ำหนักของ Contract นี้คือ `KG`
- น้ำหนักใช้ทศนิยมไม่เกิน 2 ตำแหน่งตามตัวอย่าง `34.56`
- Yield Percentage คำนวณและแสดงผล 2 ตำแหน่ง แต่ส่งใน JSON เป็น `number`
- ใช้การปัดเศษแบบ `ROUND_HALF_UP`
- TRCloud ต้องตอบ JSON ทุกกรณีและห้ามตอบ HTML Error Page

#### 14.3.1 ตารางประเภทข้อมูลมาตรฐาน

| Field หรือกลุ่มข้อมูล | JSON Type | ตัวอย่าง | กฎสำคัญ |
|---|---|---|---|
| `success`, `active`, `retryable` | `boolean` | `true` | ห้ามส่งเป็น `"true"` หรือ `1` |
| `expires_in` | `number` (integer) | `3600` | หน่วยเป็นวินาที |
| `weight` | `number` | `34.56` | หน่วย `KG`, ไม่เกิน 2 ตำแหน่ง |
| `inbound_weight`, `waste_weight`, `net_yield_weight` | `number` | `4.56` | หน่วย `KG`, ไม่เกิน 2 ตำแหน่ง |
| `transferred_weight`, `source_stock_weight_after`, `receiving_stock_weight_after`, `branch_stock_weight_after` | `number` | `84.56` | ยอด Stock รวมตามน้ำหนัก หน่วย `KG` |
| `yield_percentage` | `number` | `86.81` | ค่าเปอร์เซ็นต์หลังปัดเศษ 2 ตำแหน่ง |
| `receipt_created`, `yield_finalized` | `boolean` | `true` | ห้ามส่งเป็น String หรือ Number |
| `sku`, `sn` | `string` | `"00001"` | ต้องเก็บเลขศูนย์นำหน้า |
| Identifier ทุกชนิด | `string` | `"USR-1001"` | รวม UUID และ TRCloud Reference ID |
| Timestamp | `string` | `"2026-08-31T12:30:00.999+07:00"` | รวม `recorded_at`, `received_at`, `processed_at`; รูปแบบ RFC 3339 |
| `permissions`, `companies`, `branches` | `array` | `[]` | ต้องเป็น Array แม้ไม่มีรายการ |
| `data`, `error`, `user_profile` | `object` | `{}` | ยกเว้น `data` ของ Search SKU ซึ่งเป็น Array |

ค่าตัวเลขใน JSON อาจไม่คงเลขศูนย์ท้ายทศนิยมหลังผ่าน Serializer เช่น `30.00` อาจถูกส่งเป็น `30` ซึ่งยังเป็นค่า Number เดียวกัน ส่วนการแสดงผลบนหน้าจอให้แอป Format เป็น 2 ตำแหน่งตามกฎของระบบ

### 14.4 Header มาตรฐาน

| Header | บังคับ | ใช้กับ |
|---|---|---|
| `Content-Type: application/json` | ใช่ | POST ทุกเส้น |
| `Accept: application/json` | ใช่ | ทุกเส้น |
| `Authorization: Bearer {access_token}` | ใช่ | ทุกเส้นยกเว้น Login |
| `X-Request-ID: {uuid}` | ใช่ | ทุกเส้น |
| `Idempotency-Key: {uuid}` | ใช่ | Create Weighing, Receive Weighing และ Create Waste Weighing |

TRCloud ต้องส่ง `X-Request-ID` ค่าเดิมกลับมาใน Response เพื่อใช้ตรวจสอบ Log ร่วมกัน

### 14.5 รูปแบบ Response กลาง

| Field | JSON Type | บังคับ | รายละเอียด |
|---|---|---|---|
| `success` | `boolean` | ใช่ | `true` เมื่อสำเร็จ และ `false` เมื่อผิดพลาด |
| `data` | `object` หรือ `array` | เมื่อสำเร็จ | Type ต้องตรงกับ Response ของแต่ละ Endpoint |
| `error` | `object` | เมื่อผิดพลาด | ไม่ส่งพร้อม `data` |
| `error.code` | `string` | เมื่อผิดพลาด | Error Code ตามหัวข้อ 14.12 |
| `error.message` | `string` | เมื่อผิดพลาด | ข้อความที่ไม่เปิดเผยข้อมูลอ่อนไหว |
| `error.retryable` | `boolean` | เมื่อผิดพลาด | ระบุว่าสามารถ Retry คำขอเดิมได้หรือไม่ |
| `request_id` | `string` | ใช่ | UUID เดียวกับ `X-Request-ID` |

Response สำเร็จ:

```json
{
  "success": true,
  "data": {},
  "request_id": "8d0195f8-9457-4a89-8b13-933f94622dad"
}
```

Response ผิดพลาด:

```json
{
  "success": false,
  "error": {
    "code": "ITEM_NOT_FOUND",
    "message": "Item was not found",
    "retryable": false
  },
  "request_id": "8d0195f8-9457-4a89-8b13-933f94622dad"
}
```

### 14.6 API 1 - Login

#### 14.6.1 POST `/v1/login`

ใช้ Login และรับ User Profile/Permission ใน Response เดียว

Request Fields:

| Field | JSON Type | บังคับ |
|---|---|---|
| `username` | `string` | ใช่ |
| `password` | `string` | ใช่ |
| `device_id` | `string` | ใช่ |

Request:

```json
{
  "username": "user@example.com",
  "password": "********",
  "device_id": "ANDROID-DEVICE-001"
}
```

Response `200 OK`:

```json
{
  "success": true,
  "data": {
    "access_token": "{access_token}",
    "expires_in": 3600,
    "user_profile": {
      "user_id": "USR-1001",
      "username": "user@example.com",
      "display_name": "Example User"
    },
    "permissions": [
      "ITEM_READ",
      "WEIGHING_CREATE",
      "WEIGHING_READ",
      "STOCK_RECEIVE",
      "WASTE_CREATE",
      "YIELD_READ"
    ],
    "companies": [
      {
        "company_id": "COM-001",
        "company_name": "SUNFORD",
        "branches": [
          {
            "branch_id": "BR-001",
            "branch_name": "Bangkok Branch"
          },
          {
            "branch_id": "BR-002",
            "branch_name": "Destination Branch"
          }
        ]
      }
    ]
  },
  "request_id": "8d0195f8-9457-4a89-8b13-933f94622dad"
}
```

Response Data Types:

| Field | JSON Type |
|---|---|
| `access_token` | `string` |
| `expires_in` | `number` (integer) |
| `user_profile` | `object` |
| `user_profile.user_id` | `string` |
| `user_profile.username` | `string` |
| `user_profile.display_name` | `string` |
| `permissions` | `array<string>` |
| `companies` | `array<object>` |
| `companies[].company_id` | `string` |
| `companies[].company_name` | `string` |
| `companies[].branches` | `array<object>` |
| `companies[].branches[].branch_id` | `string` |
| `companies[].branches[].branch_name` | `string` |

กฎ:

- TRCloud ตรวจ Username/Password และ Permission
- Password ห้ามปรากฏใน Log
- Login ไม่สำเร็จตอบ `401 LOGIN_FAILED`
- เมื่อ Token หมดอายุ ผู้ใช้ Login ใหม่ผ่าน Endpoint เดิม
- Android ไม่จัดเก็บ TRCloud Credential หรือ TRCloud Token โดยตรง

### 14.7 API 2 - Search SKU

#### 14.7.1 GET `/v1/items`

Query Parameter:

| Parameter | Type | บังคับ | รายละเอียด |
|---|---|---|---|
| `query` | `string` | ใช่ | SKU Code หรือชื่อสินค้า |
| `company_id` | `string` | ใช่ | บริษัทที่เลือกจาก Login |
| `branch_id` | `string` | ใช่ | สาขาที่เลือกจาก Login |

ตัวอย่าง:

```text
GET /v1/items?query=00001&company_id=COM-001&branch_id=BR-001
```

Response `200 OK`:

```json
{
  "success": true,
  "data": [
    {
      "item_id": "ITM-00001",
      "sku": "00001",
      "name": "Example Product",
      "weight_unit": "KG"
    }
  ],
  "request_id": "8d0195f8-9457-4a89-8b13-933f94622dad"
}
```

`data` เป็น `array<object>` โดย Item แต่ละรายการมี Type ดังนี้:

| Field | JSON Type |
|---|---|
| `item_id` | `string` |
| `sku` | `string` |
| `name` | `string` |
| `weight_unit` | `string` |

กฎ:

- ค้นหาได้ด้วย SKU Code หรือชื่อสินค้า
- คืนเฉพาะสินค้าที่ User/Company/Branch มีสิทธิ์
- ไม่พบสินค้าให้คืน `data: []`
- API นี้ไม่สร้างหรือแก้ไขข้อมูล

### 14.8 API 3 - Get Item by Item ID

#### 14.8.1 GET `/v1/items/{item_id}`

Parameters:

| Parameter | ตำแหน่ง | Type | บังคับ |
|---|---|---|---|
| `item_id` | Path | `string` | ใช่ |
| `company_id` | Query | `string` | ใช่ |
| `branch_id` | Query | `string` | ใช่ |

Response `200 OK`:

```json
{
  "success": true,
  "data": {
    "item_id": "ITM-00001",
    "sku": "00001",
    "name": "Example Product",
    "weight_unit": "KG",
    "active": true
  },
  "request_id": "8d0195f8-9457-4a89-8b13-933f94622dad"
}
```

Response Data Types:

| Field | JSON Type |
|---|---|
| `item_id`, `sku`, `name`, `weight_unit` | `string` |
| `active` | `boolean` |

กฎ:

- ไม่พบ Item ตอบ `404 ITEM_NOT_FOUND`
- Item ไม่ Active ตอบข้อมูลได้ แต่ห้ามนำไปสร้าง Weighing Record
- `sku` สำหรับ Flow นี้ต้องเป็นตัวเลข 5 หลัก เช่น `00001`
- `weight_unit` ต้องเป็น `KG`

### 14.9 API 4 - Create Weighing Record

#### 14.9.1 POST `/v1/weighing-records`

Request Fields:

| Field | JSON Type | บังคับ |
|---|---|---|
| `client_record_id` | `string` (UUID) | ใช่ |
| `record_id` | `string` | ใช่ |
| `sn` | `string` | ใช่ |
| `item_id` | `string` | ใช่ |
| `sku` | `string` | ใช่ |
| `weight` | `number` | ใช่ |
| `weight_unit` | `string` | ใช่ |
| `recorded_at` | `string` (RFC 3339) | ใช่ |
| `device_id` | `string` | ใช่ |

Request:

```json
{
  "client_record_id": "94aa0437-b30d-41cf-a4f1-5af0e4ed4325",
  "record_id": "2026-08-31 12:30.999",
  "sn": "00001202608311230999",
  "item_id": "ITM-00001",
  "sku": "00001",
  "weight": 34.56,
  "weight_unit": "KG",
  "recorded_at": "2026-08-31T12:30:00.999+07:00",
  "device_id": "ANDROID-DEVICE-001"
}
```

Response `201 Created`:

```json
{
  "success": true,
  "data": {
    "client_record_id": "94aa0437-b30d-41cf-a4f1-5af0e4ed4325",
    "record_id": "2026-08-31 12:30.999",
    "trcloud_reference_id": "TRC-WR-000001",
    "sku": "00001",
    "sn": "00001202608311230999",
    "weight": 34.56,
    "weight_unit": "KG",
    "source_branch_id": "BR-001",
    "created_by_user_id": "USR-1001",
    "source_stock_weight_after": 134.56,
    "status": "SUCCESS"
  },
  "request_id": "8d0195f8-9457-4a89-8b13-933f94622dad"
}
```

Response Data Types:

| Field | JSON Type |
|---|---|
| `client_record_id`, `record_id`, `trcloud_reference_id` | `string` |
| `sku`, `sn`, `weight_unit`, `source_branch_id`, `created_by_user_id`, `status` | `string` |
| `weight`, `source_stock_weight_after` | `number` |

กฎการสร้างข้อมูลใน Android App ตามภาพที่ยืนยัน:

- `sku` เป็นตัวเลข 5 หลัก เช่น `00001`
- Company และ `source_branch_id` ต้องมาจาก Session ที่ Login ขณะสร้างรายการชั่งเข้า และห้ามรับค่าเหล่านี้จาก Request Body
- TRCloud ต้องตรวจ Permission `WEIGHING_CREATE` และกำหนด `created_by_user_id` จาก Access Token
- หนึ่ง SN แทนสินค้าหนึ่งรายการ โดย `weight` คือน้ำหนักสุทธิของสินค้ารายการนั้น
- ยอด Stock ของแต่ละสาขาคำนวณโดยรวมน้ำหนักสุทธิของทุก SN ในสาขา ไม่ได้นับเป็นจำนวนชิ้น
- `record_id` แสดงวันที่และเวลาระดับ Millisecond เช่น `2026-08-31 12:30.999`
- `sn` ประกอบด้วย SKU 5 หลัก + วันเวลา `yyyyMMddHHmmSSS`
- ตัวอย่าง SN: `00001` + `202608311230999` = `00001202608311230999`
- แอปต้องสร้าง QR Code โดย Encode ค่า SN เป็น Plain Text ตรงตัว เช่น `00001202608311230999`
- Payload ภายใน QR Code ต้องไม่มี Prefix, URL, JSON, ช่องว่าง หรืออักขระขึ้นบรรทัดใหม่
- แอปต้องสร้าง Barcode แบบ Code 128 โดย Encode ค่า SN Plain Text เดียวกับ QR Code
- QR Code และ Barcode เป็นรูปแทนค่า SN สำหรับการพิมพ์ ไม่ใช่ Identifier ใหม่ และ API ส่งเฉพาะ Field `sn` โดยไม่มี Field `barcode`
- แอปใช้ QR Code สำหรับ Scan Receive ส่วน Barcode บนฉลากไม่ได้เพิ่ม Flow ค้นหาหรือ Endpoint ใหม่
- ฉลากขนาด `6 × 4 cm` ต้องแสดงเฉพาะ: ชื่อสินค้า, วันที่–เวลาบันทึกรูปแบบ `dd/MM/yyyy HH:mm:ss` เขตเวลา `Asia/Bangkok`, QR Code และ Barcode
- แอปต้องสร้าง Client Record ID, Record ID และ SN แล้วเก็บสถานะรายการก่อนส่งคำขอ
- แอปต้องตรวจความไม่ซ้ำของ Record ID และ SN ใน Local Database ก่อนบันทึก
- น้ำหนักต้องมากกว่า 0 และไม่เกิน 999.99 KG
- แอปพิมพ์ฉลากได้หลัง TRCloud ตอบ `201 Created` และยืนยัน SN สำเร็จแล้วเท่านั้น
- TRCloud ต้องตรวจค่าและบันทึก Record ID/SN ตาม Request โดยห้ามสร้างหรือเปลี่ยนค่า
- เมื่อสร้างรายการสำเร็จ TRCloud ต้องเพิ่ม `weight` ของ SN เข้า Stock รวมตามน้ำหนักของ `source_branch_id` และคืน `source_stock_weight_after`
- ถ้า TRCloud พบ SN ซ้ำ ให้ตอบ `409 IDENTIFIER_CONFLICT` โดยไม่แก้ค่าใน Request
- เมื่อได้รับ `409 IDENTIFIER_CONFLICT` ก่อนพิมพ์ฉลาก แอปต้องสร้าง Record ID/SN ใหม่และส่งคำขอใหม่ด้วย Idempotency Key ใหม่
- ห้ามพิมพ์ QR Code ของ SN ที่ยังไม่ได้รับการยืนยันจาก TRCloud วิธีนี้ป้องกัน SN ซ้ำข้ามอุปกรณ์โดยไม่เปลี่ยนรูปแบบ SN ตามตัวอย่าง

กฎ Idempotency:

- `Idempotency-Key` ต้องตรงกับ `client_record_id`
- Key เดิมและ Request เดิมต้องคืน Record เดิม
- Key เดิมแต่ข้อมูลต่างกันตอบ `409 IDEMPOTENCY_CONFLICT`
- Retry ต้องส่ง Record ID และ SN ค่าเดิมจาก Local Database ทุกครั้ง
- TRCloud Response ต้อง Echo รหัสเดิมกลับมาเพื่อให้ SUNFORD ตรวจว่าไม่มีการเปลี่ยนค่า

### 14.10 API 5 - Scan Receive and Transfer Stock by SN

#### 14.10.1 POST `/v1/weighing-records/receive`

ใช้เมื่ออีกสาขาหนึ่งสแกน QR Code เพื่อรับสินค้า แอปอ่านค่า SN แล้วส่งคำขอผ่าน Session ที่ Login อยู่ สาขารับต้องอ้างอิงจากสาขาปัจจุบันของ Session เท่านั้น และต้องไม่ใช่สาขาต้นทางของ SN

Request Fields:

| Field | JSON Type | บังคับ | รายละเอียด |
|---|---|---|---|
| `client_receipt_id` | `string` (UUID) | ใช่ | สร้างโดยแอปและใช้เป็น Idempotency Key |
| `sn` | `string` | ใช่ | SN ที่อ่านจาก QR Code |
| `device_id` | `string` | ใช่ | อุปกรณ์ Android ที่ใช้สแกน |

Request:

```json
{
  "client_receipt_id": "6e5299dd-74de-4538-a585-118728346d34",
  "sn": "00001202608311230999",
  "device_id": "ANDROID-DEVICE-001"
}
```

Response `201 Created`:

```json
{
  "success": true,
  "data": {
    "client_receipt_id": "6e5299dd-74de-4538-a585-118728346d34",
    "trcloud_receipt_reference_id": "TRC-RCV-000001",
    "stock_movement_reference_id": "TRC-MOV-000001",
    "record_id": "2026-08-31 12:30.999",
    "item_id": "ITM-00001",
    "sku": "00001",
    "product_name": "Example Product",
    "sn": "00001202608311230999",
    "weight": 34.56,
    "weight_unit": "KG",
    "source_branch_id": "BR-001",
    "receiving_branch_id": "BR-002",
    "transferred_weight": 34.56,
    "source_stock_weight_after": 100.0,
    "receiving_stock_weight_after": 84.56,
    "receipt_created": true,
    "received_by_user_id": "USR-1001",
    "received_at": "2026-08-31T13:00:00.000+07:00",
    "status": "SUCCESS"
  },
  "request_id": "8d0195f8-9457-4a89-8b13-933f94622dad"
}
```

Response Data Types:

| Field | JSON Type |
|---|---|
| `client_receipt_id`, `trcloud_receipt_reference_id`, `stock_movement_reference_id`, `record_id` | `string` |
| `item_id`, `sku`, `product_name`, `sn`, `weight_unit` | `string` |
| `source_branch_id`, `receiving_branch_id`, `received_by_user_id`, `received_at`, `status` | `string` |
| `weight`, `transferred_weight`, `source_stock_weight_after`, `receiving_stock_weight_after` | `number` |
| `receipt_created` | `boolean` |

กฎการรับสินค้าและย้าย Stock:

- แอปต้องตรวจรูปแบบ SN ที่อ่านจาก QR Code ก่อนส่ง Request
- SUNFORD Integration API ต้องอ้างอิง Company และสาขาปัจจุบันจาก Session ที่ Login อยู่ ห้ามรับสาขารับจาก Request Body
- TRCloud ต้องค้นหารายการด้วย SN และต้องพบเพียง 1 รายการ
- TRCloud ต้องตรวจ Permission `STOCK_RECEIVE` และสิทธิ์ของสาขาปัจจุบันจาก Access Token/Session
- TRCloud ต้องกำหนด `received_by_user_id` จาก Access Token ห้ามเชื่อค่าผู้ใช้จาก Request
- `received_at` ต้องสร้างจากเวลาของ TRCloud เท่านั้น Request ห้ามส่งเวลารับจากอุปกรณ์
- `receiving_branch_id` ต้องเป็นสาขาปัจจุบันที่ Login อยู่และต้องไม่เท่ากับ `source_branch_id`
- หากสาขาปัจจุบันเท่ากับสาขาต้นทาง ให้ตอบ `409 SAME_BRANCH_TRANSFER_NOT_ALLOWED` และห้ามสร้าง Receipt หรือปรับ Stock
- TRCloud ต้องล็อก Stock ของ SN นี้ระหว่างประมวลผล เพื่อป้องกันสองสาขาสแกนรับพร้อมกัน
- TRCloud ต้องตรวจว่า Stock ของ SN ยังอยู่ที่ `source_branch_id` และยังไม่เคยมี Receipt
- TRCloud ต้องสร้าง Stock Movement ตาม `weight` ของ SN จาก `source_branch_id` ไป `receiving_branch_id` พร้อม `stock_movement_reference_id`
- TRCloud ต้องลดยอด Stock รวมตามน้ำหนักของสาขาต้นทางและเพิ่มยอด Stock รวมตามน้ำหนักของสาขาที่สแกนด้วยค่าเดียวกัน
- `transferred_weight` ต้องเท่ากับน้ำหนักสุทธิของ SN และต้องไม่เปลี่ยนระหว่างการย้ายสาขา
- การสร้าง Receipt, การย้ายสาขา และการปรับยอด Stock ตามน้ำหนักต้องสำเร็จใน Database Transaction เดียวกัน
- หากขั้นตอนใดไม่สำเร็จต้อง Rollback ทั้งหมด ห้ามเกิดสถานะรับสินค้าแล้วแต่ Stock ยังไม่ย้าย
- Response สำเร็จส่งได้หลัง Commit Transaction แล้วเท่านั้น
- แอปต้องตรวจ `success: true` และ `receiving_branch_id` ตรงกับสาขาที่ Login ก่อนอนุญาตให้ทำ Waste/Yield ต่อ
- `Idempotency-Key` ต้องตรงกับ `client_receipt_id`
- Key เดิมและ Request เดิมต้องคืนผล Receipt เดิมโดยไม่ย้าย Stock ซ้ำ
- Key เดิมแต่ข้อมูลต่างกันตอบ `409 IDEMPOTENCY_CONFLICT`
- หากมี Receipt อยู่ที่สาขาที่ Login และยังไม่มี Waste/Yield ให้คืน Receipt เดิมด้วย `receipt_created: false` โดยไม่ย้าย Stock ซ้ำ และอนุญาตให้ทำงานต่อ
- หากมี Receipt อยู่ที่สาขาอื่นให้ตอบ `409 RECEIPT_ALREADY_EXISTS`
- หาก SN มี Waste/Yield แล้วให้ตอบ `409 YIELD_ALREADY_FINALIZED` และห้ามเริ่มบันทึกซ้ำ
- หากยอดหรือเจ้าของ Stock ไม่ตรงกับ Source Record ให้ตอบ `409 STOCK_BALANCE_CONFLICT`
- QR Code ที่ว่าง อ่านไม่ได้ หรือไม่ได้บรรจุ SN รูปแบบที่กำหนดให้แอปแจ้งข้อผิดพลาดก่อนเรียก API

### 14.11 API 6 - Create Waste Weighing Record

#### 14.11.1 POST `/v1/waste-weighing-records`

Request Fields:

| Field | JSON Type | บังคับ |
|---|---|---|
| `client_waste_record_id` | `string` (UUID) | ใช่ |
| `transaction_id` | `string` (UUID) | ใช่ |
| `source_record_id`, `source_sn` | `string` | ใช่ |
| `waste_weight` | `number` | ใช่ |
| `weight_unit` | `string` | ใช่ |
| `recorded_at` | `string` (RFC 3339) | ใช่ |
| `device_id` | `string` | ใช่ |

Request:

```json
{
  "client_waste_record_id": "bb078e58-9ffc-44c5-a5e9-40472ce223d7",
  "transaction_id": "bb078e58-9ffc-44c5-a5e9-40472ce223d7",
  "source_record_id": "2026-08-31 12:30.999",
  "source_sn": "00001202608311230999",
  "waste_weight": 4.56,
  "weight_unit": "KG",
  "recorded_at": "2026-08-31T14:00:00.000+07:00",
  "device_id": "ANDROID-DEVICE-001"
}
```

Response `201 Created`:

```json
{
  "success": true,
  "data": {
    "client_waste_record_id": "bb078e58-9ffc-44c5-a5e9-40472ce223d7",
    "transaction_id": "bb078e58-9ffc-44c5-a5e9-40472ce223d7",
    "trcloud_reference_id": "TRC-WY-000001",
    "source_record_id": "2026-08-31 12:30.999",
    "source_sn": "00001202608311230999",
    "inbound_weight": 34.56,
    "waste_weight": 4.56,
    "net_yield_weight": 30.0,
    "yield_percentage": 86.81,
    "weight_unit": "KG",
    "branch_id": "BR-002",
    "branch_stock_weight_after": 80.0,
    "yield_finalized": true,
    "processed_by_user_id": "USR-1001",
    "processed_at": "2026-08-31T14:00:01.000+07:00",
    "status": "SUCCESS"
  },
  "request_id": "8d0195f8-9457-4a89-8b13-933f94622dad"
}
```

Response Data Types:

| Field | JSON Type |
|---|---|
| `client_waste_record_id`, `transaction_id`, `trcloud_reference_id` | `string` |
| `source_record_id`, `source_sn`, `weight_unit`, `branch_id` | `string` |
| `processed_by_user_id`, `processed_at`, `status` | `string` |
| `inbound_weight`, `waste_weight`, `net_yield_weight`, `yield_percentage`, `branch_stock_weight_after` | `number` |
| `yield_finalized` | `boolean` |

สูตร:

```text
net_yield_weight = inbound_weight - waste_weight
yield_percentage = (net_yield_weight / inbound_weight) x 100
```

กฎ:

- TRCloud ต้องดึง Inbound Weight จาก Source Record
- Waste Weight ต้องมากกว่า 0 และไม่มากกว่า Inbound Weight
- SUNFORD Integration API ต้องอ้างอิง Company และสาขาปัจจุบันจาก Session ที่ Login อยู่ ห้ามรับสาขาทำ Waste/Yield จาก Request Body
- Source Record ต้องมี Receipt อยู่ที่สาขาปัจจุบันที่ Login แล้วเท่านั้น
- หาก Receipt อยู่คนละสาขา ให้ตอบ `409 RECEIPT_BRANCH_MISMATCH` และห้ามสร้าง Waste/Yield
- TRCloud ต้องตรวจ Permission `WASTE_CREATE`, กำหนด `processed_by_user_id` จาก Access Token และสร้าง `processed_at` จากเวลาของ TRCloud
- Contract นี้ให้สร้าง Waste/Yield ได้ 1 ครั้งต่อ Source Record
- ถ้าสร้างแล้วตอบ `409 YIELD_ALREADY_FINALIZED` และห้ามสแกน SN เพื่อเริ่มบันทึกซ้ำอีก
- แอปสร้าง `client_waste_record_id` และ `transaction_id` ก่อนส่งคำขอ โดยใช้ UUID ค่าเดียวกัน
- TRCloud ต้องเก็บ Transaction ID ตามค่าที่แอปส่งและห้ามสร้างหรือเปลี่ยนค่า
- TRCloud เป็นผู้ตรวจและคืน Net Yield Weight, Yield Percentage และ `trcloud_reference_id`
- เมื่อบันทึก Waste/Yield สำเร็จ TRCloud ต้องหัก `waste_weight` ออกจาก Stock รวมตามน้ำหนักของสาขาปัจจุบัน และน้ำหนักคงเหลือของ SN เท่ากับ `net_yield_weight`
- Contract นี้บันทึกผล Waste และ Net Yield กับ SN เดิม โดยกำหนด `yield_finalized: true`
- การบันทึก Waste/Yield, การปรับน้ำหนัก Stock และการ Finalize SN ต้องสำเร็จใน Database Transaction เดียวกัน
- `Idempotency-Key` ต้องตรงกับ `client_waste_record_id`
- Retry ด้วย Key เดิมต้องคืน Transaction เดิมและห้ามสร้างซ้ำ

### 14.11.2 กฎ Receipt และการ Finalize SN

- หนึ่ง SN สร้าง Receipt ได้เพียงหนึ่งครั้ง และ Receipt ต้องเป็นการย้ายไปยังสาขาอื่นที่ไม่ใช่สาขาต้นทาง
- สาขารับและสาขาที่ทำ Waste/Yield ต้องอ้างอิงจากสาขาปัจจุบันของ Session ที่ Login อยู่
- หนึ่ง SN สร้าง Waste/Yield ได้เพียงหนึ่งครั้ง โดยบังคับ Unique Constraint ที่ `source_sn`
- เมื่อ Waste/Yield สำเร็จต้องกำหนด `yield_finalized: true` และห้ามสแกน SN นั้นเพื่อเริ่มบันทึกใหม่
- Android App และ API ทั้ง 6 เส้นไม่รองรับการยกเลิก Receipt, แก้สาขารับ หรือ Reverse Stock Movement
- กรณีผู้ใช้รับสินค้าผิดสาขา ให้ผู้มีสิทธิ์แก้ผ่าน **TRCloud Admin เท่านั้น** โดยไม่เพิ่ม API และต้องระบุเหตุผลก่อนยืนยัน
- สาขาที่แก้ใหม่ต้องไม่ใช่สาขาต้นทางของ SN และผู้ดำเนินการต้องมีสิทธิ์เข้าถึง Company และสาขาที่เกี่ยวข้อง
- หาก SN ยังไม่ทำ Waste/Yield ให้ TRCloud Admin ย้าย `transferred_weight` ออกจากยอดน้ำหนักของสาขาที่รับผิด ไปยังยอดน้ำหนักของสาขารับที่ถูกต้อง พร้อมแก้ Receiving Branch ของ Receipt เดิมใน Database Transaction เดียวกัน
- หาก SN ทำ Waste/Yield แล้ว ให้ TRCloud Admin ย้ายยอดคงเหลือ `net_yield_weight` พร้อมเปลี่ยนสาขาอ้างอิงของ Receipt และ Waste/Yield ที่เกี่ยวข้องใน Database Transaction เดียวกัน โดยห้ามสร้าง Receipt หรือ Waste/Yield รายการใหม่
- การแก้สาขาต้องคง SN, Receipt Reference ID, Source Record และประวัติเดิม ห้ามลบหรือเขียนทับหลักฐานการรับเดิม
- Audit Log ของการแก้สาขาต้องเก็บอย่างน้อย: SN, Receipt Reference ID, สาขาต้นทาง, สาขารับเดิม, สาขารับใหม่, น้ำหนักที่ย้าย, ยอดน้ำหนักก่อนและหลังของทั้งสองสาขาที่แก้, เหตุผล, ผู้แก้ และเวลาจาก TRCloud Server
- ทุกขั้นตอนต้องเก็บ Audit Log, ผู้ดำเนินการ และเวลาจาก TRCloud Server

### 14.12 Error Code ที่ใช้กับ 6 APIs

| HTTP | Error Code | ความหมาย |
|---:|---|---|
| 400 | `VALIDATION_ERROR` | Field หรือ Query ไม่ถูกต้อง |
| 401 | `LOGIN_FAILED` | Username หรือ Password ไม่ถูกต้อง |
| 401 | `TOKEN_INVALID` | Token ไม่ถูกต้องหรือหมดอายุ |
| 403 | `PERMISSION_DENIED` | User ไม่มีสิทธิ์ |
| 404 | `ITEM_NOT_FOUND` | ไม่พบสินค้า |
| 404 | `WEIGHING_RECORD_NOT_FOUND` | ไม่พบรายการจาก SN |
| 409 | `IDEMPOTENCY_CONFLICT` | Key เดิมแต่ข้อมูลต่างกัน |
| 409 | `IDENTIFIER_CONFLICT` | Record ID, SN หรือ Transaction ID ซ้ำกับรายการอื่น |
| 409 | `SN_NOT_UNIQUE` | SN พบมากกว่า 1 รายการ |
| 409 | `SAME_BRANCH_TRANSFER_NOT_ALLOWED` | สาขาที่ Login ตรงกับสาขาต้นทาง จึงห้ามรับหรือย้าย Stock |
| 409 | `RECEIPT_ALREADY_EXISTS` | SN มี Receipt อยู่ที่สาขาอื่นแล้ว |
| 409 | `STOCK_BALANCE_CONFLICT` | ยอดหรือสาขาเจ้าของ Stock ไม่ตรงกับ Source Record |
| 409 | `RECEIPT_BRANCH_MISMATCH` | Receipt ของ SN ไม่อยู่ในสาขาที่ Login |
| 409 | `YIELD_ALREADY_FINALIZED` | SN บันทึก Waste/Yield สำเร็จแล้วและห้ามเริ่มซ้ำ |
| 422 | `ITEM_INACTIVE` | สินค้าไม่พร้อมใช้งาน |
| 422 | `WEIGHT_INVALID` | น้ำหนักรับเข้าไม่ถูกต้อง |
| 422 | `WASTE_WEIGHT_INVALID` | น้ำหนักของเสียไม่ถูกต้อง |
| 500 | `INTERNAL_ERROR` | TRCloud Internal Error |
| 503 | `SERVICE_UNAVAILABLE` | TRCloud ไม่พร้อมใช้งาน |

Error ทุกครั้งต้องคืน JSON และ `request_id` โดยไม่แสดง Password, Token, Stack Trace หรือข้อมูลอ่อนไหว

### 14.13 กำหนดส่งมอบ 6 APIs จาก TRCloud

| Deadline (`Asia/Bangkok`) | API ที่ต้องพร้อมบน Sandbox |
|---|---|
| วันที่ 1 - พุธ 9 กันยายน 2026 เวลา 12:00 น. | ยืนยัน Contract, Base URL, Credential และ Technical Contact |
| วันที่ 2 - พฤหัสบดี 10 กันยายน 2026 เวลา 17:00 น. | API 1 - Login |
| วันที่ 3 - ศุกร์ 11 กันยายน 2026 เวลา 17:00 น. | API 2 - Search SKU และ API 3 - Get Item |
| วันที่ 5 - จันทร์ 14 กันยายน 2026 เวลา 17:00 น. | API 4 - Create Weighing Record |
| วันที่ 7 - พุธ 16 กันยายน 2026 เวลา 17:00 น. | API 5 - Receive by SN และ Stock Transfer |
| วันที่ 9 - ศุกร์ 18 กันยายน 2026 เวลา 17:00 น. | API 6 - Create Waste Weighing Record |
| วันที่ 11 - จันทร์ 21 กันยายน 2026 เวลา 12:00 น. | ทั้ง 6 APIs ตรึง Field/Error Code พร้อม OpenAPI, API Collection และ Integration Test Data |
| วันที่ 12 - อังคาร 22 กันยายน 2026 เวลา 17:00 น. | TRCloud แก้ Blocker/Critical จาก Integration Test |
| วันที่ 13 - พุธ 23 กันยายน 2026 เวลา 09:00-17:00 น. | TRCloud สนับสนุน UAT และตรวจ Transaction จริง |

รายละเอียดสิ่งส่งมอบและหลักฐานตรวจรับให้ยึดหัวข้อ 4.3 ระหว่างรอ Endpoint จริง SUNFORD ใช้ Mock Server ตาม 6 APIs นี้ได้ แต่ Milestone จะผ่านเมื่อทดสอบกับ TRCloud Sandbox สำเร็จ

### 14.14 UAT Acceptance Criteria

1. Login คืน Access Token, User Profile, Permission, Company และ Branch ครบ
2. Search SKU คืนรายการตรงกับ TRCloud
3. Get Item by Item ID คืนรายละเอียดและหน่วย KG ถูกต้อง
4. Android App สร้าง Record ID และ SN แล้วส่ง Create Weighing ขณะเชื่อมต่ออินเทอร์เน็ต
5. SKU `00001` และ Record `2026-08-31 12:30.999` สร้าง SN `00001202608311230999` ในแอปตรงตามเอกสาร
6. แอปสร้าง QR Code และ Barcode Code 128 จาก SN ค่าเดียวกัน พร้อมพิมพ์ฉลากขนาด `6 × 4 cm` ที่มีเฉพาะชื่อสินค้า, วันที่–เวลาบันทึก, QR Code และ Barcode หลัง TRCloud ยืนยัน SN สำเร็จแล้วเท่านั้น
7. Create Weighing ส่ง Record ID/SN และน้ำหนักสุทธิ โดย Source Branch อ้างอิงจาก Session ที่ Login และ TRCloud เพิ่มน้ำหนักเข้า Stock รวมของสาขานั้น
8. Retry Create Weighing ด้วย Idempotency Key เดิมไม่สร้างรายการซ้ำหรือเปลี่ยนรหัส
9. แอปสแกน QR Code และส่ง Receive Request โดยอ้างอิงสาขารับจาก Session ที่ Login เท่านั้น
10. TRCloud ปฏิเสธทันทีหากสาขาที่ Login ตรงกับสาขาต้นทาง
11. TRCloud สร้าง Receipt และ Stock Movement, ลดยอดน้ำหนักต้นทางและเพิ่มยอดน้ำหนักสาขาที่สแกนใน Transaction เดียวกัน
12. Retry Receive ด้วย Idempotency Key เดิมคืน Receipt เดิมและไม่ย้าย Stock ซ้ำ
13. หนึ่ง SN ต้องมี Receipt ได้เพียงหนึ่งรายการ และการสแกนพร้อมกันจากสองสาขาต้องมีเพียงหนึ่งคำขอที่สร้าง Receipt สำเร็จ
14. App สร้าง Transaction ID ของ Waste/Yield และส่งคำขอขณะเชื่อมต่ออินเทอร์เน็ต
15. Create Waste Weighing ส่ง Transaction ID ที่แอปสร้าง และ TRCloud เก็บพร้อม Echo ค่าเดิมกลับมา
16. Waste/Yield ต้องอ้างอิงสาขาจาก Session ที่ Login และถูกปฏิเสธหาก Receipt ไม่ได้อยู่ที่สาขานั้น
17. Waste Weight มากกว่า Inbound Weight ถูกปฏิเสธ
18. เมื่อ Waste/Yield สำเร็จต้องกำหนด `yield_finalized: true` และ SN เดิมต้องไม่สามารถสแกนเพื่อเริ่มบันทึกซ้ำได้
19. Retry Create Waste ด้วย Idempotency Key เดิมไม่สร้าง Transaction ซ้ำหรือเปลี่ยน Transaction ID
20. หาก SN ซ้ำก่อนพิมพ์ฉลาก แอปต้องสร้างรหัสใหม่ด้วย Idempotency Key ใหม่ และห้ามพิมพ์ SN ที่ TRCloud ยังไม่ยืนยัน
21. User ไม่สามารถรับ Stock, อ่าน หรือสร้างข้อมูลข้าม Company/Branch ที่ไม่มีสิทธิ์
22. Error ทุกกรณีเป็น JSON และมี Request ID
23. ผู้รับสินค้ามาจาก Access Token และ `received_at` มาจากเวลาของ TRCloud Server เท่านั้น
24. หลัง Waste/Yield สำเร็จ TRCloud หัก Waste Weight จาก Stock รวมของสาขาและ Finalize SN ใน Transaction เดียวกัน
25. กรณีรับผิดสาขา ผู้มีสิทธิ์แก้ได้ผ่าน TRCloud Admin โดยปรับ Receipt, ข้อมูลที่เกี่ยวข้อง และยอดน้ำหนักของสาขาที่ได้รับผลกระทบใน Transaction เดียว พร้อม Audit Log ครบถ้วน โดยไม่เพิ่ม API
26. OpenAPI/API Collection ตรงกับ 6 Endpoints ในเอกสารนี้

การเพิ่ม API เส้นที่ 7 หรือเปลี่ยน Method, Endpoint, Field, รูปแบบ SN/QR Code/Barcode, สูตร Yield หรือ Error Code ต้องได้รับการยืนยันจาก SUNFORD ก่อน
