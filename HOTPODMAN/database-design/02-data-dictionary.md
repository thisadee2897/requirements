# พจนานุกรมข้อมูล HOTPOTMAN ทั้งระบบ

สถานะ: แบบออกแบบ ยังไม่ได้สร้างฐานข้อมูลหรือรัน Migration

รวม 128 ตารางเชิงตรรกะ แบ่งสร้างตามเฟส ไม่ใช่ข้อกำหนดให้สร้างทั้งหมดในวันแรก

## วิธีอ่าน

- `F` Foundation, `P` Purchasing/Delivery Phase 1, `W` Weighing/Warehouse, `O` Operations, `R` Reporting/Integration delivery; ดูแผนใน 04-migration-and-acceptance.md
- ทุกตารางมี `id uuid PK`; tenant table มี `company_id` และต้องมี `UNIQUE(company_id,id)` เพื่อใช้ composite FK กฎนี้รวมตาราง join ที่มี surrogate id
- `U` unique, `I` index; reference คอลัมน์แสดง FK target เชิงตรรกะ ใน implementation ต้องขยาย company_id ตามกฎ composite FK ใน 03-invariants-and-transactions.md
- เว้นแต่ระบุ `?`/nullable ในตาราง คอลัมน์เป็น NOT NULL; default id=UUID, created_at/updated_at=now(), version=1; ค่าอื่นต้องส่ง explicit หรือค่าที่ระบุใน policy ไม่เดา default
- Append table ไม่มี updated_at/version; ห้าม runtime update/delete business content ใช้ reversal ใหม่ ส่วน state-machine/projection เป็น mutable ตามกฎ
- JSON ใช้ snapshot/config/payload ที่ validate schema และ version ไม่ใช้แทน FK/จำนวน/เงินหลัก; address/locale text เป็นข้อมูลธุรกิจ ไม่ใช่คำสั่ง
- UUID ไม่รับประกัน tenant isolation; actor FK global user ต้องตรวจ membership ณ เวลา action และเก็บ audit เมื่อสิทธิ์เปลี่ยนภายหลัง
- FK ปริยาย `ON DELETE RESTRICT`; ไม่มี cascade ลบประวัติ เอกสาร immutable ตอน confirm/post แม้ระบุ mutable สำหรับ draft/state
- Field status/kind ใช้ text + CHECK allowlist ตาม 03; ไม่เปิดรับค่าอิสระจาก client

## `geo.provinces`

**เฟส:** F · **หนึ่งแถวคือ:** หนึ่งจังหวัด/กรุงเทพมหานคร · **ประเภท:** mutable

**คำอธิบาย:** ตารางเก็บข้อมูล หนึ่งจังหวัด/กรุงเทพมหานคร; หนึ่งแถวมีความหมายตามนี้และอยู่ในเฟส F

| คอลัมน์ | PostgreSQL type | NULL | PK / FK | อ้างอิง | คำอธิบายภาษาไทย |
|---|---|---|---|---|---|
| `id` | `uuid` | ไม่ได้ | PK | — | รหัสหลักภายในของแถวข้อมูล ไม่เปลี่ยนตลอดอายุรายการ; Primary Key ชนิด UUID ห้ามซ้ำหรือเป็น NULL |
| `official_code` | `text` | ไม่ได้ | — | — | รหัสพื้นที่ทางการ เก็บข้อความแยกจาก UUID |
| `name_th` | `text` | ไม่ได้ | — | — | ชื่อภาษาไทย |
| `name_en` | `text` | ได้ | — | — | ชื่อภาษาอังกฤษ |
| `active` | `boolean` | ไม่ได้ | — | — | สถานะเปิดใช้งาน |
| `source_ref` | `text` | ไม่ได้ | — | — | แหล่งข้อมูลอ้างอิงที่ตรวจสอบย้อนกลับได้ |
| `source_version` | `text` | ไม่ได้ | — | — | รุ่นข้อมูลต้นทาง |
| `created_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่สร้างแถวข้อมูลในระบบ; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `updated_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่แก้ไขแถวข้อมูลล่าสุด ต้องอัปเดตทุกช่องทางเขียน; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `version` | `integer` | ไม่ได้ | — | — | เลขรุ่นแถวสำหรับตรวจการแก้ไขพร้อมกัน |

**Keys / Index:** U(official_code)

**กฎเฉพาะ:** global reference; runtime read-only; รหัสทางการเป็น text แยกจาก UUID; ไม่ลบรายการที่เคยอ้างอิง

## `geo.districts`

**เฟส:** F · **หนึ่งแถวคือ:** หนึ่งอำเภอ/เขต · **ประเภท:** mutable

**คำอธิบาย:** ตารางเก็บข้อมูล หนึ่งอำเภอ/เขต; หนึ่งแถวมีความหมายตามนี้และอยู่ในเฟส F

| คอลัมน์ | PostgreSQL type | NULL | PK / FK | อ้างอิง | คำอธิบายภาษาไทย |
|---|---|---|---|---|---|
| `id` | `uuid` | ไม่ได้ | PK | — | รหัสหลักภายในของแถวข้อมูล ไม่เปลี่ยนตลอดอายุรายการ; Primary Key ชนิด UUID ห้ามซ้ำหรือเป็น NULL |
| `province_id` | `uuid` | ไม่ได้ | FK | `geo.provinces.id` | รหัสอ้างอิง หนึ่งจังหวัด/กรุงเทพมหานคร ไปยัง geo.provinces.id (บทบาทฟิลด์ province_id) |
| `official_code` | `text` | ไม่ได้ | — | — | รหัสพื้นที่ทางการ เก็บข้อความแยกจาก UUID |
| `name_th` | `text` | ไม่ได้ | — | — | ชื่อภาษาไทย |
| `name_en` | `text` | ได้ | — | — | ชื่อภาษาอังกฤษ |
| `active` | `boolean` | ไม่ได้ | — | — | สถานะเปิดใช้งาน |
| `source_ref` | `text` | ไม่ได้ | — | — | แหล่งข้อมูลอ้างอิงที่ตรวจสอบย้อนกลับได้ |
| `source_version` | `text` | ไม่ได้ | — | — | รุ่นข้อมูลต้นทาง |
| `created_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่สร้างแถวข้อมูลในระบบ; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `updated_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่แก้ไขแถวข้อมูลล่าสุด ต้องอัปเดตทุกช่องทางเขียน; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `version` | `integer` | ไม่ได้ | — | — | เลขรุ่นแถวสำหรับตรวจการแก้ไขพร้อมกัน |

**Keys / Index:** U(official_code); U(province_id,id)

**กฎเฉพาะ:** global reference; parent geography ห้ามเปลี่ยนเมื่อใช้งานแล้ว ให้สร้าง record ใหม่และ retire record เดิม

## `geo.subdistricts`

**เฟส:** F · **หนึ่งแถวคือ:** หนึ่งตำบล/แขวง · **ประเภท:** mutable

**คำอธิบาย:** ตารางเก็บข้อมูล หนึ่งตำบล/แขวง; หนึ่งแถวมีความหมายตามนี้และอยู่ในเฟส F

| คอลัมน์ | PostgreSQL type | NULL | PK / FK | อ้างอิง | คำอธิบายภาษาไทย |
|---|---|---|---|---|---|
| `id` | `uuid` | ไม่ได้ | PK | — | รหัสหลักภายในของแถวข้อมูล ไม่เปลี่ยนตลอดอายุรายการ; Primary Key ชนิด UUID ห้ามซ้ำหรือเป็น NULL |
| `district_id` | `uuid` | ไม่ได้ | FK | `geo.districts.id` | รหัสอ้างอิง หนึ่งอำเภอ/เขต ไปยัง geo.districts.id (บทบาทฟิลด์ district_id) |
| `official_code` | `text` | ไม่ได้ | — | — | รหัสพื้นที่ทางการ เก็บข้อความแยกจาก UUID |
| `name_th` | `text` | ไม่ได้ | — | — | ชื่อภาษาไทย |
| `name_en` | `text` | ได้ | — | — | ชื่อภาษาอังกฤษ |
| `active` | `boolean` | ไม่ได้ | — | — | สถานะเปิดใช้งาน |
| `source_ref` | `text` | ไม่ได้ | — | — | แหล่งข้อมูลอ้างอิงที่ตรวจสอบย้อนกลับได้ |
| `source_version` | `text` | ไม่ได้ | — | — | รุ่นข้อมูลต้นทาง |
| `created_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่สร้างแถวข้อมูลในระบบ; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `updated_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่แก้ไขแถวข้อมูลล่าสุด ต้องอัปเดตทุกช่องทางเขียน; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `version` | `integer` | ไม่ได้ | — | — | เลขรุ่นแถวสำหรับตรวจการแก้ไขพร้อมกัน |

**Keys / Index:** U(official_code); U(district_id,id)

**กฎเฉพาะ:** global reference; parent geography immutable หลังใช้งาน; ไม่ hard delete

## `geo.postal_codes`

**เฟส:** F · **หนึ่งแถวคือ:** หนึ่งรหัสไปรษณีย์ไทย · **ประเภท:** mutable

**คำอธิบาย:** ตารางเก็บข้อมูล หนึ่งรหัสไปรษณีย์ไทย; หนึ่งแถวมีความหมายตามนี้และอยู่ในเฟส F

| คอลัมน์ | PostgreSQL type | NULL | PK / FK | อ้างอิง | คำอธิบายภาษาไทย |
|---|---|---|---|---|---|
| `id` | `uuid` | ไม่ได้ | PK | — | รหัสหลักภายในของแถวข้อมูล ไม่เปลี่ยนตลอดอายุรายการ; Primary Key ชนิด UUID ห้ามซ้ำหรือเป็น NULL |
| `code` | `text` | ไม่ได้ | — | — | รหัสธุรกิจของรายการตามขอบเขต Unique ของตาราง |
| `active` | `boolean` | ไม่ได้ | — | — | สถานะเปิดใช้งาน |
| `source_ref` | `text` | ไม่ได้ | — | — | แหล่งข้อมูลอ้างอิงที่ตรวจสอบย้อนกลับได้ |
| `source_version` | `text` | ไม่ได้ | — | — | รุ่นข้อมูลต้นทาง |
| `created_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่สร้างแถวข้อมูลในระบบ; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `updated_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่แก้ไขแถวข้อมูลล่าสุด ต้องอัปเดตทุกช่องทางเขียน; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `version` | `integer` | ไม่ได้ | — | — | เลขรุ่นแถวสำหรับตรวจการแก้ไขพร้อมกัน |

**Keys / Index:** U(code)

**กฎเฉพาะ:** CHECK code เป็นเลข 5 หลัก; เก็บ text ไม่ integer; id เป็น UUID; ไม่ใช้รหัสไปรษณีย์อนุมานจังหวัดโดยไม่มี mapping

## `geo.subdistrict_postal_codes`

**เฟส:** F · **หนึ่งแถวคือ:** หนึ่งคู่ตำบลกับรหัสไปรษณีย์ที่อนุญาต · **ประเภท:** mutable

**คำอธิบาย:** ตารางเก็บข้อมูล หนึ่งคู่ตำบลกับรหัสไปรษณีย์ที่อนุญาต; หนึ่งแถวมีความหมายตามนี้และอยู่ในเฟส F

| คอลัมน์ | PostgreSQL type | NULL | PK / FK | อ้างอิง | คำอธิบายภาษาไทย |
|---|---|---|---|---|---|
| `id` | `uuid` | ไม่ได้ | PK | — | รหัสหลักภายในของแถวข้อมูล ไม่เปลี่ยนตลอดอายุรายการ; Primary Key ชนิด UUID ห้ามซ้ำหรือเป็น NULL |
| `subdistrict_id` | `uuid` | ไม่ได้ | FK | `geo.subdistricts.id` | รหัสอ้างอิง หนึ่งตำบล/แขวง ไปยัง geo.subdistricts.id (บทบาทฟิลด์ subdistrict_id) |
| `postal_code_id` | `uuid` | ไม่ได้ | FK | `geo.postal_codes.id` | รหัสอ้างอิง หนึ่งรหัสไปรษณีย์ไทย ไปยัง geo.postal_codes.id (บทบาทฟิลด์ postal_code_id) |
| `coverage_note` | `text` | ได้ | — | — | ข้อจำกัดหรือคำอธิบายพื้นที่ให้บริการไปรษณีย์ |
| `active` | `boolean` | ไม่ได้ | — | — | สถานะเปิดใช้งาน |
| `source_ref` | `text` | ไม่ได้ | — | — | แหล่งข้อมูลอ้างอิงที่ตรวจสอบย้อนกลับได้ |
| `source_version` | `text` | ไม่ได้ | — | — | รุ่นข้อมูลต้นทาง |
| `created_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่สร้างแถวข้อมูลในระบบ; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `updated_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่แก้ไขแถวข้อมูลล่าสุด ต้องอัปเดตทุกช่องทางเขียน; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `version` | `integer` | ไม่ได้ | — | — | เลขรุ่นแถวสำหรับตรวจการแก้ไขพร้อมกัน |

**Keys / Index:** U(subdistrict_id,postal_code_id); I(postal_code_id)

**กฎเฉพาะ:** many-to-many mapping; ตรวจ coverage เพิ่มเมื่อพื้นที่ย่อยมีเงื่อนไข; ไม่ลบ mapping ที่ถูกใช้; เปลี่ยน active ผ่าน reference import เท่านั้น

## `org.companies`

**เฟส:** F · **หนึ่งแถวคือ:** หนึ่งบริษัท · **ประเภท:** mutable

**คำอธิบาย:** ตารางเก็บข้อมูล หนึ่งบริษัท; หนึ่งแถวมีความหมายตามนี้และอยู่ในเฟส F

| คอลัมน์ | PostgreSQL type | NULL | PK / FK | อ้างอิง | คำอธิบายภาษาไทย |
|---|---|---|---|---|---|
| `id` | `uuid` | ไม่ได้ | PK | — | รหัสหลักภายในของแถวข้อมูล ไม่เปลี่ยนตลอดอายุรายการ; Primary Key ชนิด UUID ห้ามซ้ำหรือเป็น NULL |
| `code` | `text` | ไม่ได้ | — | — | รหัสธุรกิจของรายการตามขอบเขต Unique ของตาราง |
| `legal_name` | `text` | ไม่ได้ | — | — | ชื่อจดทะเบียนตามกฎหมาย |
| `tax_id` | `text` | ได้ | — | — | เลขประจำตัวผู้เสียภาษี เก็บข้อความ |
| `address_line1` | `text` | ไม่ได้ | — | — | รายละเอียดที่อยู่หลัก บ้านเลขที่ อาคาร หมู่ ซอย ถนน |
| `address_line2` | `text` | ได้ | — | — | รายละเอียดที่อยู่เพิ่มเติม |
| `province_id` | `uuid` | ไม่ได้ | FK | `geo.provinces.id` | รหัสอ้างอิง หนึ่งจังหวัด/กรุงเทพมหานคร ไปยัง geo.provinces.id (บทบาทฟิลด์ province_id) |
| `district_id` | `uuid` | ไม่ได้ | FK | `geo.districts.id` | รหัสอ้างอิง หนึ่งอำเภอ/เขต ไปยัง geo.districts.id (บทบาทฟิลด์ district_id) |
| `subdistrict_id` | `uuid` | ไม่ได้ | FK | `geo.subdistricts.id` | รหัสอ้างอิง หนึ่งตำบล/แขวง ไปยัง geo.subdistricts.id (บทบาทฟิลด์ subdistrict_id) |
| `postal_code_id` | `uuid` | ไม่ได้ | FK | `geo.postal_codes.id` | รหัสอ้างอิง หนึ่งรหัสไปรษณีย์ไทย ไปยัง geo.postal_codes.id (บทบาทฟิลด์ postal_code_id) |
| `timezone` | `text` | ไม่ได้ | — | — | ชื่อเขตเวลาธุรกิจแบบ IANA เช่น Asia/Bangkok |
| `base_currency` | `char(3)` | ไม่ได้ | — | — | สกุลเงินหลักของบริษัท |
| `active` | `boolean` | ไม่ได้ | — | — | สถานะเปิดใช้งาน |
| `created_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่สร้างแถวข้อมูลในระบบ; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `updated_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่แก้ไขแถวข้อมูลล่าสุด ต้องอัปเดตทุกช่องทางเขียน; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `version` | `integer` | ไม่ได้ | — | — | เลขรุ่นแถวสำหรับตรวจการแก้ไขพร้อมกัน |

**Keys / Index:** U(code)

**กฎเฉพาะ:** สร้างสำนักงานใหญ่และคลังหลักใน transaction เดียว ห้าม hard delete บริษัทที่ provision แล้ว; structured Thai address: composite geography FKs + postal mapping ตาม 07-address-model.md

## `org.branches`

**เฟส:** F · **หนึ่งแถวคือ:** หนึ่งสาขาในบริษัท · **ประเภท:** mutable

**คำอธิบาย:** ตารางเก็บข้อมูล หนึ่งสาขาในบริษัท; หนึ่งแถวมีความหมายตามนี้และอยู่ในเฟส F

| คอลัมน์ | PostgreSQL type | NULL | PK / FK | อ้างอิง | คำอธิบายภาษาไทย |
|---|---|---|---|---|---|
| `id` | `uuid` | ไม่ได้ | PK | — | รหัสหลักภายในของแถวข้อมูล ไม่เปลี่ยนตลอดอายุรายการ; Primary Key ชนิด UUID ห้ามซ้ำหรือเป็น NULL |
| `company_id` | `uuid` | ไม่ได้ | FK | `org.companies.id` | รหัสอ้างอิงบริษัทเจ้าของข้อมูล ไปยัง org.companies.id (บทบาทฟิลด์ company_id) |
| `code` | `text` | ไม่ได้ | — | — | รหัสธุรกิจของรายการตามขอบเขต Unique ของตาราง |
| `name` | `text` | ไม่ได้ | — | — | ชื่อรายการสำหรับแสดงผล |
| `is_head_office` | `boolean` | ไม่ได้ | — | — | ระบุว่าเป็นสำนักงานใหญ่ของบริษัท |
| `active` | `boolean` | ไม่ได้ | — | — | สถานะเปิดใช้งาน |
| `address_line1` | `text` | ไม่ได้ | — | — | รายละเอียดที่อยู่หลัก บ้านเลขที่ อาคาร หมู่ ซอย ถนน |
| `address_line2` | `text` | ได้ | — | — | รายละเอียดที่อยู่เพิ่มเติม |
| `province_id` | `uuid` | ไม่ได้ | FK | `geo.provinces.id` | รหัสอ้างอิง หนึ่งจังหวัด/กรุงเทพมหานคร ไปยัง geo.provinces.id (บทบาทฟิลด์ province_id) |
| `district_id` | `uuid` | ไม่ได้ | FK | `geo.districts.id` | รหัสอ้างอิง หนึ่งอำเภอ/เขต ไปยัง geo.districts.id (บทบาทฟิลด์ district_id) |
| `subdistrict_id` | `uuid` | ไม่ได้ | FK | `geo.subdistricts.id` | รหัสอ้างอิง หนึ่งตำบล/แขวง ไปยัง geo.subdistricts.id (บทบาทฟิลด์ subdistrict_id) |
| `postal_code_id` | `uuid` | ไม่ได้ | FK | `geo.postal_codes.id` | รหัสอ้างอิง หนึ่งรหัสไปรษณีย์ไทย ไปยัง geo.postal_codes.id (บทบาทฟิลด์ postal_code_id) |
| `contact` | `jsonb` | ไม่ได้ | — | — | รายละเอียดการติดต่อที่ตรวจรูปแบบแล้ว; ต้องตรวจ schema และจำกัดข้อมูลตามสิทธิ์ |
| `created_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่สร้างแถวข้อมูลในระบบ; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `updated_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่แก้ไขแถวข้อมูลล่าสุด ต้องอัปเดตทุกช่องทางเขียน; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `version` | `integer` | ไม่ได้ | — | — | เลขรุ่นแถวสำหรับตรวจการแก้ไขพร้อมกัน |

**Keys / Index:** U(company_id,code); partial U(company_id) WHERE is_head_office

**กฎเฉพาะ:** สำนักงานใหญ่ต้อง active และเปลี่ยน identity/company/type ไม่ได้; deferred exact-one trigger ทุกบริษัท; structured Thai address: composite geography FKs + postal mapping ตาม 07-address-model.md

## `org.warehouses`

**เฟส:** F · **หนึ่งแถวคือ:** หนึ่งคลังในสาขา · **ประเภท:** mutable

**คำอธิบาย:** ตารางเก็บข้อมูล หนึ่งคลังในสาขา; หนึ่งแถวมีความหมายตามนี้และอยู่ในเฟส F

| คอลัมน์ | PostgreSQL type | NULL | PK / FK | อ้างอิง | คำอธิบายภาษาไทย |
|---|---|---|---|---|---|
| `id` | `uuid` | ไม่ได้ | PK | — | รหัสหลักภายในของแถวข้อมูล ไม่เปลี่ยนตลอดอายุรายการ; Primary Key ชนิด UUID ห้ามซ้ำหรือเป็น NULL |
| `company_id` | `uuid` | ไม่ได้ | FK | `org.companies.id` | รหัสอ้างอิงบริษัทเจ้าของข้อมูล ไปยัง org.companies.id (บทบาทฟิลด์ company_id) |
| `branch_id` | `uuid` | ไม่ได้ | FK | `org.branches.id` | รหัสอ้างอิงสาขาเจ้าของรายการ ไปยัง org.branches.id (บทบาทฟิลด์ branch_id) |
| `code` | `text` | ไม่ได้ | — | — | รหัสธุรกิจของรายการตามขอบเขต Unique ของตาราง |
| `name` | `text` | ไม่ได้ | — | — | ชื่อรายการสำหรับแสดงผล |
| `is_default` | `boolean` | ไม่ได้ | — | — | ระบุว่าเป็นรายการหลักหรือค่าเริ่มต้นของกลุ่ม |
| `active` | `boolean` | ไม่ได้ | — | — | สถานะเปิดใช้งาน |
| `created_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่สร้างแถวข้อมูลในระบบ; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `updated_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่แก้ไขแถวข้อมูลล่าสุด ต้องอัปเดตทุกช่องทางเขียน; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `version` | `integer` | ไม่ได้ | — | — | เลขรุ่นแถวสำหรับตรวจการแก้ไขพร้อมกัน |

**Keys / Index:** U(company_id,branch_id,code); partial U(company_id,branch_id) WHERE is_default

**กฎเฉพาะ:** ทุกสาขาต้องมีคลังหลักหนึ่งแห่ง ลบไม่ได้ active เมื่อสาขา active

## `org.locations`

**เฟส:** W · **หนึ่งแถวคือ:** หนึ่งโหนดสถานที่จริง · **ประเภท:** mutable

**คำอธิบาย:** ตารางเก็บข้อมูล หนึ่งโหนดสถานที่จริง; หนึ่งแถวมีความหมายตามนี้และอยู่ในเฟส W

| คอลัมน์ | PostgreSQL type | NULL | PK / FK | อ้างอิง | คำอธิบายภาษาไทย |
|---|---|---|---|---|---|
| `id` | `uuid` | ไม่ได้ | PK | — | รหัสหลักภายในของแถวข้อมูล ไม่เปลี่ยนตลอดอายุรายการ; Primary Key ชนิด UUID ห้ามซ้ำหรือเป็น NULL |
| `company_id` | `uuid` | ไม่ได้ | FK | `org.companies.id` | รหัสอ้างอิงบริษัทเจ้าของข้อมูล ไปยัง org.companies.id (บทบาทฟิลด์ company_id) |
| `warehouse_id` | `uuid` | ไม่ได้ | FK | `org.warehouses.id` | รหัสอ้างอิงคลังที่เกี่ยวข้อง ไปยัง org.warehouses.id (บทบาทฟิลด์ warehouse_id) |
| `parent_id` | `uuid` | ได้ | FK | `org.locations.id` | รหัสอ้างอิง หนึ่งโหนดสถานที่จริง ไปยัง org.locations.id (บทบาทฟิลด์ parent_id) |
| `code` | `text` | ไม่ได้ | — | — | รหัสธุรกิจของรายการตามขอบเขต Unique ของตาราง |
| `name` | `text` | ไม่ได้ | — | — | ชื่อรายการสำหรับแสดงผล |
| `kind` | `text` | ไม่ได้ | — | — | ชนิดรายการตามค่าที่อนุญาตของตาราง |
| `is_stockable` | `boolean` | ไม่ได้ | — | — | ระบุว่าสถานที่นี้รับเก็บยอดสต็อกได้ |
| `active` | `boolean` | ไม่ได้ | — | — | สถานะเปิดใช้งาน |
| `created_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่สร้างแถวข้อมูลในระบบ; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `updated_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่แก้ไขแถวข้อมูลล่าสุด ต้องอัปเดตทุกช่องทางเขียน; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `version` | `integer` | ไม่ได้ | — | — | เลขรุ่นแถวสำหรับตรวจการแก้ไขพร้อมกัน |

**Keys / Index:** U(company_id,warehouse_id,code); I(company_id,parent_id)

**กฎเฉพาะ:** ZONE/COLD_ROOM/RACK/BIN/STAGING; parent warehouse เดียวกัน ห้ามวงจร; posting ใช้ stockable leaf

## `org.usage_points`

**เฟส:** W · **หนึ่งแถวคือ:** หนึ่งจุดใช้งาน/ครัว · **ประเภท:** mutable

**คำอธิบาย:** ตารางเก็บข้อมูล หนึ่งจุดใช้งาน/ครัว; หนึ่งแถวมีความหมายตามนี้และอยู่ในเฟส W

| คอลัมน์ | PostgreSQL type | NULL | PK / FK | อ้างอิง | คำอธิบายภาษาไทย |
|---|---|---|---|---|---|
| `id` | `uuid` | ไม่ได้ | PK | — | รหัสหลักภายในของแถวข้อมูล ไม่เปลี่ยนตลอดอายุรายการ; Primary Key ชนิด UUID ห้ามซ้ำหรือเป็น NULL |
| `company_id` | `uuid` | ไม่ได้ | FK | `org.companies.id` | รหัสอ้างอิงบริษัทเจ้าของข้อมูล ไปยัง org.companies.id (บทบาทฟิลด์ company_id) |
| `branch_id` | `uuid` | ไม่ได้ | FK | `org.branches.id` | รหัสอ้างอิงสาขาเจ้าของรายการ ไปยัง org.branches.id (บทบาทฟิลด์ branch_id) |
| `code` | `text` | ไม่ได้ | — | — | รหัสธุรกิจของรายการตามขอบเขต Unique ของตาราง |
| `name` | `text` | ไม่ได้ | — | — | ชื่อรายการสำหรับแสดงผล |
| `active` | `boolean` | ไม่ได้ | — | — | สถานะเปิดใช้งาน |
| `created_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่สร้างแถวข้อมูลในระบบ; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `updated_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่แก้ไขแถวข้อมูลล่าสุด ต้องอัปเดตทุกช่องทางเขียน; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `version` | `integer` | ไม่ได้ | — | — | เลขรุ่นแถวสำหรับตรวจการแก้ไขพร้อมกัน |

**Keys / Index:** U(company_id,branch_id,code)

**กฎเฉพาะ:** ใช้กฎ tenant, FK และ audit กลาง

## `security.users`

**เฟส:** F · **หนึ่งแถวคือ:** หนึ่งตัวตนผู้ใช้กลาง · **ประเภท:** mutable

**คำอธิบาย:** ตารางเก็บข้อมูล หนึ่งตัวตนผู้ใช้กลาง; หนึ่งแถวมีความหมายตามนี้และอยู่ในเฟส F

| คอลัมน์ | PostgreSQL type | NULL | PK / FK | อ้างอิง | คำอธิบายภาษาไทย |
|---|---|---|---|---|---|
| `id` | `uuid` | ไม่ได้ | PK | — | รหัสหลักภายในของแถวข้อมูล ไม่เปลี่ยนตลอดอายุรายการ; Primary Key ชนิด UUID ห้ามซ้ำหรือเป็น NULL |
| `username` | `text` | ไม่ได้ | — | — | ชื่อผู้ใช้สำหรับเข้าสู่ระบบ |
| `email` | `text` | ไม่ได้ | — | — | อีเมลสำหรับติดต่อหรือเข้าสู่ระบบ |
| `password_hash` | `text` | ไม่ได้ | — | — | ค่าแฮชรหัสผ่าน ห้ามคืนผ่าน API หรือบันทึกใน log |
| `active` | `boolean` | ไม่ได้ | — | — | สถานะเปิดใช้งาน |
| `locale` | `text` | ไม่ได้ | — | — | รหัสภาษาที่ใช้แสดงผล |
| `last_login_at` | `timestamptz` | ได้ | — | — | เวลาที่เข้าสู่ระบบสำเร็จล่าสุด; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `created_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่สร้างแถวข้อมูลในระบบ; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `updated_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่แก้ไขแถวข้อมูลล่าสุด ต้องอัปเดตทุกช่องทางเขียน; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `version` | `integer` | ไม่ได้ | — | — | เลขรุ่นแถวสำหรับตรวจการแก้ไขพร้อมกัน |

**Keys / Index:** U(lower(username)); U(lower(email))

**กฎเฉพาะ:** ไม่ hard delete; locale th/lo/zh/my; ไม่เผย hash

## `security.memberships`

**เฟส:** F · **หนึ่งแถวคือ:** หนึ่งสมาชิกต่อบริษัท · **ประเภท:** mutable

**คำอธิบาย:** ตารางเก็บข้อมูล หนึ่งสมาชิกต่อบริษัท; หนึ่งแถวมีความหมายตามนี้และอยู่ในเฟส F

| คอลัมน์ | PostgreSQL type | NULL | PK / FK | อ้างอิง | คำอธิบายภาษาไทย |
|---|---|---|---|---|---|
| `id` | `uuid` | ไม่ได้ | PK | — | รหัสหลักภายในของแถวข้อมูล ไม่เปลี่ยนตลอดอายุรายการ; Primary Key ชนิด UUID ห้ามซ้ำหรือเป็น NULL |
| `company_id` | `uuid` | ไม่ได้ | FK | `org.companies.id` | รหัสอ้างอิงบริษัทเจ้าของข้อมูล ไปยัง org.companies.id (บทบาทฟิลด์ company_id) |
| `user_id` | `uuid` | ไม่ได้ | FK | `security.users.id` | รหัสอ้างอิง หนึ่งตัวตนผู้ใช้กลาง ไปยัง security.users.id (บทบาทฟิลด์ user_id) |
| `active` | `boolean` | ไม่ได้ | — | — | สถานะเปิดใช้งาน |
| `joined_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่เริ่มเป็นสมาชิกบริษัท; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `created_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่สร้างแถวข้อมูลในระบบ; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `updated_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่แก้ไขแถวข้อมูลล่าสุด ต้องอัปเดตทุกช่องทางเขียน; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `version` | `integer` | ไม่ได้ | — | — | เลขรุ่นแถวสำหรับตรวจการแก้ไขพร้อมกัน |

**Keys / Index:** U(company_id,user_id)

**กฎเฉพาะ:** ไม่ให้ company admin ยึด global user ที่อยู่บริษัทอื่นผ่านการเปลี่ยน email/password

## `security.access_scopes`

**เฟส:** F · **หนึ่งแถวคือ:** หนึ่งขอบเขตสิทธิ์ · **ประเภท:** mutable

**คำอธิบาย:** ตารางเก็บข้อมูล หนึ่งขอบเขตสิทธิ์; หนึ่งแถวมีความหมายตามนี้และอยู่ในเฟส F

| คอลัมน์ | PostgreSQL type | NULL | PK / FK | อ้างอิง | คำอธิบายภาษาไทย |
|---|---|---|---|---|---|
| `id` | `uuid` | ไม่ได้ | PK | — | รหัสหลักภายในของแถวข้อมูล ไม่เปลี่ยนตลอดอายุรายการ; Primary Key ชนิด UUID ห้ามซ้ำหรือเป็น NULL |
| `company_id` | `uuid` | ไม่ได้ | FK | `org.companies.id` | รหัสอ้างอิงบริษัทเจ้าของข้อมูล ไปยัง org.companies.id (บทบาทฟิลด์ company_id) |
| `kind` | `text` | ไม่ได้ | — | — | ชนิดรายการตามค่าที่อนุญาตของตาราง |
| `branch_id` | `uuid` | ได้ | FK | `org.branches.id` | รหัสอ้างอิงสาขาเจ้าของรายการ ไปยัง org.branches.id (บทบาทฟิลด์ branch_id) |
| `warehouse_id` | `uuid` | ได้ | FK | `org.warehouses.id` | รหัสอ้างอิงคลังที่เกี่ยวข้อง ไปยัง org.warehouses.id (บทบาทฟิลด์ warehouse_id) |
| `created_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่สร้างแถวข้อมูลในระบบ; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `updated_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่แก้ไขแถวข้อมูลล่าสุด ต้องอัปเดตทุกช่องทางเขียน; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `version` | `integer` | ไม่ได้ | — | — | เลขรุ่นแถวสำหรับตรวจการแก้ไขพร้อมกัน |

**Keys / Index:** U NULLS NOT DISTINCT(company_id,kind,branch_id,warehouse_id)

**กฎเฉพาะ:** COMPANY: both null; BRANCH: branch only; WAREHOUSE: branch+warehouse matching

## `security.membership_scopes`

**เฟส:** F · **หนึ่งแถวคือ:** หนึ่งสมาชิกที่เข้าถึง scope · **ประเภท:** mutable

**คำอธิบาย:** ตารางเก็บข้อมูล หนึ่งสมาชิกที่เข้าถึง scope; หนึ่งแถวมีความหมายตามนี้และอยู่ในเฟส F

| คอลัมน์ | PostgreSQL type | NULL | PK / FK | อ้างอิง | คำอธิบายภาษาไทย |
|---|---|---|---|---|---|
| `id` | `uuid` | ไม่ได้ | PK | — | รหัสหลักภายในของแถวข้อมูล ไม่เปลี่ยนตลอดอายุรายการ; Primary Key ชนิด UUID ห้ามซ้ำหรือเป็น NULL |
| `company_id` | `uuid` | ไม่ได้ | FK | `org.companies.id` | รหัสอ้างอิงบริษัทเจ้าของข้อมูล ไปยัง org.companies.id (บทบาทฟิลด์ company_id) |
| `membership_id` | `uuid` | ไม่ได้ | FK | `security.memberships.id` | รหัสอ้างอิง หนึ่งสมาชิกต่อบริษัท ไปยัง security.memberships.id (บทบาทฟิลด์ membership_id) |
| `scope_id` | `uuid` | ไม่ได้ | FK | `security.access_scopes.id` | รหัสอ้างอิง หนึ่งขอบเขตสิทธิ์ ไปยัง security.access_scopes.id (บทบาทฟิลด์ scope_id) |
| `created_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่สร้างแถวข้อมูลในระบบ; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `updated_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่แก้ไขแถวข้อมูลล่าสุด ต้องอัปเดตทุกช่องทางเขียน; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `version` | `integer` | ไม่ได้ | — | — | เลขรุ่นแถวสำหรับตรวจการแก้ไขพร้อมกัน |

**Keys / Index:** U(company_id,membership_id,scope_id)

**กฎเฉพาะ:** ใช้กฎ tenant, FK และ audit กลาง

## `security.roles`

**เฟส:** F · **หนึ่งแถวคือ:** หนึ่งบทบาทภายในบริษัท · **ประเภท:** mutable

**คำอธิบาย:** ตารางเก็บข้อมูล หนึ่งบทบาทภายในบริษัท; หนึ่งแถวมีความหมายตามนี้และอยู่ในเฟส F

| คอลัมน์ | PostgreSQL type | NULL | PK / FK | อ้างอิง | คำอธิบายภาษาไทย |
|---|---|---|---|---|---|
| `id` | `uuid` | ไม่ได้ | PK | — | รหัสหลักภายในของแถวข้อมูล ไม่เปลี่ยนตลอดอายุรายการ; Primary Key ชนิด UUID ห้ามซ้ำหรือเป็น NULL |
| `company_id` | `uuid` | ไม่ได้ | FK | `org.companies.id` | รหัสอ้างอิงบริษัทเจ้าของข้อมูล ไปยัง org.companies.id (บทบาทฟิลด์ company_id) |
| `code` | `text` | ไม่ได้ | — | — | รหัสธุรกิจของรายการตามขอบเขต Unique ของตาราง |
| `name` | `text` | ไม่ได้ | — | — | ชื่อรายการสำหรับแสดงผล |
| `system_managed` | `boolean` | ไม่ได้ | — | — | ระบุว่าเป็นข้อมูลที่ระบบดูแลและจำกัดการแก้ไข |
| `active` | `boolean` | ไม่ได้ | — | — | สถานะเปิดใช้งาน |
| `created_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่สร้างแถวข้อมูลในระบบ; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `updated_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่แก้ไขแถวข้อมูลล่าสุด ต้องอัปเดตทุกช่องทางเขียน; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `version` | `integer` | ไม่ได้ | — | — | เลขรุ่นแถวสำหรับตรวจการแก้ไขพร้อมกัน |

**Keys / Index:** U(company_id,code)

**กฎเฉพาะ:** ใช้กฎ tenant, FK และ audit กลาง

## `security.permissions`

**เฟส:** F · **หนึ่งแถวคือ:** หนึ่ง permission code กลาง · **ประเภท:** mutable

**คำอธิบาย:** ตารางเก็บข้อมูล หนึ่ง permission code กลาง; หนึ่งแถวมีความหมายตามนี้และอยู่ในเฟส F

| คอลัมน์ | PostgreSQL type | NULL | PK / FK | อ้างอิง | คำอธิบายภาษาไทย |
|---|---|---|---|---|---|
| `id` | `uuid` | ไม่ได้ | PK | — | รหัสหลักภายในของแถวข้อมูล ไม่เปลี่ยนตลอดอายุรายการ; Primary Key ชนิด UUID ห้ามซ้ำหรือเป็น NULL |
| `code` | `text` | ไม่ได้ | — | — | รหัสธุรกิจของรายการตามขอบเขต Unique ของตาราง |
| `module` | `text` | ไม่ได้ | — | — | โมดูลเจ้าของสิทธิ์หรือการตั้งค่า |
| `description` | `text` | ไม่ได้ | — | — | คำอธิบายรายละเอียด |
| `created_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่สร้างแถวข้อมูลในระบบ; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `updated_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่แก้ไขแถวข้อมูลล่าสุด ต้องอัปเดตทุกช่องทางเขียน; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `version` | `integer` | ไม่ได้ | — | — | เลขรุ่นแถวสำหรับตรวจการแก้ไขพร้อมกัน |

**Keys / Index:** U(code)

**กฎเฉพาะ:** global catalog ไม่ใช่สิทธิ์ข้าม tenant

## `security.role_permissions`

**เฟส:** F · **หนึ่งแถวคือ:** หนึ่ง permission ของ role · **ประเภท:** mutable

**คำอธิบาย:** ตารางเก็บข้อมูล หนึ่ง permission ของ role; หนึ่งแถวมีความหมายตามนี้และอยู่ในเฟส F

| คอลัมน์ | PostgreSQL type | NULL | PK / FK | อ้างอิง | คำอธิบายภาษาไทย |
|---|---|---|---|---|---|
| `id` | `uuid` | ไม่ได้ | PK | — | รหัสหลักภายในของแถวข้อมูล ไม่เปลี่ยนตลอดอายุรายการ; Primary Key ชนิด UUID ห้ามซ้ำหรือเป็น NULL |
| `company_id` | `uuid` | ไม่ได้ | FK | `org.companies.id` | รหัสอ้างอิงบริษัทเจ้าของข้อมูล ไปยัง org.companies.id (บทบาทฟิลด์ company_id) |
| `role_id` | `uuid` | ไม่ได้ | FK | `security.roles.id` | รหัสอ้างอิง หนึ่งบทบาทภายในบริษัท ไปยัง security.roles.id (บทบาทฟิลด์ role_id) |
| `permission_id` | `uuid` | ไม่ได้ | FK | `security.permissions.id` | รหัสอ้างอิง หนึ่ง permission code กลาง ไปยัง security.permissions.id (บทบาทฟิลด์ permission_id) |
| `created_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่สร้างแถวข้อมูลในระบบ; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `updated_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่แก้ไขแถวข้อมูลล่าสุด ต้องอัปเดตทุกช่องทางเขียน; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `version` | `integer` | ไม่ได้ | — | — | เลขรุ่นแถวสำหรับตรวจการแก้ไขพร้อมกัน |

**Keys / Index:** U(company_id,role_id,permission_id)

**กฎเฉพาะ:** ใช้กฎ tenant, FK และ audit กลาง

## `security.role_assignments`

**เฟส:** F · **หนึ่งแถวคือ:** หนึ่ง role ที่ผูก membership+scope · **ประเภท:** mutable

**คำอธิบาย:** ตารางเก็บข้อมูล หนึ่ง role ที่ผูก membership+scope; หนึ่งแถวมีความหมายตามนี้และอยู่ในเฟส F

| คอลัมน์ | PostgreSQL type | NULL | PK / FK | อ้างอิง | คำอธิบายภาษาไทย |
|---|---|---|---|---|---|
| `id` | `uuid` | ไม่ได้ | PK | — | รหัสหลักภายในของแถวข้อมูล ไม่เปลี่ยนตลอดอายุรายการ; Primary Key ชนิด UUID ห้ามซ้ำหรือเป็น NULL |
| `company_id` | `uuid` | ไม่ได้ | FK | `org.companies.id` | รหัสอ้างอิงบริษัทเจ้าของข้อมูล ไปยัง org.companies.id (บทบาทฟิลด์ company_id) |
| `membership_scope_id` | `uuid` | ไม่ได้ | FK | `security.membership_scopes.id` | รหัสอ้างอิง หนึ่งสมาชิกที่เข้าถึง scope ไปยัง security.membership_scopes.id (บทบาทฟิลด์ membership_scope_id) |
| `role_id` | `uuid` | ไม่ได้ | FK | `security.roles.id` | รหัสอ้างอิง หนึ่งบทบาทภายในบริษัท ไปยัง security.roles.id (บทบาทฟิลด์ role_id) |
| `active` | `boolean` | ไม่ได้ | — | — | สถานะเปิดใช้งาน |
| `created_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่สร้างแถวข้อมูลในระบบ; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `updated_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่แก้ไขแถวข้อมูลล่าสุด ต้องอัปเดตทุกช่องทางเขียน; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `version` | `integer` | ไม่ได้ | — | — | เลขรุ่นแถวสำหรับตรวจการแก้ไขพร้อมกัน |

**Keys / Index:** U(company_id,membership_scope_id,role_id)

**กฎเฉพาะ:** ไม่มี tenant-wide superuser โดยปริยาย; คง admin คนสุดท้าย

## `security.sessions`

**เฟส:** F · **หนึ่งแถวคือ:** หนึ่งอุปกรณ์/session ของ user · **ประเภท:** mutable

**คำอธิบาย:** ตารางเก็บข้อมูล หนึ่งอุปกรณ์/session ของ user; หนึ่งแถวมีความหมายตามนี้และอยู่ในเฟส F

| คอลัมน์ | PostgreSQL type | NULL | PK / FK | อ้างอิง | คำอธิบายภาษาไทย |
|---|---|---|---|---|---|
| `id` | `uuid` | ไม่ได้ | PK | — | รหัสหลักภายในของแถวข้อมูล ไม่เปลี่ยนตลอดอายุรายการ; Primary Key ชนิด UUID ห้ามซ้ำหรือเป็น NULL |
| `user_id` | `uuid` | ไม่ได้ | FK | `security.users.id` | รหัสอ้างอิง หนึ่งตัวตนผู้ใช้กลาง ไปยัง security.users.id (บทบาทฟิลด์ user_id) |
| `family_id` | `uuid` | ไม่ได้ | — | — | รหัสกลุ่มโทเค็นสำหรับติดตามการหมุนเวียนและเพิกถอน |
| `expires_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่สิทธิ์ ข้อมูล หรือสินค้าหมดอายุตามบริบทตาราง; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `revoked_at` | `timestamptz` | ได้ | — | — | เวลาที่เพิกถอนสิทธิ์หรือโทเค็น; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `revocation_reason` | `text` | ได้ | — | — | เหตุผลการเพิกถอน |
| `device_label` | `text` | ได้ | — | — | ชื่อที่ใช้แสดงอุปกรณ์ |
| `ip` | `inet` | ได้ | — | — | หมายเลขเครือข่ายของผู้ดำเนินการ |
| `user_agent` | `text` | ได้ | — | — | ข้อมูลโปรแกรมหรืออุปกรณ์ผู้เรียกที่ผ่านการจำกัดความยาว |
| `created_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่สร้างแถวข้อมูลในระบบ; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `updated_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่แก้ไขแถวข้อมูลล่าสุด ต้องอัปเดตทุกช่องทางเขียน; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `version` | `integer` | ไม่ได้ | — | — | เลขรุ่นแถวสำหรับตรวจการแก้ไขพร้อมกัน |

**Keys / Index:** I(user_id,revoked_at); U(family_id)

**กฎเฉพาะ:** session กลาง ตรวจ membership ปัจจุบันทุกบริษัท

## `security.refresh_tokens`

**เฟส:** F · **หนึ่งแถวคือ:** หนึ่งรุ่น token ใน session · **ประเภท:** mutable

**คำอธิบาย:** ตารางเก็บข้อมูล หนึ่งรุ่น token ใน session; หนึ่งแถวมีความหมายตามนี้และอยู่ในเฟส F

| คอลัมน์ | PostgreSQL type | NULL | PK / FK | อ้างอิง | คำอธิบายภาษาไทย |
|---|---|---|---|---|---|
| `id` | `uuid` | ไม่ได้ | PK | — | รหัสหลักภายในของแถวข้อมูล ไม่เปลี่ยนตลอดอายุรายการ; Primary Key ชนิด UUID ห้ามซ้ำหรือเป็น NULL |
| `session_id` | `uuid` | ไม่ได้ | FK | `security.sessions.id` | รหัสอ้างอิง หนึ่งอุปกรณ์/session ของ user ไปยัง security.sessions.id (บทบาทฟิลด์ session_id) |
| `jti` | `uuid` | ไม่ได้ | — | — | รหัสประจำโทเค็นสำหรับติดตามและเพิกถอน |
| `token_hash` | `text` | ไม่ได้ | — | — | ค่าแฮชโทเค็น ห้ามเก็บ plaintext หรือเผยผ่าน API |
| `expires_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่สิทธิ์ ข้อมูล หรือสินค้าหมดอายุตามบริบทตาราง; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `consumed_at` | `timestamptz` | ได้ | — | — | เวลาที่บันทึกการใช้จริง; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `revoked_at` | `timestamptz` | ได้ | — | — | เวลาที่เพิกถอนสิทธิ์หรือโทเค็น; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `replaced_by_id` | `uuid` | ได้ | FK | `security.refresh_tokens.id` | รหัสอ้างอิง หนึ่งรุ่น token ใน session ไปยัง security.refresh_tokens.id (บทบาทฟิลด์ replaced_by_id) |
| `created_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่สร้างแถวข้อมูลในระบบ; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `updated_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่แก้ไขแถวข้อมูลล่าสุด ต้องอัปเดตทุกช่องทางเขียน; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `version` | `integer` | ไม่ได้ | — | — | เลขรุ่นแถวสำหรับตรวจการแก้ไขพร้อมกัน |

**Keys / Index:** U(jti); U(token_hash); I(session_id)

**กฎเฉพาะ:** rotation atomic และ revoke family เมื่อ reuse; ไม่มี plaintext

## `platform.documents`

**เฟส:** P · **หนึ่งแถวคือ:** หนึ่งเอกสารธุรกิจที่เป็น FK กลาง · **ประเภท:** mutable

**คำอธิบาย:** ตารางเก็บข้อมูล หนึ่งเอกสารธุรกิจที่เป็น FK กลาง; หนึ่งแถวมีความหมายตามนี้และอยู่ในเฟส P

| คอลัมน์ | PostgreSQL type | NULL | PK / FK | อ้างอิง | คำอธิบายภาษาไทย |
|---|---|---|---|---|---|
| `id` | `uuid` | ไม่ได้ | PK | — | รหัสหลักภายในของแถวข้อมูล ไม่เปลี่ยนตลอดอายุรายการ; Primary Key ชนิด UUID ห้ามซ้ำหรือเป็น NULL |
| `company_id` | `uuid` | ไม่ได้ | FK | `org.companies.id` | รหัสอ้างอิงบริษัทเจ้าของข้อมูล ไปยัง org.companies.id (บทบาทฟิลด์ company_id) |
| `branch_id` | `uuid` | ไม่ได้ | FK | `org.branches.id` | รหัสอ้างอิงสาขาเจ้าของรายการ ไปยัง org.branches.id (บทบาทฟิลด์ branch_id) |
| `kind` | `text` | ไม่ได้ | — | — | ชนิดรายการตามค่าที่อนุญาตของตาราง |
| `document_no` | `text` | ได้ | — | — | เลขที่เอกสารธุรกิจ |
| `status` | `text` | ไม่ได้ | — | — | สถานะรายการตาม state machine ของตาราง |
| `effective_at` | `timestamptz` | ได้ | — | — | เวลาที่รายการมีผลทางธุรกิจ แยกจากเวลาบันทึก; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `created_by` | `uuid` | ไม่ได้ | FK | `security.users.id` | รหัสอ้างอิงผู้สร้าง ไปยัง security.users.id (บทบาทฟิลด์ created_by) |
| `confirmed_by` | `uuid` | ได้ | FK | `security.users.id` | รหัสอ้างอิงผู้ยืนยัน ไปยัง security.users.id (บทบาทฟิลด์ confirmed_by) |
| `confirmed_at` | `timestamptz` | ได้ | — | — | เวลาที่ผู้มีสิทธิ์ยืนยันรายการ; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `reverses_document_id` | `uuid` | ได้ | FK | `platform.documents.id` | รหัสอ้างอิง หนึ่งเอกสารธุรกิจที่เป็น FK กลาง ไปยัง platform.documents.id (บทบาทฟิลด์ reverses_document_id) |
| `created_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่สร้างแถวข้อมูลในระบบ; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `updated_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่แก้ไขแถวข้อมูลล่าสุด ต้องอัปเดตทุกช่องทางเขียน; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `version` | `integer` | ไม่ได้ | — | — | เลขรุ่นแถวสำหรับตรวจการแก้ไขพร้อมกัน |

**Keys / Index:** U(company_id,branch_id,kind,document_no); I(company_id,kind,status,created_at)

**กฎเฉพาะ:** typed header exactly one ตาม kind; status ต้อง transition ผ่าน service; ไม่ใช้ทะเบียนนี้แทนตารางธุรกิจ

## `platform.document_lines`

**เฟส:** P · **หนึ่งแถวคือ:** หนึ่ง line identity ในเอกสาร · **ประเภท:** mutable

**คำอธิบาย:** ตารางเก็บข้อมูล หนึ่ง line identity ในเอกสาร; หนึ่งแถวมีความหมายตามนี้และอยู่ในเฟส P

| คอลัมน์ | PostgreSQL type | NULL | PK / FK | อ้างอิง | คำอธิบายภาษาไทย |
|---|---|---|---|---|---|
| `id` | `uuid` | ไม่ได้ | PK | — | รหัสหลักภายในของแถวข้อมูล ไม่เปลี่ยนตลอดอายุรายการ; Primary Key ชนิด UUID ห้ามซ้ำหรือเป็น NULL |
| `company_id` | `uuid` | ไม่ได้ | FK | `org.companies.id` | รหัสอ้างอิงบริษัทเจ้าของข้อมูล ไปยัง org.companies.id (บทบาทฟิลด์ company_id) |
| `document_id` | `uuid` | ไม่ได้ | FK | `platform.documents.id` | รหัสอ้างอิง หนึ่งเอกสารธุรกิจที่เป็น FK กลาง ไปยัง platform.documents.id (บทบาทฟิลด์ document_id) |
| `line_no` | `integer` | ไม่ได้ | — | — | ลำดับรายการภายในเอกสาร |
| `kind` | `text` | ไม่ได้ | — | — | ชนิดรายการตามค่าที่อนุญาตของตาราง |
| `created_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่สร้างแถวข้อมูลในระบบ; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `updated_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่แก้ไขแถวข้อมูลล่าสุด ต้องอัปเดตทุกช่องทางเขียน; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `version` | `integer` | ไม่ได้ | — | — | เลขรุ่นแถวสำหรับตรวจการแก้ไขพร้อมกัน |

**Keys / Index:** U(company_id,document_id,line_no)

**กฎเฉพาะ:** มี typed child exactly one ตอน document สมบูรณ์; ID ไม่เปลี่ยนเมื่อ PO revision

## `platform.number_sequences`

**เฟส:** P · **หนึ่งแถวคือ:** หนึ่งเลข running ตามชนิด/สาขา/ปี · **ประเภท:** mutable

**คำอธิบาย:** ตารางเก็บข้อมูล หนึ่งเลข running ตามชนิด/สาขา/ปี; หนึ่งแถวมีความหมายตามนี้และอยู่ในเฟส P

| คอลัมน์ | PostgreSQL type | NULL | PK / FK | อ้างอิง | คำอธิบายภาษาไทย |
|---|---|---|---|---|---|
| `id` | `uuid` | ไม่ได้ | PK | — | รหัสหลักภายในของแถวข้อมูล ไม่เปลี่ยนตลอดอายุรายการ; Primary Key ชนิด UUID ห้ามซ้ำหรือเป็น NULL |
| `company_id` | `uuid` | ไม่ได้ | FK | `org.companies.id` | รหัสอ้างอิงบริษัทเจ้าของข้อมูล ไปยัง org.companies.id (บทบาทฟิลด์ company_id) |
| `branch_id` | `uuid` | ไม่ได้ | FK | `org.branches.id` | รหัสอ้างอิงสาขาเจ้าของรายการ ไปยัง org.branches.id (บทบาทฟิลด์ branch_id) |
| `kind` | `text` | ไม่ได้ | — | — | ชนิดรายการตามค่าที่อนุญาตของตาราง |
| `fiscal_year` | `integer` | ไม่ได้ | — | — | ปีที่ใช้แยกชุดเลขเอกสาร ต้องระบุระบบปีตามนโยบายเลขเอกสาร |
| `prefix` | `text` | ไม่ได้ | — | — | ข้อความนำหน้าเลขเอกสาร |
| `next_value` | `bigint` | ไม่ได้ | — | — | เลขลำดับถัดไปของชุดเลขเอกสาร |
| `created_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่สร้างแถวข้อมูลในระบบ; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `updated_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่แก้ไขแถวข้อมูลล่าสุด ต้องอัปเดตทุกช่องทางเขียน; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `version` | `integer` | ไม่ได้ | — | — | เลขรุ่นแถวสำหรับตรวจการแก้ไขพร้อมกัน |

**Keys / Index:** U(company_id,branch_id,kind,fiscal_year)

**กฎเฉพาะ:** atomic UPDATE RETURNING; เลขยกเลิกไม่ reuse; gaps ยอมรับได้

## `platform.files`

**เฟส:** F · **หนึ่งแถวคือ:** หนึ่ง object ส่วนตัว · **ประเภท:** mutable

**คำอธิบาย:** ตารางเก็บข้อมูล หนึ่ง object ส่วนตัว; หนึ่งแถวมีความหมายตามนี้และอยู่ในเฟส F

| คอลัมน์ | PostgreSQL type | NULL | PK / FK | อ้างอิง | คำอธิบายภาษาไทย |
|---|---|---|---|---|---|
| `id` | `uuid` | ไม่ได้ | PK | — | รหัสหลักภายในของแถวข้อมูล ไม่เปลี่ยนตลอดอายุรายการ; Primary Key ชนิด UUID ห้ามซ้ำหรือเป็น NULL |
| `company_id` | `uuid` | ไม่ได้ | FK | `org.companies.id` | รหัสอ้างอิงบริษัทเจ้าของข้อมูล ไปยัง org.companies.id (บทบาทฟิลด์ company_id) |
| `object_key` | `text` | ไม่ได้ | — | — | ตำแหน่งอ้างอิงไฟล์ใน object storage ไม่ใช่ public URL |
| `original_name` | `text` | ไม่ได้ | — | — | ชื่อไฟล์ต้นฉบับ |
| `mime_type` | `text` | ไม่ได้ | — | — | ชนิดเนื้อหาไฟล์ |
| `size_bytes` | `bigint` | ไม่ได้ | — | — | ขนาดไฟล์ หน่วยไบต์ |
| `sha256` | `text` | ไม่ได้ | — | — | ค่าแฮช SHA-256 สำหรับตรวจไฟล์ |
| `scan_status` | `text` | ไม่ได้ | — | — | สถานะตรวจความปลอดภัยไฟล์ |
| `uploaded_by` | `uuid` | ไม่ได้ | FK | `security.users.id` | รหัสอ้างอิง หนึ่งตัวตนผู้ใช้กลาง ไปยัง security.users.id (บทบาทฟิลด์ uploaded_by) |
| `retention_until` | `timestamptz` | ได้ | — | — | เวลาสิ้นสุดระยะเก็บรักษาตามนโยบาย; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `deleted_at` | `timestamptz` | ได้ | — | — | เวลาลบแบบเก็บประวัติ ค่า NULL หมายถึงยังไม่ลบ; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `created_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่สร้างแถวข้อมูลในระบบ; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `updated_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่แก้ไขแถวข้อมูลล่าสุด ต้องอัปเดตทุกช่องทางเขียน; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `version` | `integer` | ไม่ได้ | — | — | เลขรุ่นแถวสำหรับตรวจการแก้ไขพร้อมกัน |

**Keys / Index:** U(company_id,object_key); I(company_id,created_at)

**กฎเฉพาะ:** ไม่เก็บ signed URL เป็น canonical; FK references ก่อนลบ; scan clean ก่อนใช้งาน

## `platform.document_files`

**เฟส:** P · **หนึ่งแถวคือ:** หนึ่งไฟล์ประกอบเอกสาร · **ประเภท:** mutable

**คำอธิบาย:** ตารางเก็บข้อมูล หนึ่งไฟล์ประกอบเอกสาร; หนึ่งแถวมีความหมายตามนี้และอยู่ในเฟส P

| คอลัมน์ | PostgreSQL type | NULL | PK / FK | อ้างอิง | คำอธิบายภาษาไทย |
|---|---|---|---|---|---|
| `id` | `uuid` | ไม่ได้ | PK | — | รหัสหลักภายในของแถวข้อมูล ไม่เปลี่ยนตลอดอายุรายการ; Primary Key ชนิด UUID ห้ามซ้ำหรือเป็น NULL |
| `company_id` | `uuid` | ไม่ได้ | FK | `org.companies.id` | รหัสอ้างอิงบริษัทเจ้าของข้อมูล ไปยัง org.companies.id (บทบาทฟิลด์ company_id) |
| `document_id` | `uuid` | ไม่ได้ | FK | `platform.documents.id` | รหัสอ้างอิง หนึ่งเอกสารธุรกิจที่เป็น FK กลาง ไปยัง platform.documents.id (บทบาทฟิลด์ document_id) |
| `line_id` | `uuid` | ได้ | FK | `platform.document_lines.id` | รหัสอ้างอิง หนึ่ง line identity ในเอกสาร ไปยัง platform.document_lines.id (บทบาทฟิลด์ line_id) |
| `file_id` | `uuid` | ไม่ได้ | FK | `platform.files.id` | รหัสอ้างอิง หนึ่ง object ส่วนตัว ไปยัง platform.files.id (บทบาทฟิลด์ file_id) |
| `purpose` | `text` | ไม่ได้ | — | — | วัตถุประสงค์ของรายการ |
| `created_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่สร้างแถวข้อมูลในระบบ; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `updated_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่แก้ไขแถวข้อมูลล่าสุด ต้องอัปเดตทุกช่องทางเขียน; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `version` | `integer` | ไม่ได้ | — | — | เลขรุ่นแถวสำหรับตรวจการแก้ไขพร้อมกัน |

**Keys / Index:** U NULLS NOT DISTINCT(company_id,document_id,line_id,file_id,purpose)

**กฎเฉพาะ:** line ต้องอยู่ document เดียวกัน

## `platform.approval_policies`

**เฟส:** P · **หนึ่งแถวคือ:** หนึ่งรุ่นกฎอนุมัติ · **ประเภท:** mutable

**คำอธิบาย:** ตารางเก็บข้อมูล หนึ่งรุ่นกฎอนุมัติ; หนึ่งแถวมีความหมายตามนี้และอยู่ในเฟส P

| คอลัมน์ | PostgreSQL type | NULL | PK / FK | อ้างอิง | คำอธิบายภาษาไทย |
|---|---|---|---|---|---|
| `id` | `uuid` | ไม่ได้ | PK | — | รหัสหลักภายในของแถวข้อมูล ไม่เปลี่ยนตลอดอายุรายการ; Primary Key ชนิด UUID ห้ามซ้ำหรือเป็น NULL |
| `company_id` | `uuid` | ไม่ได้ | FK | `org.companies.id` | รหัสอ้างอิงบริษัทเจ้าของข้อมูล ไปยัง org.companies.id (บทบาทฟิลด์ company_id) |
| `code` | `text` | ไม่ได้ | — | — | รหัสธุรกิจของรายการตามขอบเขต Unique ของตาราง |
| `revision` | `integer` | ไม่ได้ | — | — | หมายเลขฉบับของข้อมูล |
| `scope_id` | `uuid` | ไม่ได้ | FK | `security.access_scopes.id` | รหัสอ้างอิง หนึ่งขอบเขตสิทธิ์ ไปยัง security.access_scopes.id (บทบาทฟิลด์ scope_id) |
| `document_kind` | `text` | ไม่ได้ | — | — | ชนิดเอกสารธุรกิจ |
| `min_amount` | `numeric(20,2)` | ได้ | — | — | วงเงินต่ำสุดที่กฎนี้ครอบคลุม; เลขทศนิยมแม่นยำ ส่ง API เป็น string ไม่คำนวณด้วย float |
| `max_amount` | `numeric(20,2)` | ได้ | — | — | วงเงินสูงสุดที่กฎนี้ครอบคลุม; เลขทศนิยมแม่นยำ ส่ง API เป็น string ไม่คำนวณด้วย float |
| `currency` | `char(3)` | ไม่ได้ | — | — | รหัสสกุลเงินของรายการ |
| `active` | `boolean` | ไม่ได้ | — | — | สถานะเปิดใช้งาน |
| `maker_checker` | `boolean` | ไม่ได้ | — | — | กำหนดให้ผู้สร้างและผู้อนุมัติเป็นคนละคน |
| `created_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่สร้างแถวข้อมูลในระบบ; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `updated_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่แก้ไขแถวข้อมูลล่าสุด ต้องอัปเดตทุกช่องทางเขียน; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `version` | `integer` | ไม่ได้ | — | — | เลขรุ่นแถวสำหรับตรวจการแก้ไขพร้อมกัน |

**Keys / Index:** U(company_id,code,revision)

**กฎเฉพาะ:** ไม่แก้ policy ที่ถูกใช้งาน; resolve precedence ชัด ไม่รวมกฎโดยเดา

## `platform.approval_policy_steps`

**เฟส:** P · **หนึ่งแถวคือ:** หนึ่งขั้นอนุมัติ · **ประเภท:** mutable

**คำอธิบาย:** ตารางเก็บข้อมูล หนึ่งขั้นอนุมัติ; หนึ่งแถวมีความหมายตามนี้และอยู่ในเฟส P

| คอลัมน์ | PostgreSQL type | NULL | PK / FK | อ้างอิง | คำอธิบายภาษาไทย |
|---|---|---|---|---|---|
| `id` | `uuid` | ไม่ได้ | PK | — | รหัสหลักภายในของแถวข้อมูล ไม่เปลี่ยนตลอดอายุรายการ; Primary Key ชนิด UUID ห้ามซ้ำหรือเป็น NULL |
| `company_id` | `uuid` | ไม่ได้ | FK | `org.companies.id` | รหัสอ้างอิงบริษัทเจ้าของข้อมูล ไปยัง org.companies.id (บทบาทฟิลด์ company_id) |
| `policy_id` | `uuid` | ไม่ได้ | FK | `platform.approval_policies.id` | รหัสอ้างอิง หนึ่งรุ่นกฎอนุมัติ ไปยัง platform.approval_policies.id (บทบาทฟิลด์ policy_id) |
| `step_no` | `integer` | ไม่ได้ | — | — | ลำดับขั้นตอนอนุมัติ |
| `role_id` | `uuid` | ไม่ได้ | FK | `security.roles.id` | รหัสอ้างอิง หนึ่งบทบาทภายในบริษัท ไปยัง security.roles.id (บทบาทฟิลด์ role_id) |
| `required_count` | `integer` | ไม่ได้ | — | — | จำนวนผู้อนุมัติที่ต้องครบตามขั้นตอน |
| `created_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่สร้างแถวข้อมูลในระบบ; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `updated_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่แก้ไขแถวข้อมูลล่าสุด ต้องอัปเดตทุกช่องทางเขียน; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `version` | `integer` | ไม่ได้ | — | — | เลขรุ่นแถวสำหรับตรวจการแก้ไขพร้อมกัน |

**Keys / Index:** U(company_id,policy_id,step_no)

**กฎเฉพาะ:** quorum >0

## `platform.approval_requests`

**เฟส:** P · **หนึ่งแถวคือ:** หนึ่งคำขออนุมัติ snapshot · **ประเภท:** mutable

**คำอธิบาย:** ตารางเก็บข้อมูล หนึ่งคำขออนุมัติ snapshot; หนึ่งแถวมีความหมายตามนี้และอยู่ในเฟส P

| คอลัมน์ | PostgreSQL type | NULL | PK / FK | อ้างอิง | คำอธิบายภาษาไทย |
|---|---|---|---|---|---|
| `id` | `uuid` | ไม่ได้ | PK | — | รหัสหลักภายในของแถวข้อมูล ไม่เปลี่ยนตลอดอายุรายการ; Primary Key ชนิด UUID ห้ามซ้ำหรือเป็น NULL |
| `company_id` | `uuid` | ไม่ได้ | FK | `org.companies.id` | รหัสอ้างอิงบริษัทเจ้าของข้อมูล ไปยัง org.companies.id (บทบาทฟิลด์ company_id) |
| `document_id` | `uuid` | ไม่ได้ | FK | `platform.documents.id` | รหัสอ้างอิง หนึ่งเอกสารธุรกิจที่เป็น FK กลาง ไปยัง platform.documents.id (บทบาทฟิลด์ document_id) |
| `subject_revision` | `integer` | ไม่ได้ | — | — | ฉบับรายการที่ส่งอนุมัติ |
| `policy_id` | `uuid` | ไม่ได้ | FK | `platform.approval_policies.id` | รหัสอ้างอิง หนึ่งรุ่นกฎอนุมัติ ไปยัง platform.approval_policies.id (บทบาทฟิลด์ policy_id) |
| `policy_snapshot` | `jsonb` | ไม่ได้ | — | — | สำเนานโยบายที่ใช้ตัดสินรายการ ณ ขณะนั้น; ต้องตรวจ schema และจำกัดข้อมูลตามสิทธิ์ |
| `subject_hash` | `text` | ไม่ได้ | — | — | ค่าแฮชเนื้อหาที่ส่งอนุมัติ |
| `requested_by` | `uuid` | ไม่ได้ | FK | `security.users.id` | รหัสอ้างอิงผู้ร้องขอ ไปยัง security.users.id (บทบาทฟิลด์ requested_by) |
| `status` | `text` | ไม่ได้ | — | — | สถานะรายการตาม state machine ของตาราง |
| `created_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่สร้างแถวข้อมูลในระบบ; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `updated_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่แก้ไขแถวข้อมูลล่าสุด ต้องอัปเดตทุกช่องทางเขียน; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `version` | `integer` | ไม่ได้ | — | — | เลขรุ่นแถวสำหรับตรวจการแก้ไขพร้อมกัน |

**Keys / Index:** I(company_id,document_id,status)

**กฎเฉพาะ:** ห้ามอนุมัติรุ่นคนละ hash; company/branch/scope ต้องตรวจทุก action

## `platform.approval_decisions`

**เฟส:** P · **หนึ่งแถวคือ:** หนึ่งผลตัดสินใจต่อคน/ขั้น · **ประเภท:** append

**คำอธิบาย:** ตารางเก็บข้อมูล หนึ่งผลตัดสินใจต่อคน/ขั้น; หนึ่งแถวมีความหมายตามนี้และอยู่ในเฟส P

| คอลัมน์ | PostgreSQL type | NULL | PK / FK | อ้างอิง | คำอธิบายภาษาไทย |
|---|---|---|---|---|---|
| `id` | `uuid` | ไม่ได้ | PK | — | รหัสหลักภายในของแถวข้อมูล ไม่เปลี่ยนตลอดอายุรายการ; Primary Key ชนิด UUID ห้ามซ้ำหรือเป็น NULL |
| `company_id` | `uuid` | ไม่ได้ | FK | `org.companies.id` | รหัสอ้างอิงบริษัทเจ้าของข้อมูล ไปยัง org.companies.id (บทบาทฟิลด์ company_id) |
| `request_id` | `uuid` | ไม่ได้ | FK | `platform.approval_requests.id` | รหัสอ้างอิงรหัสติดตามคำขอ API เชื่อม log และ audit ไปยัง platform.approval_requests.id (บทบาทฟิลด์ request_id) |
| `step_no` | `integer` | ไม่ได้ | — | — | ลำดับขั้นตอนอนุมัติ |
| `decided_by` | `uuid` | ไม่ได้ | FK | `security.users.id` | รหัสอ้างอิง หนึ่งตัวตนผู้ใช้กลาง ไปยัง security.users.id (บทบาทฟิลด์ decided_by) |
| `decision` | `text` | ไม่ได้ | — | — | ผลการตัดสินใจตามค่าที่อนุญาต |
| `reason` | `text` | ได้ | — | — | เหตุผลประกอบการดำเนินการ |
| `decided_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่ตัดสินใจอนุมัติหรือปฏิเสธ; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `created_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่สร้างแถวข้อมูลในระบบ; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |

**Keys / Index:** U(company_id,request_id,step_no,decided_by)

**กฎเฉพาะ:** APPROVE/REJECT/RETURN; immutable

## `platform.setting_definitions`

**เฟส:** F · **หนึ่งแถวคือ:** หนึ่งชนิด setting · **ประเภท:** mutable

**คำอธิบาย:** ตารางเก็บข้อมูล หนึ่งชนิด setting; หนึ่งแถวมีความหมายตามนี้และอยู่ในเฟส F

| คอลัมน์ | PostgreSQL type | NULL | PK / FK | อ้างอิง | คำอธิบายภาษาไทย |
|---|---|---|---|---|---|
| `id` | `uuid` | ไม่ได้ | PK | — | รหัสหลักภายในของแถวข้อมูล ไม่เปลี่ยนตลอดอายุรายการ; Primary Key ชนิด UUID ห้ามซ้ำหรือเป็น NULL |
| `key` | `text` | ไม่ได้ | — | — | กุญแจเฉพาะสำหรับระบุรายการตามบริบทตาราง |
| `value_schema` | `jsonb` | ไม่ได้ | — | — | ข้อกำหนดรูปแบบและชนิดค่าคุณลักษณะ; ต้องตรวจ schema และจำกัดข้อมูลตามสิทธิ์ |
| `default_value` | `jsonb` | ไม่ได้ | — | — | ค่าเริ่มต้นของคุณลักษณะ; ต้องตรวจ schema และจำกัดข้อมูลตามสิทธิ์ |
| `allowed_scope_kinds` | `jsonb` | ไม่ได้ | — | — | ชนิดขอบเขตสิทธิ์ที่อนุญาต; ต้องตรวจ schema และจำกัดข้อมูลตามสิทธิ์ |
| `requires_approval` | `boolean` | ไม่ได้ | — | — | กำหนดว่าการดำเนินงานต้องได้รับอนุมัติ |
| `created_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่สร้างแถวข้อมูลในระบบ; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `updated_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่แก้ไขแถวข้อมูลล่าสุด ต้องอัปเดตทุกช่องทางเขียน; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `version` | `integer` | ไม่ได้ | — | — | เลขรุ่นแถวสำหรับตรวจการแก้ไขพร้อมกัน |

**Keys / Index:** U(key)

**กฎเฉพาะ:** versioned config schema ไม่ใช่ arbitrary executable JSON

## `platform.setting_versions`

**เฟส:** P · **หนึ่งแถวคือ:** หนึ่งรุ่นค่าที่ scope · **ประเภท:** mutable

**คำอธิบาย:** ตารางเก็บข้อมูล หนึ่งรุ่นค่าที่ scope; หนึ่งแถวมีความหมายตามนี้และอยู่ในเฟส P

| คอลัมน์ | PostgreSQL type | NULL | PK / FK | อ้างอิง | คำอธิบายภาษาไทย |
|---|---|---|---|---|---|
| `id` | `uuid` | ไม่ได้ | PK | — | รหัสหลักภายในของแถวข้อมูล ไม่เปลี่ยนตลอดอายุรายการ; Primary Key ชนิด UUID ห้ามซ้ำหรือเป็น NULL |
| `company_id` | `uuid` | ไม่ได้ | FK | `org.companies.id` | รหัสอ้างอิงบริษัทเจ้าของข้อมูล ไปยัง org.companies.id (บทบาทฟิลด์ company_id) |
| `definition_id` | `uuid` | ไม่ได้ | FK | `platform.setting_definitions.id` | รหัสอ้างอิง หนึ่งชนิด setting ไปยัง platform.setting_definitions.id (บทบาทฟิลด์ definition_id) |
| `scope_id` | `uuid` | ไม่ได้ | FK | `security.access_scopes.id` | รหัสอ้างอิง หนึ่งขอบเขตสิทธิ์ ไปยัง security.access_scopes.id (บทบาทฟิลด์ scope_id) |
| `revision` | `integer` | ไม่ได้ | — | — | หมายเลขฉบับของข้อมูล |
| `value` | `jsonb` | ไม่ได้ | — | — | มูลค่าหรือค่าข้อมูลตามชนิดและบริบทของตาราง; ต้องตรวจ schema และจำกัดข้อมูลตามสิทธิ์ |
| `valid_from` | `timestamptz` | ไม่ได้ | — | — | วันเวลาเริ่มมีผลของข้อมูล; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `valid_to` | `timestamptz` | ได้ | — | — | วันเวลาสิ้นสุดการมีผลของข้อมูล; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `approval_document_id` | `uuid` | ได้ | FK | `platform.documents.id` | รหัสอ้างอิง หนึ่งเอกสารธุรกิจที่เป็น FK กลาง ไปยัง platform.documents.id (บทบาทฟิลด์ approval_document_id) |
| `changed_by` | `uuid` | ไม่ได้ | FK | `security.users.id` | รหัสอ้างอิง หนึ่งตัวตนผู้ใช้กลาง ไปยัง security.users.id (บทบาทฟิลด์ changed_by) |
| `created_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่สร้างแถวข้อมูลในระบบ; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `updated_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่แก้ไขแถวข้อมูลล่าสุด ต้องอัปเดตทุกช่องทางเขียน; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `version` | `integer` | ไม่ได้ | — | — | เลขรุ่นแถวสำหรับตรวจการแก้ไขพร้อมกัน |

**Keys / Index:** U(company_id,definition_id,scope_id,revision); no overlapping active periods

**กฎเฉพาะ:** warehouse > branch > company > default; transaction snapshot effective settings

## `platform.ui_features`

**เฟส:** F · **หนึ่งแถวคือ:** หนึ่ง menu/action catalog · **ประเภท:** mutable

**คำอธิบาย:** ตารางเก็บข้อมูล หนึ่ง menu/action catalog; หนึ่งแถวมีความหมายตามนี้และอยู่ในเฟส F

| คอลัมน์ | PostgreSQL type | NULL | PK / FK | อ้างอิง | คำอธิบายภาษาไทย |
|---|---|---|---|---|---|
| `id` | `uuid` | ไม่ได้ | PK | — | รหัสหลักภายในของแถวข้อมูล ไม่เปลี่ยนตลอดอายุรายการ; Primary Key ชนิด UUID ห้ามซ้ำหรือเป็น NULL |
| `code` | `text` | ไม่ได้ | — | — | รหัสธุรกิจของรายการตามขอบเขต Unique ของตาราง |
| `parent_id` | `uuid` | ได้ | FK | `platform.ui_features.id` | รหัสอ้างอิง หนึ่ง menu/action catalog ไปยัง platform.ui_features.id (บทบาทฟิลด์ parent_id) |
| `permission_id` | `uuid` | ได้ | FK | `security.permissions.id` | รหัสอ้างอิง หนึ่ง permission code กลาง ไปยัง security.permissions.id (บทบาทฟิลด์ permission_id) |
| `kind` | `text` | ไม่ได้ | — | — | ชนิดรายการตามค่าที่อนุญาตของตาราง |
| `labels` | `jsonb` | ไม่ได้ | — | — | ชื่อแสดงผลหลายภาษา; ต้องตรวจ schema และจำกัดข้อมูลตามสิทธิ์ |
| `created_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่สร้างแถวข้อมูลในระบบ; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `updated_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่แก้ไขแถวข้อมูลล่าสุด ต้องอัปเดตทุกช่องทางเขียน; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `version` | `integer` | ไม่ได้ | — | — | เลขรุ่นแถวสำหรับตรวจการแก้ไขพร้อมกัน |

**Keys / Index:** U(code)

**กฎเฉพาะ:** labels th/lo/zh/my; menu ไม่ใช่ authorization

## `platform.feature_overrides`

**เฟส:** F · **หนึ่งแถวคือ:** หนึ่งการเปิด/ปิด menu/action ที่ scope · **ประเภท:** mutable

**คำอธิบาย:** ตารางเก็บข้อมูล หนึ่งการเปิด/ปิด menu/action ที่ scope; หนึ่งแถวมีความหมายตามนี้และอยู่ในเฟส F

| คอลัมน์ | PostgreSQL type | NULL | PK / FK | อ้างอิง | คำอธิบายภาษาไทย |
|---|---|---|---|---|---|
| `id` | `uuid` | ไม่ได้ | PK | — | รหัสหลักภายในของแถวข้อมูล ไม่เปลี่ยนตลอดอายุรายการ; Primary Key ชนิด UUID ห้ามซ้ำหรือเป็น NULL |
| `company_id` | `uuid` | ไม่ได้ | FK | `org.companies.id` | รหัสอ้างอิงบริษัทเจ้าของข้อมูล ไปยัง org.companies.id (บทบาทฟิลด์ company_id) |
| `feature_id` | `uuid` | ไม่ได้ | FK | `platform.ui_features.id` | รหัสอ้างอิง หนึ่ง menu/action catalog ไปยัง platform.ui_features.id (บทบาทฟิลด์ feature_id) |
| `scope_id` | `uuid` | ไม่ได้ | FK | `security.access_scopes.id` | รหัสอ้างอิง หนึ่งขอบเขตสิทธิ์ ไปยัง security.access_scopes.id (บทบาทฟิลด์ scope_id) |
| `enabled` | `boolean` | ไม่ได้ | — | — | สถานะเปิดใช้คุณสมบัติ |
| `created_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่สร้างแถวข้อมูลในระบบ; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `updated_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่แก้ไขแถวข้อมูลล่าสุด ต้องอัปเดตทุกช่องทางเขียน; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `version` | `integer` | ไม่ได้ | — | — | เลขรุ่นแถวสำหรับตรวจการแก้ไขพร้อมกัน |

**Keys / Index:** U(company_id,feature_id,scope_id)

**กฎเฉพาะ:** permission guard ยังตรวจแม้ menu hidden

## `platform.audit_events`

**เฟส:** F · **หนึ่งแถวคือ:** หนึ่งเหตุการณ์ตรวจสอบ · **ประเภท:** append

**คำอธิบาย:** ตารางเก็บข้อมูล หนึ่งเหตุการณ์ตรวจสอบ; หนึ่งแถวมีความหมายตามนี้และอยู่ในเฟส F

| คอลัมน์ | PostgreSQL type | NULL | PK / FK | อ้างอิง | คำอธิบายภาษาไทย |
|---|---|---|---|---|---|
| `id` | `uuid` | ไม่ได้ | PK | — | รหัสหลักภายในของแถวข้อมูล ไม่เปลี่ยนตลอดอายุรายการ; Primary Key ชนิด UUID ห้ามซ้ำหรือเป็น NULL |
| `company_id` | `uuid` | ไม่ได้ | FK | `org.companies.id` | รหัสอ้างอิงบริษัทเจ้าของข้อมูล ไปยัง org.companies.id (บทบาทฟิลด์ company_id) |
| `actor_id` | `uuid` | ได้ | FK | `security.users.id` | รหัสอ้างอิงผู้ดำเนินการ ไปยัง security.users.id (บทบาทฟิลด์ actor_id) |
| `action` | `text` | ไม่ได้ | — | — | การกระทำที่บันทึก |
| `entity_kind` | `text` | ไม่ได้ | — | — | ชนิดรายการข้อมูลที่เกี่ยวข้อง |
| `entity_id` | `uuid` | ได้ | — | — | รหัสรายการที่เกี่ยวข้อง ใช้คู่กับชนิดรายการและตรวจผ่านตัวแก้การอ้างอิง |
| `document_id` | `uuid` | ได้ | FK | `platform.documents.id` | รหัสอ้างอิง หนึ่งเอกสารธุรกิจที่เป็น FK กลาง ไปยัง platform.documents.id (บทบาทฟิลด์ document_id) |
| `before_data` | `jsonb` | ได้ | — | — | สำเนาข้อมูลก่อนดำเนินการ; ต้องตรวจ schema และจำกัดข้อมูลตามสิทธิ์ |
| `after_data` | `jsonb` | ได้ | — | — | สำเนาข้อมูลหลังดำเนินการ; ต้องตรวจ schema และจำกัดข้อมูลตามสิทธิ์ |
| `reason` | `text` | ได้ | — | — | เหตุผลประกอบการดำเนินการ |
| `request_id` | `uuid` | ไม่ได้ | — | — | รหัสติดตามคำขอ API เชื่อม log และ audit |
| `ip` | `inet` | ได้ | — | — | หมายเลขเครือข่ายของผู้ดำเนินการ |
| `user_agent` | `text` | ได้ | — | — | ข้อมูลโปรแกรมหรืออุปกรณ์ผู้เรียกที่ผ่านการจำกัดความยาว |
| `occurred_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่เหตุการณ์เกิดขึ้นจริง; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `created_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่สร้างแถวข้อมูลในระบบ; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |

**Keys / Index:** I(company_id,occurred_at); I(company_id,document_id,occurred_at)

**กฎเฉพาะ:** entity_id เชิงหลักฐาน ไม่ใช่ FK ธุรกิจ; allowlist PII; เก็บ >=5 ปี ห้าม runtime update/delete

## `security.auth_events`

**เฟส:** F · **หนึ่งแถวคือ:** หนึ่งเหตุการณ์ auth กลาง · **ประเภท:** append

**คำอธิบาย:** ตารางเก็บข้อมูล หนึ่งเหตุการณ์ auth กลาง; หนึ่งแถวมีความหมายตามนี้และอยู่ในเฟส F

| คอลัมน์ | PostgreSQL type | NULL | PK / FK | อ้างอิง | คำอธิบายภาษาไทย |
|---|---|---|---|---|---|
| `id` | `uuid` | ไม่ได้ | PK | — | รหัสหลักภายในของแถวข้อมูล ไม่เปลี่ยนตลอดอายุรายการ; Primary Key ชนิด UUID ห้ามซ้ำหรือเป็น NULL |
| `user_id` | `uuid` | ได้ | FK | `security.users.id` | รหัสอ้างอิง หนึ่งตัวตนผู้ใช้กลาง ไปยัง security.users.id (บทบาทฟิลด์ user_id) |
| `event_type` | `text` | ไม่ได้ | — | — | ประเภทเหตุการณ์ที่กฎนี้รองรับ |
| `request_id` | `uuid` | ไม่ได้ | — | — | รหัสติดตามคำขอ API เชื่อม log และ audit |
| `occurred_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่เหตุการณ์เกิดขึ้นจริง; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `ip` | `inet` | ได้ | — | — | หมายเลขเครือข่ายของผู้ดำเนินการ |
| `reason_code` | `text` | ได้ | — | — | รหัสเหตุผลที่ควบคุมด้วยชุดค่าที่อนุญาต |
| `created_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่สร้างแถวข้อมูลในระบบ; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |

**Keys / Index:** I(user_id,occurred_at)

**กฎเฉพาะ:** แยก audit tenant; ไม่ log password/token/email ที่ login ล้มเหลว

## `catalog.units`

**เฟส:** F · **หนึ่งแถวคือ:** หนึ่งหน่วยในบริษัท · **ประเภท:** mutable

**คำอธิบาย:** ตารางเก็บข้อมูล หนึ่งหน่วยในบริษัท; หนึ่งแถวมีความหมายตามนี้และอยู่ในเฟส F

| คอลัมน์ | PostgreSQL type | NULL | PK / FK | อ้างอิง | คำอธิบายภาษาไทย |
|---|---|---|---|---|---|
| `id` | `uuid` | ไม่ได้ | PK | — | รหัสหลักภายในของแถวข้อมูล ไม่เปลี่ยนตลอดอายุรายการ; Primary Key ชนิด UUID ห้ามซ้ำหรือเป็น NULL |
| `company_id` | `uuid` | ไม่ได้ | FK | `org.companies.id` | รหัสอ้างอิงบริษัทเจ้าของข้อมูล ไปยัง org.companies.id (บทบาทฟิลด์ company_id) |
| `code` | `text` | ไม่ได้ | — | — | รหัสธุรกิจของรายการตามขอบเขต Unique ของตาราง |
| `name` | `text` | ไม่ได้ | — | — | ชื่อรายการสำหรับแสดงผล |
| `dimension` | `text` | ไม่ได้ | — | — | มิติของหน่วย เช่นน้ำหนักหรือจำนวนชิ้น |
| `decimal_places` | `integer` | ไม่ได้ | — | — | จำนวนตำแหน่งทศนิยมที่รองรับ |
| `active` | `boolean` | ไม่ได้ | — | — | สถานะเปิดใช้งาน |
| `created_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่สร้างแถวข้อมูลในระบบ; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `updated_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่แก้ไขแถวข้อมูลล่าสุด ต้องอัปเดตทุกช่องทางเขียน; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `version` | `integer` | ไม่ได้ | — | — | เลขรุ่นแถวสำหรับตรวจการแก้ไขพร้อมกัน |

**Keys / Index:** U(company_id,code)

**กฎเฉพาะ:** COUNT/MASS/VOLUME; dimension immutable หลังมีธุรกรรม

## `catalog.categories`

**เฟส:** F · **หนึ่งแถวคือ:** หนึ่งหมวดสินค้า · **ประเภท:** mutable

**คำอธิบาย:** ตารางเก็บข้อมูล หนึ่งหมวดสินค้า; หนึ่งแถวมีความหมายตามนี้และอยู่ในเฟส F

| คอลัมน์ | PostgreSQL type | NULL | PK / FK | อ้างอิง | คำอธิบายภาษาไทย |
|---|---|---|---|---|---|
| `id` | `uuid` | ไม่ได้ | PK | — | รหัสหลักภายในของแถวข้อมูล ไม่เปลี่ยนตลอดอายุรายการ; Primary Key ชนิด UUID ห้ามซ้ำหรือเป็น NULL |
| `company_id` | `uuid` | ไม่ได้ | FK | `org.companies.id` | รหัสอ้างอิงบริษัทเจ้าของข้อมูล ไปยัง org.companies.id (บทบาทฟิลด์ company_id) |
| `parent_id` | `uuid` | ได้ | FK | `catalog.categories.id` | รหัสอ้างอิง หนึ่งหมวดสินค้า ไปยัง catalog.categories.id (บทบาทฟิลด์ parent_id) |
| `code` | `text` | ไม่ได้ | — | — | รหัสธุรกิจของรายการตามขอบเขต Unique ของตาราง |
| `name` | `text` | ไม่ได้ | — | — | ชื่อรายการสำหรับแสดงผล |
| `active` | `boolean` | ไม่ได้ | — | — | สถานะเปิดใช้งาน |
| `created_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่สร้างแถวข้อมูลในระบบ; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `updated_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่แก้ไขแถวข้อมูลล่าสุด ต้องอัปเดตทุกช่องทางเขียน; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `version` | `integer` | ไม่ได้ | — | — | เลขรุ่นแถวสำหรับตรวจการแก้ไขพร้อมกัน |

**Keys / Index:** U(company_id,code)

**กฎเฉพาะ:** no cycle

## `catalog.products`

**เฟส:** F · **หนึ่งแถวคือ:** หนึ่งสินค้ากลาง · **ประเภท:** mutable

**คำอธิบาย:** ตารางเก็บข้อมูล หนึ่งสินค้ากลาง; หนึ่งแถวมีความหมายตามนี้และอยู่ในเฟส F

| คอลัมน์ | PostgreSQL type | NULL | PK / FK | อ้างอิง | คำอธิบายภาษาไทย |
|---|---|---|---|---|---|
| `id` | `uuid` | ไม่ได้ | PK | — | รหัสหลักภายในของแถวข้อมูล ไม่เปลี่ยนตลอดอายุรายการ; Primary Key ชนิด UUID ห้ามซ้ำหรือเป็น NULL |
| `company_id` | `uuid` | ไม่ได้ | FK | `org.companies.id` | รหัสอ้างอิงบริษัทเจ้าของข้อมูล ไปยัง org.companies.id (บทบาทฟิลด์ company_id) |
| `code` | `text` | ไม่ได้ | — | — | รหัสธุรกิจของรายการตามขอบเขต Unique ของตาราง |
| `barcode` | `text` | ได้ | — | — | รหัสบาร์โค้ด เก็บข้อความเพื่อรักษาเลขศูนย์นำหน้า |
| `name` | `text` | ไม่ได้ | — | — | ชื่อรายการสำหรับแสดงผล |
| `description` | `text` | ได้ | — | — | คำอธิบายรายละเอียด |
| `category_id` | `uuid` | ได้ | FK | `catalog.categories.id` | รหัสอ้างอิง หนึ่งหมวดสินค้า ไปยัง catalog.categories.id (บทบาทฟิลด์ category_id) |
| `stock_unit_id` | `uuid` | ไม่ได้ | FK | `catalog.units.id` | รหัสอ้างอิง หนึ่งหน่วยในบริษัท ไปยัง catalog.units.id (บทบาทฟิลด์ stock_unit_id) |
| `tracking_mode` | `text` | ไม่ได้ | — | — | รูปแบบติดตามสินค้า เช่นล็อตหรือรายบรรจุภัณฑ์ |
| `price` | `numeric(20,6)` | ไม่ได้ | — | — | ราคาต่อหน่วยสินค้า; เลขทศนิยมแม่นยำ ส่ง API เป็น string ไม่คำนวณด้วย float |
| `cost` | `numeric(20,6)` | ได้ | — | — | ต้นทุนต่อหน่วยตามนโยบายสินค้า; เลขทศนิยมแม่นยำ ส่ง API เป็น string ไม่คำนวณด้วย float |
| `active` | `boolean` | ไม่ได้ | — | — | สถานะเปิดใช้งาน |
| `deleted_at` | `timestamptz` | ได้ | — | — | เวลาลบแบบเก็บประวัติ ค่า NULL หมายถึงยังไม่ลบ; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `lot_required` | `boolean` | ไม่ได้ | — | — | กำหนดให้สินค้าต้องติดตามล็อต |
| `package_required` | `boolean` | ไม่ได้ | — | — | กำหนดให้ติดตามรายบรรจุภัณฑ์ |
| `shelf_life_hours` | `integer` | ได้ | — | — | อายุใช้งานสินค้าเป็นจำนวนชั่วโมง |
| `picking_policy` | `text` | ไม่ได้ | — | — | นโยบายเลือกลำดับสินค้า เช่น FEFO หรือ FIFO |
| `created_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่สร้างแถวข้อมูลในระบบ; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `updated_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่แก้ไขแถวข้อมูลล่าสุด ต้องอัปเดตทุกช่องทางเขียน; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `version` | `integer` | ไม่ได้ | — | — | เลขรุ่นแถวสำหรับตรวจการแก้ไขพร้อมกัน |

**Keys / Index:** U(company_id,code); I(company_id,barcode); I(company_id,deleted_at,created_at)

**กฎเฉพาะ:** tracking QUANTITY/WEIGHT/DUAL; price/cost เป็น master reference ไม่ใช่ source of stock value

## `catalog.product_units`

**เฟส:** P · **หนึ่งแถวคือ:** หนึ่งหน่วยซื้อ/แพ็กของสินค้า · **ประเภท:** mutable

**คำอธิบาย:** ตารางเก็บข้อมูล หนึ่งหน่วยซื้อ/แพ็กของสินค้า; หนึ่งแถวมีความหมายตามนี้และอยู่ในเฟส P

| คอลัมน์ | PostgreSQL type | NULL | PK / FK | อ้างอิง | คำอธิบายภาษาไทย |
|---|---|---|---|---|---|
| `id` | `uuid` | ไม่ได้ | PK | — | รหัสหลักภายในของแถวข้อมูล ไม่เปลี่ยนตลอดอายุรายการ; Primary Key ชนิด UUID ห้ามซ้ำหรือเป็น NULL |
| `company_id` | `uuid` | ไม่ได้ | FK | `org.companies.id` | รหัสอ้างอิงบริษัทเจ้าของข้อมูล ไปยัง org.companies.id (บทบาทฟิลด์ company_id) |
| `product_id` | `uuid` | ไม่ได้ | FK | `catalog.products.id` | รหัสอ้างอิงสินค้าในรายการ ไปยัง catalog.products.id (บทบาทฟิลด์ product_id) |
| `unit_id` | `uuid` | ไม่ได้ | FK | `catalog.units.id` | รหัสอ้างอิง หนึ่งหน่วยในบริษัท ไปยัง catalog.units.id (บทบาทฟิลด์ unit_id) |
| `code` | `text` | ไม่ได้ | — | — | รหัสธุรกิจของรายการตามขอบเขต Unique ของตาราง |
| `conversion_mode` | `text` | ไม่ได้ | — | — | วิธีแปลงหน่วย เช่นอัตราคงที่หรือใช้ผลชั่ง |
| `fixed_factor` | `numeric(24,9)` | ได้ | — | — | ตัวคูณแปลงหน่วยแบบคงที่; เลขทศนิยมแม่นยำ ส่ง API เป็น string ไม่คำนวณด้วย float |
| `order_precision` | `integer` | ไม่ได้ | — | — | จำนวนตำแหน่งทศนิยมที่อนุญาตในการสั่งซื้อ |
| `valid_from` | `timestamptz` | ไม่ได้ | — | — | วันเวลาเริ่มมีผลของข้อมูล; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `valid_to` | `timestamptz` | ได้ | — | — | วันเวลาสิ้นสุดการมีผลของข้อมูล; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `created_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่สร้างแถวข้อมูลในระบบ; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `updated_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่แก้ไขแถวข้อมูลล่าสุด ต้องอัปเดตทุกช่องทางเขียน; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `version` | `integer` | ไม่ได้ | — | — | เลขรุ่นแถวสำหรับตรวจการแก้ไขพร้อมกัน |

**Keys / Index:** U(company_id,product_id,code,valid_from)

**กฎเฉพาะ:** FIXED factor >0 และ dimension เทียบกันได้; VARIABLE_WEIGHT ไม่ใช้ factor แปลงแพ็กเป็น kg; document snapshot

## `catalog.product_barcodes`

**เฟส:** W · **หนึ่งแถวคือ:** หนึ่ง barcode สินค้า/หน่วยบรรจุ · **ประเภท:** mutable

**คำอธิบาย:** ตารางเก็บข้อมูล หนึ่ง barcode สินค้า/หน่วยบรรจุ; หนึ่งแถวมีความหมายตามนี้และอยู่ในเฟส W

| คอลัมน์ | PostgreSQL type | NULL | PK / FK | อ้างอิง | คำอธิบายภาษาไทย |
|---|---|---|---|---|---|
| `id` | `uuid` | ไม่ได้ | PK | — | รหัสหลักภายในของแถวข้อมูล ไม่เปลี่ยนตลอดอายุรายการ; Primary Key ชนิด UUID ห้ามซ้ำหรือเป็น NULL |
| `company_id` | `uuid` | ไม่ได้ | FK | `org.companies.id` | รหัสอ้างอิงบริษัทเจ้าของข้อมูล ไปยัง org.companies.id (บทบาทฟิลด์ company_id) |
| `product_id` | `uuid` | ไม่ได้ | FK | `catalog.products.id` | รหัสอ้างอิงสินค้าในรายการ ไปยัง catalog.products.id (บทบาทฟิลด์ product_id) |
| `product_unit_id` | `uuid` | ได้ | FK | `catalog.product_units.id` | รหัสอ้างอิง หนึ่งหน่วยซื้อ/แพ็กของสินค้า ไปยัง catalog.product_units.id (บทบาทฟิลด์ product_unit_id) |
| `code` | `text` | ไม่ได้ | — | — | รหัสธุรกิจของรายการตามขอบเขต Unique ของตาราง |
| `active` | `boolean` | ไม่ได้ | — | — | สถานะเปิดใช้งาน |
| `created_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่สร้างแถวข้อมูลในระบบ; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `updated_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่แก้ไขแถวข้อมูลล่าสุด ต้องอัปเดตทุกช่องทางเขียน; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `version` | `integer` | ไม่ได้ | — | — | เลขรุ่นแถวสำหรับตรวจการแก้ไขพร้อมกัน |

**Keys / Index:** U(company_id,code)

**กฎเฉพาะ:** Product.barcode เป็น primary alias ที่ต้องตรงกับตารางนี้

## `catalog.product_translations`

**เฟส:** F · **หนึ่งแถวคือ:** หนึ่งคำแปลต่อสินค้า/ภาษา · **ประเภท:** mutable

**คำอธิบาย:** ตารางเก็บข้อมูล หนึ่งคำแปลต่อสินค้า/ภาษา; หนึ่งแถวมีความหมายตามนี้และอยู่ในเฟส F

| คอลัมน์ | PostgreSQL type | NULL | PK / FK | อ้างอิง | คำอธิบายภาษาไทย |
|---|---|---|---|---|---|
| `id` | `uuid` | ไม่ได้ | PK | — | รหัสหลักภายในของแถวข้อมูล ไม่เปลี่ยนตลอดอายุรายการ; Primary Key ชนิด UUID ห้ามซ้ำหรือเป็น NULL |
| `company_id` | `uuid` | ไม่ได้ | FK | `org.companies.id` | รหัสอ้างอิงบริษัทเจ้าของข้อมูล ไปยัง org.companies.id (บทบาทฟิลด์ company_id) |
| `product_id` | `uuid` | ไม่ได้ | FK | `catalog.products.id` | รหัสอ้างอิงสินค้าในรายการ ไปยัง catalog.products.id (บทบาทฟิลด์ product_id) |
| `locale` | `text` | ไม่ได้ | — | — | รหัสภาษาที่ใช้แสดงผล |
| `name` | `text` | ไม่ได้ | — | — | ชื่อรายการสำหรับแสดงผล |
| `description` | `text` | ได้ | — | — | คำอธิบายรายละเอียด |
| `created_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่สร้างแถวข้อมูลในระบบ; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `updated_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่แก้ไขแถวข้อมูลล่าสุด ต้องอัปเดตทุกช่องทางเขียน; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `version` | `integer` | ไม่ได้ | — | — | เลขรุ่นแถวสำหรับตรวจการแก้ไขพร้อมกัน |

**Keys / Index:** U(company_id,product_id,locale)

**กฎเฉพาะ:** ใช้กฎ tenant, FK และ audit กลาง

## `catalog.branch_products`

**เฟส:** P · **หนึ่งแถวคือ:** หนึ่งนโยบายสินค้าต่อสาขา · **ประเภท:** mutable

**คำอธิบาย:** ตารางเก็บข้อมูล หนึ่งนโยบายสินค้าต่อสาขา; หนึ่งแถวมีความหมายตามนี้และอยู่ในเฟส P

| คอลัมน์ | PostgreSQL type | NULL | PK / FK | อ้างอิง | คำอธิบายภาษาไทย |
|---|---|---|---|---|---|
| `id` | `uuid` | ไม่ได้ | PK | — | รหัสหลักภายในของแถวข้อมูล ไม่เปลี่ยนตลอดอายุรายการ; Primary Key ชนิด UUID ห้ามซ้ำหรือเป็น NULL |
| `company_id` | `uuid` | ไม่ได้ | FK | `org.companies.id` | รหัสอ้างอิงบริษัทเจ้าของข้อมูล ไปยัง org.companies.id (บทบาทฟิลด์ company_id) |
| `product_id` | `uuid` | ไม่ได้ | FK | `catalog.products.id` | รหัสอ้างอิงสินค้าในรายการ ไปยัง catalog.products.id (บทบาทฟิลด์ product_id) |
| `branch_id` | `uuid` | ไม่ได้ | FK | `org.branches.id` | รหัสอ้างอิงสาขาเจ้าของรายการ ไปยัง org.branches.id (บทบาทฟิลด์ branch_id) |
| `active` | `boolean` | ไม่ได้ | — | — | สถานะเปิดใช้งาน |
| `min_stock` | `numeric(20,6)` | ได้ | — | — | จำนวนสต็อกขั้นต่ำสำหรับแจ้งเตือน; เลขทศนิยมแม่นยำ ส่ง API เป็น string ไม่คำนวณด้วย float |
| `par_stock` | `numeric(20,6)` | ได้ | — | — | จำนวนสต็อกเป้าหมาย; เลขทศนิยมแม่นยำ ส่ง API เป็น string ไม่คำนวณด้วย float |
| `shelf_life_hours` | `integer` | ได้ | — | — | อายุใช้งานสินค้าเป็นจำนวนชั่วโมง |
| `created_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่สร้างแถวข้อมูลในระบบ; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `updated_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่แก้ไขแถวข้อมูลล่าสุด ต้องอัปเดตทุกช่องทางเขียน; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `version` | `integer` | ไม่ได้ | — | — | เลขรุ่นแถวสำหรับตรวจการแก้ไขพร้อมกัน |

**Keys / Index:** U(company_id,product_id,branch_id)

**กฎเฉพาะ:** ไม่เก็บยอดคงเหลือใน master

## `catalog.suppliers`

**เฟส:** P · **หนึ่งแถวคือ:** หนึ่งผู้ขายในบริษัท · **ประเภท:** mutable

**คำอธิบาย:** ตารางเก็บข้อมูล หนึ่งผู้ขายในบริษัท; หนึ่งแถวมีความหมายตามนี้และอยู่ในเฟส P

| คอลัมน์ | PostgreSQL type | NULL | PK / FK | อ้างอิง | คำอธิบายภาษาไทย |
|---|---|---|---|---|---|
| `id` | `uuid` | ไม่ได้ | PK | — | รหัสหลักภายในของแถวข้อมูล ไม่เปลี่ยนตลอดอายุรายการ; Primary Key ชนิด UUID ห้ามซ้ำหรือเป็น NULL |
| `company_id` | `uuid` | ไม่ได้ | FK | `org.companies.id` | รหัสอ้างอิงบริษัทเจ้าของข้อมูล ไปยัง org.companies.id (บทบาทฟิลด์ company_id) |
| `code` | `text` | ไม่ได้ | — | — | รหัสธุรกิจของรายการตามขอบเขต Unique ของตาราง |
| `legal_name` | `text` | ไม่ได้ | — | — | ชื่อจดทะเบียนตามกฎหมาย |
| `tax_id` | `text` | ได้ | — | — | เลขประจำตัวผู้เสียภาษี เก็บข้อความ |
| `kind` | `text` | ไม่ได้ | — | — | ชนิดรายการตามค่าที่อนุญาตของตาราง |
| `internal_branch_id` | `uuid` | ได้ | FK | `org.branches.id` | รหัสอ้างอิง หนึ่งสาขาในบริษัท ไปยัง org.branches.id (บทบาทฟิลด์ internal_branch_id) |
| `active` | `boolean` | ไม่ได้ | — | — | สถานะเปิดใช้งาน |
| `deleted_at` | `timestamptz` | ได้ | — | — | เวลาลบแบบเก็บประวัติ ค่า NULL หมายถึงยังไม่ลบ; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `payment_terms_days` | `integer` | ไม่ได้ | — | — | จำนวนวันเครดิตตามเงื่อนไขชำระเงิน |
| `currency` | `char(3)` | ไม่ได้ | — | — | รหัสสกุลเงินของรายการ |
| `notes` | `text` | ได้ | — | — | หมายเหตุเพิ่มเติม |
| `created_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่สร้างแถวข้อมูลในระบบ; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `updated_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่แก้ไขแถวข้อมูลล่าสุด ต้องอัปเดตทุกช่องทางเขียน; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `version` | `integer` | ไม่ได้ | — | — | เลขรุ่นแถวสำหรับตรวจการแก้ไขพร้อมกัน |

**Keys / Index:** U(company_id,code)

**กฎเฉพาะ:** EXTERNAL/INTERNAL; internal ไม่แปลว่าต้องซื้อเสมอ ใช้ transfer ตามธุรกิจ

## `catalog.supplier_contacts`

**เฟส:** P · **หนึ่งแถวคือ:** หนึ่งผู้ติดต่อ supplier · **ประเภท:** mutable

**คำอธิบาย:** ตารางเก็บข้อมูล หนึ่งผู้ติดต่อ supplier; หนึ่งแถวมีความหมายตามนี้และอยู่ในเฟส P

| คอลัมน์ | PostgreSQL type | NULL | PK / FK | อ้างอิง | คำอธิบายภาษาไทย |
|---|---|---|---|---|---|
| `id` | `uuid` | ไม่ได้ | PK | — | รหัสหลักภายในของแถวข้อมูล ไม่เปลี่ยนตลอดอายุรายการ; Primary Key ชนิด UUID ห้ามซ้ำหรือเป็น NULL |
| `company_id` | `uuid` | ไม่ได้ | FK | `org.companies.id` | รหัสอ้างอิงบริษัทเจ้าของข้อมูล ไปยัง org.companies.id (บทบาทฟิลด์ company_id) |
| `supplier_id` | `uuid` | ไม่ได้ | FK | `catalog.suppliers.id` | รหัสอ้างอิงผู้ขายในรายการ ไปยัง catalog.suppliers.id (บทบาทฟิลด์ supplier_id) |
| `name` | `text` | ไม่ได้ | — | — | ชื่อรายการสำหรับแสดงผล |
| `phone` | `text` | ได้ | — | — | เบอร์โทรศัพท์ เก็บข้อความ |
| `email` | `text` | ได้ | — | — | อีเมลสำหรับติดต่อหรือเข้าสู่ระบบ |
| `channel` | `text` | ได้ | — | — | ช่องทางการส่งหรือสื่อสาร |
| `active` | `boolean` | ไม่ได้ | — | — | สถานะเปิดใช้งาน |
| `created_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่สร้างแถวข้อมูลในระบบ; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `updated_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่แก้ไขแถวข้อมูลล่าสุด ต้องอัปเดตทุกช่องทางเขียน; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `version` | `integer` | ไม่ได้ | — | — | เลขรุ่นแถวสำหรับตรวจการแก้ไขพร้อมกัน |

**Keys / Index:** I(company_id,supplier_id)

**กฎเฉพาะ:** ใช้กฎ tenant, FK และ audit กลาง

## `catalog.supplier_addresses`

**เฟส:** P · **หนึ่งแถวคือ:** หนึ่งที่อยู่ supplier · **ประเภท:** mutable

**คำอธิบาย:** ตารางเก็บข้อมูล หนึ่งที่อยู่ supplier; หนึ่งแถวมีความหมายตามนี้และอยู่ในเฟส P

| คอลัมน์ | PostgreSQL type | NULL | PK / FK | อ้างอิง | คำอธิบายภาษาไทย |
|---|---|---|---|---|---|
| `id` | `uuid` | ไม่ได้ | PK | — | รหัสหลักภายในของแถวข้อมูล ไม่เปลี่ยนตลอดอายุรายการ; Primary Key ชนิด UUID ห้ามซ้ำหรือเป็น NULL |
| `company_id` | `uuid` | ไม่ได้ | FK | `org.companies.id` | รหัสอ้างอิงบริษัทเจ้าของข้อมูล ไปยัง org.companies.id (บทบาทฟิลด์ company_id) |
| `supplier_id` | `uuid` | ไม่ได้ | FK | `catalog.suppliers.id` | รหัสอ้างอิงผู้ขายในรายการ ไปยัง catalog.suppliers.id (บทบาทฟิลด์ supplier_id) |
| `kind` | `text` | ไม่ได้ | — | — | ชนิดรายการตามค่าที่อนุญาตของตาราง |
| `address_line1` | `text` | ไม่ได้ | — | — | รายละเอียดที่อยู่หลัก บ้านเลขที่ อาคาร หมู่ ซอย ถนน |
| `address_line2` | `text` | ได้ | — | — | รายละเอียดที่อยู่เพิ่มเติม |
| `province_id` | `uuid` | ไม่ได้ | FK | `geo.provinces.id` | รหัสอ้างอิง หนึ่งจังหวัด/กรุงเทพมหานคร ไปยัง geo.provinces.id (บทบาทฟิลด์ province_id) |
| `district_id` | `uuid` | ไม่ได้ | FK | `geo.districts.id` | รหัสอ้างอิง หนึ่งอำเภอ/เขต ไปยัง geo.districts.id (บทบาทฟิลด์ district_id) |
| `subdistrict_id` | `uuid` | ไม่ได้ | FK | `geo.subdistricts.id` | รหัสอ้างอิง หนึ่งตำบล/แขวง ไปยัง geo.subdistricts.id (บทบาทฟิลด์ subdistrict_id) |
| `postal_code_id` | `uuid` | ไม่ได้ | FK | `geo.postal_codes.id` | รหัสอ้างอิง หนึ่งรหัสไปรษณีย์ไทย ไปยัง geo.postal_codes.id (บทบาทฟิลด์ postal_code_id) |
| `tax_branch_code` | `text` | ได้ | — | — | รหัสสาขาสำหรับเอกสารภาษี เก็บข้อความรักษาศูนย์นำหน้า |
| `is_default` | `boolean` | ไม่ได้ | — | — | ระบุว่าเป็นรายการหลักหรือค่าเริ่มต้นของกลุ่ม |
| `created_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่สร้างแถวข้อมูลในระบบ; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `updated_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่แก้ไขแถวข้อมูลล่าสุด ต้องอัปเดตทุกช่องทางเขียน; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `version` | `integer` | ไม่ได้ | — | — | เลขรุ่นแถวสำหรับตรวจการแก้ไขพร้อมกัน |

**Keys / Index:** partial U(company_id,supplier_id,kind) WHERE is_default

**กฎเฉพาะ:** ใช้กฎ tenant, FK และ audit กลาง; structured Thai address: composite geography FKs + postal mapping ตาม 07-address-model.md

## `catalog.supplier_products`

**เฟส:** P · **หนึ่งแถวคือ:** หนึ่งข้อเสนอสินค้า/หน่วยจาก supplier · **ประเภท:** mutable

**คำอธิบาย:** ตารางเก็บข้อมูล หนึ่งข้อเสนอสินค้า/หน่วยจาก supplier; หนึ่งแถวมีความหมายตามนี้และอยู่ในเฟส P

| คอลัมน์ | PostgreSQL type | NULL | PK / FK | อ้างอิง | คำอธิบายภาษาไทย |
|---|---|---|---|---|---|
| `id` | `uuid` | ไม่ได้ | PK | — | รหัสหลักภายในของแถวข้อมูล ไม่เปลี่ยนตลอดอายุรายการ; Primary Key ชนิด UUID ห้ามซ้ำหรือเป็น NULL |
| `company_id` | `uuid` | ไม่ได้ | FK | `org.companies.id` | รหัสอ้างอิงบริษัทเจ้าของข้อมูล ไปยัง org.companies.id (บทบาทฟิลด์ company_id) |
| `supplier_id` | `uuid` | ไม่ได้ | FK | `catalog.suppliers.id` | รหัสอ้างอิงผู้ขายในรายการ ไปยัง catalog.suppliers.id (บทบาทฟิลด์ supplier_id) |
| `product_id` | `uuid` | ไม่ได้ | FK | `catalog.products.id` | รหัสอ้างอิงสินค้าในรายการ ไปยัง catalog.products.id (บทบาทฟิลด์ product_id) |
| `product_unit_id` | `uuid` | ไม่ได้ | FK | `catalog.product_units.id` | รหัสอ้างอิง หนึ่งหน่วยซื้อ/แพ็กของสินค้า ไปยัง catalog.product_units.id (บทบาทฟิลด์ product_unit_id) |
| `supplier_sku` | `text` | ได้ | — | — | รหัสสินค้าของผู้ขาย |
| `minimum_order` | `numeric(20,6)` | ได้ | — | — | จำนวนสั่งซื้อขั้นต่ำตามหน่วยที่กำหนด; เลขทศนิยมแม่นยำ ส่ง API เป็น string ไม่คำนวณด้วย float |
| `lead_days` | `integer` | ได้ | — | — | จำนวนวันเตรียมสินค้าก่อนส่ง |
| `active` | `boolean` | ไม่ได้ | — | — | สถานะเปิดใช้งาน |
| `created_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่สร้างแถวข้อมูลในระบบ; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `updated_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่แก้ไขแถวข้อมูลล่าสุด ต้องอัปเดตทุกช่องทางเขียน; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `version` | `integer` | ไม่ได้ | — | — | เลขรุ่นแถวสำหรับตรวจการแก้ไขพร้อมกัน |

**Keys / Index:** U(company_id,supplier_id,product_id,product_unit_id)

**กฎเฉพาะ:** unit ต้องเป็นของ product เดียวกัน

## `catalog.supplier_prices`

**เฟส:** P · **หนึ่งแถวคือ:** หนึ่งราคาช่วงเวลาต่อข้อเสนอ · **ประเภท:** mutable

**คำอธิบาย:** ตารางเก็บข้อมูล หนึ่งราคาช่วงเวลาต่อข้อเสนอ; หนึ่งแถวมีความหมายตามนี้และอยู่ในเฟส P

| คอลัมน์ | PostgreSQL type | NULL | PK / FK | อ้างอิง | คำอธิบายภาษาไทย |
|---|---|---|---|---|---|
| `id` | `uuid` | ไม่ได้ | PK | — | รหัสหลักภายในของแถวข้อมูล ไม่เปลี่ยนตลอดอายุรายการ; Primary Key ชนิด UUID ห้ามซ้ำหรือเป็น NULL |
| `company_id` | `uuid` | ไม่ได้ | FK | `org.companies.id` | รหัสอ้างอิงบริษัทเจ้าของข้อมูล ไปยัง org.companies.id (บทบาทฟิลด์ company_id) |
| `supplier_product_id` | `uuid` | ไม่ได้ | FK | `catalog.supplier_products.id` | รหัสอ้างอิง หนึ่งข้อเสนอสินค้า/หน่วยจาก supplier ไปยัง catalog.supplier_products.id (บทบาทฟิลด์ supplier_product_id) |
| `valid_from` | `timestamptz` | ไม่ได้ | — | — | วันเวลาเริ่มมีผลของข้อมูล; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `valid_to` | `timestamptz` | ได้ | — | — | วันเวลาสิ้นสุดการมีผลของข้อมูล; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `unit_price` | `numeric(20,6)` | ไม่ได้ | — | — | ราคาต่อหน่วยตามหน่วยและสกุลเงินในรายการ; เลขทศนิยมแม่นยำ ส่ง API เป็น string ไม่คำนวณด้วย float |
| `currency` | `char(3)` | ไม่ได้ | — | — | รหัสสกุลเงินของรายการ |
| `tax_code` | `text` | ไม่ได้ | — | — | รหัสประเภทภาษี |
| `tax_rate` | `numeric(9,6)` | ไม่ได้ | — | — | อัตราภาษีเป็นร้อยละ; เลขทศนิยมแม่นยำ ส่ง API เป็น string ไม่คำนวณด้วย float |
| `tax_inclusive` | `boolean` | ไม่ได้ | — | — | ระบุว่าราคารวมภาษีแล้ว |
| `discount_percent` | `numeric(9,6)` | ไม่ได้ | — | — | ส่วนลดเป็นร้อยละ; เลขทศนิยมแม่นยำ ส่ง API เป็น string ไม่คำนวณด้วย float |
| `created_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่สร้างแถวข้อมูลในระบบ; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `updated_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่แก้ไขแถวข้อมูลล่าสุด ต้องอัปเดตทุกช่องทางเขียน; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `version` | `integer` | ไม่ได้ | — | — | เลขรุ่นแถวสำหรับตรวจการแก้ไขพร้อมกัน |

**Keys / Index:** I(company_id,supplier_product_id,valid_from); no overlapping active ranges

**กฎเฉพาะ:** ราคาเปลี่ยนสร้างช่วงใหม่ ไม่แก้ snapshot PO

## `catalog.branch_supplier_products`

**เฟส:** P · **หนึ่งแถวคือ:** หนึ่งรายการที่สาขาซื้อได้ · **ประเภท:** mutable

**คำอธิบาย:** ตารางเก็บข้อมูล หนึ่งรายการที่สาขาซื้อได้; หนึ่งแถวมีความหมายตามนี้และอยู่ในเฟส P

| คอลัมน์ | PostgreSQL type | NULL | PK / FK | อ้างอิง | คำอธิบายภาษาไทย |
|---|---|---|---|---|---|
| `id` | `uuid` | ไม่ได้ | PK | — | รหัสหลักภายในของแถวข้อมูล ไม่เปลี่ยนตลอดอายุรายการ; Primary Key ชนิด UUID ห้ามซ้ำหรือเป็น NULL |
| `company_id` | `uuid` | ไม่ได้ | FK | `org.companies.id` | รหัสอ้างอิงบริษัทเจ้าของข้อมูล ไปยัง org.companies.id (บทบาทฟิลด์ company_id) |
| `branch_id` | `uuid` | ไม่ได้ | FK | `org.branches.id` | รหัสอ้างอิงสาขาเจ้าของรายการ ไปยัง org.branches.id (บทบาทฟิลด์ branch_id) |
| `supplier_product_id` | `uuid` | ไม่ได้ | FK | `catalog.supplier_products.id` | รหัสอ้างอิง หนึ่งข้อเสนอสินค้า/หน่วยจาก supplier ไปยัง catalog.supplier_products.id (บทบาทฟิลด์ supplier_product_id) |
| `active` | `boolean` | ไม่ได้ | — | — | สถานะเปิดใช้งาน |
| `created_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่สร้างแถวข้อมูลในระบบ; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `updated_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่แก้ไขแถวข้อมูลล่าสุด ต้องอัปเดตทุกช่องทางเขียน; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `version` | `integer` | ไม่ได้ | — | — | เลขรุ่นแถวสำหรับตรวจการแก้ไขพร้อมกัน |

**Keys / Index:** U(company_id,branch_id,supplier_product_id)

**กฎเฉพาะ:** ใช้กฎ tenant, FK และ audit กลาง

## `purchasing.purchase_orders`

**เฟส:** P · **หนึ่งแถวคือ:** หัว PO และตัวชี้รุ่นที่มีผล · **ประเภท:** mutable

**คำอธิบาย:** ตารางเก็บข้อมูล หัว PO และตัวชี้รุ่นที่มีผล; หนึ่งแถวมีความหมายตามนี้และอยู่ในเฟส P

| คอลัมน์ | PostgreSQL type | NULL | PK / FK | อ้างอิง | คำอธิบายภาษาไทย |
|---|---|---|---|---|---|
| `id` | `uuid` | ไม่ได้ | PK | — | รหัสหลักภายในของแถวข้อมูล ไม่เปลี่ยนตลอดอายุรายการ; Primary Key ชนิด UUID ห้ามซ้ำหรือเป็น NULL |
| `company_id` | `uuid` | ไม่ได้ | FK | `org.companies.id` | รหัสอ้างอิงบริษัทเจ้าของข้อมูล ไปยัง org.companies.id (บทบาทฟิลด์ company_id) |
| `document_id` | `uuid` | ไม่ได้ | FK | `platform.documents.id` | รหัสอ้างอิง หนึ่งเอกสารธุรกิจที่เป็น FK กลาง ไปยัง platform.documents.id (บทบาทฟิลด์ document_id) |
| `supplier_id` | `uuid` | ไม่ได้ | FK | `catalog.suppliers.id` | รหัสอ้างอิงผู้ขายในรายการ ไปยัง catalog.suppliers.id (บทบาทฟิลด์ supplier_id) |
| `warehouse_id` | `uuid` | ไม่ได้ | FK | `org.warehouses.id` | รหัสอ้างอิงคลังที่เกี่ยวข้อง ไปยัง org.warehouses.id (บทบาทฟิลด์ warehouse_id) |
| `current_revision_no` | `integer` | ไม่ได้ | — | — | หมายเลขฉบับแก้ไขปัจจุบัน |
| `effective_revision_no` | `integer` | ได้ | — | — | หมายเลขฉบับเอกสารที่มีผลใช้งาน |
| `held` | `boolean` | ไม่ได้ | — | — | สถานะระงับการใช้งานรายการ |
| `hold_reason` | `text` | ได้ | — | — | เหตุผลที่ระงับรายการ |
| `legacy_number` | `text` | ได้ | — | — | เลขเอกสารจากระบบเดิม |
| `created_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่สร้างแถวข้อมูลในระบบ; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `updated_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่แก้ไขแถวข้อมูลล่าสุด ต้องอัปเดตทุกช่องทางเขียน; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `version` | `integer` | ไม่ได้ | — | — | เลขรุ่นแถวสำหรับตรวจการแก้ไขพร้อมกัน |

**Keys / Index:** U(company_id,document_id); I(company_id,supplier_id)

**กฎเฉพาะ:** FK current/effective -> revisions แบบ deferred; branch/supplier/warehouse immutable หลัง issue

## `purchasing.po_lines`

**เฟส:** P · **หนึ่งแถวคือ:** identity รายการ PO คงที่ข้ามรุ่น · **ประเภท:** mutable

**คำอธิบาย:** ตารางเก็บข้อมูล identity รายการ PO คงที่ข้ามรุ่น; หนึ่งแถวมีความหมายตามนี้และอยู่ในเฟส P

| คอลัมน์ | PostgreSQL type | NULL | PK / FK | อ้างอิง | คำอธิบายภาษาไทย |
|---|---|---|---|---|---|
| `id` | `uuid` | ไม่ได้ | PK | — | รหัสหลักภายในของแถวข้อมูล ไม่เปลี่ยนตลอดอายุรายการ; Primary Key ชนิด UUID ห้ามซ้ำหรือเป็น NULL |
| `company_id` | `uuid` | ไม่ได้ | FK | `org.companies.id` | รหัสอ้างอิงบริษัทเจ้าของข้อมูล ไปยัง org.companies.id (บทบาทฟิลด์ company_id) |
| `document_line_id` | `uuid` | ไม่ได้ | FK | `platform.document_lines.id` | รหัสอ้างอิง หนึ่ง line identity ในเอกสาร ไปยัง platform.document_lines.id (บทบาทฟิลด์ document_line_id) |
| `po_id` | `uuid` | ไม่ได้ | FK | `purchasing.purchase_orders.id` | รหัสอ้างอิง หัว PO และตัวชี้รุ่นที่มีผล ไปยัง purchasing.purchase_orders.id (บทบาทฟิลด์ po_id) |
| `product_id` | `uuid` | ไม่ได้ | FK | `catalog.products.id` | รหัสอ้างอิงสินค้าในรายการ ไปยัง catalog.products.id (บทบาทฟิลด์ product_id) |
| `created_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่สร้างแถวข้อมูลในระบบ; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `updated_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่แก้ไขแถวข้อมูลล่าสุด ต้องอัปเดตทุกช่องทางเขียน; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `version` | `integer` | ไม่ได้ | — | — | เลขรุ่นแถวสำหรับตรวจการแก้ไขพร้อมกัน |

**Keys / Index:** U(company_id,document_line_id)

**กฎเฉพาะ:** ห้ามใช้ line_no ใหม่ทับสินค้าเดิมที่มีส่งมอบ; remove ด้วย revision ไม่ลบ identity

## `purchasing.po_revisions`

**เฟส:** P · **หนึ่งแถวคือ:** หนึ่งรุ่น PO snapshot · **ประเภท:** mutable

**คำอธิบาย:** ตารางเก็บข้อมูล หนึ่งรุ่น PO snapshot; หนึ่งแถวมีความหมายตามนี้และอยู่ในเฟส P

| คอลัมน์ | PostgreSQL type | NULL | PK / FK | อ้างอิง | คำอธิบายภาษาไทย |
|---|---|---|---|---|---|
| `id` | `uuid` | ไม่ได้ | PK | — | รหัสหลักภายในของแถวข้อมูล ไม่เปลี่ยนตลอดอายุรายการ; Primary Key ชนิด UUID ห้ามซ้ำหรือเป็น NULL |
| `company_id` | `uuid` | ไม่ได้ | FK | `org.companies.id` | รหัสอ้างอิงบริษัทเจ้าของข้อมูล ไปยัง org.companies.id (บทบาทฟิลด์ company_id) |
| `po_id` | `uuid` | ไม่ได้ | FK | `purchasing.purchase_orders.id` | รหัสอ้างอิง หัว PO และตัวชี้รุ่นที่มีผล ไปยัง purchasing.purchase_orders.id (บทบาทฟิลด์ po_id) |
| `revision_no` | `integer` | ไม่ได้ | — | — | หมายเลขฉบับเอกสาร |
| `state` | `text` | ไม่ได้ | — | — | สถานะภายในตามวงจรงานที่อนุญาต |
| `currency` | `char(3)` | ไม่ได้ | — | — | รหัสสกุลเงินของรายการ |
| `order_date` | `date` | ไม่ได้ | — | — | วันที่สั่งซื้อทางธุรกิจ; เป็นวันที่ปฏิทินธุรกิจ YYYY-MM-DD ไม่มีเวลาและไม่เลื่อนวันด้วย timezone |
| `requested_delivery_date` | `date` | ไม่ได้ | — | — | วันที่ผู้ซื้อขอให้จัดส่ง; เป็นวันที่ปฏิทินธุรกิจ YYYY-MM-DD ไม่มีเวลาและไม่เลื่อนวันด้วย timezone |
| `buyer_snapshot` | `jsonb` | ไม่ได้ | — | — | สำเนาข้อมูลผู้ซื้อและที่อยู่ ณ เวลาออกเอกสาร; ต้องตรวจ schema และจำกัดข้อมูลตามสิทธิ์ |
| `supplier_snapshot` | `jsonb` | ไม่ได้ | — | — | สำเนาข้อมูลผู้ขายและที่อยู่ ณ เวลาออกเอกสาร; ต้องตรวจ schema และจำกัดข้อมูลตามสิทธิ์ |
| `shipping_snapshot` | `jsonb` | ไม่ได้ | — | — | สำเนาปลายทางจัดส่งและที่อยู่ ณ เวลาออกเอกสาร; ต้องตรวจ schema และจำกัดข้อมูลตามสิทธิ์ |
| `terms_snapshot` | `jsonb` | ไม่ได้ | — | — | สำเนาเงื่อนไขซื้อขาย ณ เวลาออกเอกสาร; ต้องตรวจ schema และจำกัดข้อมูลตามสิทธิ์ |
| `net_amount` | `numeric(20,2)` | ไม่ได้ | — | — | จำนวนเงินสุทธิตามสูตรเอกสาร; เลขทศนิยมแม่นยำ ส่ง API เป็น string ไม่คำนวณด้วย float |
| `tax_amount` | `numeric(20,2)` | ไม่ได้ | — | — | จำนวนเงินภาษี; เลขทศนิยมแม่นยำ ส่ง API เป็น string ไม่คำนวณด้วย float |
| `gross_amount` | `numeric(20,2)` | ไม่ได้ | — | — | จำนวนเงินรวมก่อนหักรายการตามสูตรเอกสาร; เลขทศนิยมแม่นยำ ส่ง API เป็น string ไม่คำนวณด้วย float |
| `reason` | `text` | ได้ | — | — | เหตุผลประกอบการดำเนินการ |
| `content_hash` | `text` | ไม่ได้ | — | — | ค่าแฮชตรวจความเปลี่ยนแปลงของเนื้อหา |
| `approval_request_id` | `uuid` | ได้ | FK | `platform.approval_requests.id` | รหัสอ้างอิง หนึ่งคำขออนุมัติ snapshot ไปยัง platform.approval_requests.id (บทบาทฟิลด์ approval_request_id) |
| `issued_at` | `timestamptz` | ได้ | — | — | เวลาที่ออกเอกสารหรือเบิกจ่ายตามบริบทตาราง; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `created_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่สร้างแถวข้อมูลในระบบ; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `updated_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่แก้ไขแถวข้อมูลล่าสุด ต้องอัปเดตทุกช่องทางเขียน; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `version` | `integer` | ไม่ได้ | — | — | เลขรุ่นแถวสำหรับตรวจการแก้ไขพร้อมกัน |

**Keys / Index:** U(company_id,po_id,revision_no)

**กฎเฉพาะ:** issued content immutable; state lifecycle ต่างจาก delivery/warehouse status

## `purchasing.po_revision_lines`

**เฟส:** P · **หนึ่งแถวคือ:** หนึ่ง line snapshot ต่อ revision · **ประเภท:** mutable

**คำอธิบาย:** ตารางเก็บข้อมูล หนึ่ง line snapshot ต่อ revision; หนึ่งแถวมีความหมายตามนี้และอยู่ในเฟส P

| คอลัมน์ | PostgreSQL type | NULL | PK / FK | อ้างอิง | คำอธิบายภาษาไทย |
|---|---|---|---|---|---|
| `id` | `uuid` | ไม่ได้ | PK | — | รหัสหลักภายในของแถวข้อมูล ไม่เปลี่ยนตลอดอายุรายการ; Primary Key ชนิด UUID ห้ามซ้ำหรือเป็น NULL |
| `company_id` | `uuid` | ไม่ได้ | FK | `org.companies.id` | รหัสอ้างอิงบริษัทเจ้าของข้อมูล ไปยัง org.companies.id (บทบาทฟิลด์ company_id) |
| `revision_id` | `uuid` | ไม่ได้ | FK | `purchasing.po_revisions.id` | รหัสอ้างอิง หนึ่งรุ่น PO snapshot ไปยัง purchasing.po_revisions.id (บทบาทฟิลด์ revision_id) |
| `po_line_id` | `uuid` | ไม่ได้ | FK | `purchasing.po_lines.id` | รหัสอ้างอิง identity รายการ PO คงที่ข้ามรุ่น ไปยัง purchasing.po_lines.id (บทบาทฟิลด์ po_line_id) |
| `supplier_product_id` | `uuid` | ได้ | FK | `catalog.supplier_products.id` | รหัสอ้างอิง หนึ่งข้อเสนอสินค้า/หน่วยจาก supplier ไปยัง catalog.supplier_products.id (บทบาทฟิลด์ supplier_product_id) |
| `product_unit_id` | `uuid` | ไม่ได้ | FK | `catalog.product_units.id` | รหัสอ้างอิง หนึ่งหน่วยซื้อ/แพ็กของสินค้า ไปยัง catalog.product_units.id (บทบาทฟิลด์ product_unit_id) |
| `ordered_qty` | `numeric(20,6)` | ไม่ได้ | — | — | จำนวนที่ระบุสั่งซื้อ; เลขทศนิยมแม่นยำ ส่ง API เป็น string ไม่คำนวณด้วย float |
| `unit_price` | `numeric(20,6)` | ไม่ได้ | — | — | ราคาต่อหน่วยตามหน่วยและสกุลเงินในรายการ; เลขทศนิยมแม่นยำ ส่ง API เป็น string ไม่คำนวณด้วย float |
| `discount_amount` | `numeric(20,2)` | ไม่ได้ | — | — | ส่วนลดเป็นจำนวนเงิน; เลขทศนิยมแม่นยำ ส่ง API เป็น string ไม่คำนวณด้วย float |
| `tax_rate` | `numeric(9,6)` | ไม่ได้ | — | — | อัตราภาษีเป็นร้อยละ; เลขทศนิยมแม่นยำ ส่ง API เป็น string ไม่คำนวณด้วย float |
| `tax_amount` | `numeric(20,2)` | ไม่ได้ | — | — | จำนวนเงินภาษี; เลขทศนิยมแม่นยำ ส่ง API เป็น string ไม่คำนวณด้วย float |
| `net_amount` | `numeric(20,2)` | ไม่ได้ | — | — | จำนวนเงินสุทธิตามสูตรเอกสาร; เลขทศนิยมแม่นยำ ส่ง API เป็น string ไม่คำนวณด้วย float |
| `gross_amount` | `numeric(20,2)` | ไม่ได้ | — | — | จำนวนเงินรวมก่อนหักรายการตามสูตรเอกสาร; เลขทศนิยมแม่นยำ ส่ง API เป็น string ไม่คำนวณด้วย float |
| `conversion_snapshot` | `jsonb` | ไม่ได้ | — | — | สำเนากฎแปลงหน่วย ณ เวลาทำรายการ; ต้องตรวจ schema และจำกัดข้อมูลตามสิทธิ์ |
| `description_snapshot` | `text` | ไม่ได้ | — | — | สำเนาคำอธิบาย ณ เวลาทำรายการ |
| `removed` | `boolean` | ไม่ได้ | — | — | ระบุว่ารายการถูกนำออกจากฉบับเอกสาร |
| `created_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่สร้างแถวข้อมูลในระบบ; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `updated_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่แก้ไขแถวข้อมูลล่าสุด ต้องอัปเดตทุกช่องทางเขียน; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `version` | `integer` | ไม่ได้ | — | — | เลขรุ่นแถวสำหรับตรวจการแก้ไขพร้อมกัน |

**Keys / Index:** U(company_id,revision_id,po_line_id)

**กฎเฉพาะ:** line.po_id=revision.po_id; qty >=accepted+closed; order dimension immutable once confirmed

## `purchasing.po_charges`

**เฟส:** P · **หนึ่งแถวคือ:** หนึ่งส่วนลด/ค่าใช้จ่ายท้าย revision · **ประเภท:** mutable

**คำอธิบาย:** ตารางเก็บข้อมูล หนึ่งส่วนลด/ค่าใช้จ่ายท้าย revision; หนึ่งแถวมีความหมายตามนี้และอยู่ในเฟส P

| คอลัมน์ | PostgreSQL type | NULL | PK / FK | อ้างอิง | คำอธิบายภาษาไทย |
|---|---|---|---|---|---|
| `id` | `uuid` | ไม่ได้ | PK | — | รหัสหลักภายในของแถวข้อมูล ไม่เปลี่ยนตลอดอายุรายการ; Primary Key ชนิด UUID ห้ามซ้ำหรือเป็น NULL |
| `company_id` | `uuid` | ไม่ได้ | FK | `org.companies.id` | รหัสอ้างอิงบริษัทเจ้าของข้อมูล ไปยัง org.companies.id (บทบาทฟิลด์ company_id) |
| `revision_id` | `uuid` | ไม่ได้ | FK | `purchasing.po_revisions.id` | รหัสอ้างอิง หนึ่งรุ่น PO snapshot ไปยัง purchasing.po_revisions.id (บทบาทฟิลด์ revision_id) |
| `kind` | `text` | ไม่ได้ | — | — | ชนิดรายการตามค่าที่อนุญาตของตาราง |
| `amount` | `numeric(20,2)` | ไม่ได้ | — | — | จำนวนเงินของรายการตามสกุลเงินที่กำหนด; เลขทศนิยมแม่นยำ ส่ง API เป็น string ไม่คำนวณด้วย float |
| `tax_rate` | `numeric(9,6)` | ไม่ได้ | — | — | อัตราภาษีเป็นร้อยละ; เลขทศนิยมแม่นยำ ส่ง API เป็น string ไม่คำนวณด้วย float |
| `allocation_basis` | `text` | ไม่ได้ | — | — | เกณฑ์ที่ใช้แบ่งต้นทุน |
| `allocation_snapshot` | `jsonb` | ไม่ได้ | — | — | สำเนารายละเอียดการจัดสรรต้นทุน ณ เวลาทำรายการ; ต้องตรวจ schema และจำกัดข้อมูลตามสิทธิ์ |
| `created_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่สร้างแถวข้อมูลในระบบ; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `updated_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่แก้ไขแถวข้อมูลล่าสุด ต้องอัปเดตทุกช่องทางเขียน; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `version` | `integer` | ไม่ได้ | — | — | เลขรุ่นแถวสำหรับตรวจการแก้ไขพร้อมกัน |

**Keys / Index:** I(company_id,revision_id)

**กฎเฉพาะ:** DISCOUNT/FREIGHT/OTHER; rounding remainder deterministic รายบรรทัด

## `purchasing.po_dispatches`

**เฟส:** P · **หนึ่งแถวคือ:** หนึ่งความพยายามส่ง PO revision · **ประเภท:** mutable

**คำอธิบาย:** ตารางเก็บข้อมูล หนึ่งความพยายามส่ง PO revision; หนึ่งแถวมีความหมายตามนี้และอยู่ในเฟส P

| คอลัมน์ | PostgreSQL type | NULL | PK / FK | อ้างอิง | คำอธิบายภาษาไทย |
|---|---|---|---|---|---|
| `id` | `uuid` | ไม่ได้ | PK | — | รหัสหลักภายในของแถวข้อมูล ไม่เปลี่ยนตลอดอายุรายการ; Primary Key ชนิด UUID ห้ามซ้ำหรือเป็น NULL |
| `company_id` | `uuid` | ไม่ได้ | FK | `org.companies.id` | รหัสอ้างอิงบริษัทเจ้าของข้อมูล ไปยัง org.companies.id (บทบาทฟิลด์ company_id) |
| `revision_id` | `uuid` | ไม่ได้ | FK | `purchasing.po_revisions.id` | รหัสอ้างอิง หนึ่งรุ่น PO snapshot ไปยัง purchasing.po_revisions.id (บทบาทฟิลด์ revision_id) |
| `channel` | `text` | ไม่ได้ | — | — | ช่องทางการส่งหรือสื่อสาร |
| `recipient_snapshot` | `jsonb` | ไม่ได้ | — | — | สำเนาข้อมูลผู้รับ ณ เวลาส่ง; ต้องตรวจ schema และจำกัดข้อมูลตามสิทธิ์ |
| `sent_by` | `uuid` | ไม่ได้ | FK | `security.users.id` | รหัสอ้างอิง หนึ่งตัวตนผู้ใช้กลาง ไปยัง security.users.id (บทบาทฟิลด์ sent_by) |
| `sent_at` | `timestamptz` | ได้ | — | — | เวลาที่ส่งออกสำเร็จ; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `acknowledged_at` | `timestamptz` | ได้ | — | — | เวลาที่ได้รับการตอบรับ; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `evidence_file_id` | `uuid` | ได้ | FK | `platform.files.id` | รหัสอ้างอิง หนึ่ง object ส่วนตัว ไปยัง platform.files.id (บทบาทฟิลด์ evidence_file_id) |
| `status` | `text` | ไม่ได้ | — | — | สถานะรายการตาม state machine ของตาราง |
| `created_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่สร้างแถวข้อมูลในระบบ; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `updated_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่แก้ไขแถวข้อมูลล่าสุด ต้องอัปเดตทุกช่องทางเขียน; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `version` | `integer` | ไม่ได้ | — | — | เลขรุ่นแถวสำหรับตรวจการแก้ไขพร้อมกัน |

**Keys / Index:** I(company_id,revision_id,created_at)

**กฎเฉพาะ:** download ไม่ใช่ sent; ใบตอบรับเก็บหลักฐาน; payload ผู้รับ/รุ่น immutable เปลี่ยนได้เฉพาะสถานะการส่ง/ตอบรับพร้อม audit

## `purchasing.delivery_schedules`

**เฟส:** P · **หนึ่งแถวคือ:** หนึ่งนัดส่งต่อ PO line · **ประเภท:** append

**คำอธิบาย:** ตารางเก็บข้อมูล หนึ่งนัดส่งต่อ PO line; หนึ่งแถวมีความหมายตามนี้และอยู่ในเฟส P

| คอลัมน์ | PostgreSQL type | NULL | PK / FK | อ้างอิง | คำอธิบายภาษาไทย |
|---|---|---|---|---|---|
| `id` | `uuid` | ไม่ได้ | PK | — | รหัสหลักภายในของแถวข้อมูล ไม่เปลี่ยนตลอดอายุรายการ; Primary Key ชนิด UUID ห้ามซ้ำหรือเป็น NULL |
| `company_id` | `uuid` | ไม่ได้ | FK | `org.companies.id` | รหัสอ้างอิงบริษัทเจ้าของข้อมูล ไปยัง org.companies.id (บทบาทฟิลด์ company_id) |
| `po_line_id` | `uuid` | ไม่ได้ | FK | `purchasing.po_lines.id` | รหัสอ้างอิง identity รายการ PO คงที่ข้ามรุ่น ไปยัง purchasing.po_lines.id (บทบาทฟิลด์ po_line_id) |
| `promised_at` | `timestamptz` | ไม่ได้ | — | — | เวลานัดส่งที่ผู้ขายยืนยัน; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `scheduled_order_qty` | `numeric(20,6)` | ไม่ได้ | — | — | จำนวนตามหน่วยสั่งซื้อที่นัดส่งในรอบนี้; เลขทศนิยมแม่นยำ ส่ง API เป็น string ไม่คำนวณด้วย float |
| `supersedes_id` | `uuid` | ได้ | FK | `purchasing.delivery_schedules.id` | รหัสอ้างอิง หนึ่งนัดส่งต่อ PO line ไปยัง purchasing.delivery_schedules.id (บทบาทฟิลด์ supersedes_id) |
| `reason` | `text` | ได้ | — | — | เหตุผลประกอบการดำเนินการ |
| `supplier_confirmed` | `boolean` | ไม่ได้ | — | — | ระบุว่าผู้ขายยืนยันข้อมูลแล้ว |
| `created_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่สร้างแถวข้อมูลในระบบ; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |

**Keys / Index:** I(company_id,promised_at)

**กฎเฉพาะ:** การแก้นัดไม่เปลี่ยน qty PO; เก็บนัดเดิม

## `purchasing.po_closures`

**เฟส:** P · **หนึ่งแถวคือ:** หนึ่งปิด/เปิดค้างรายบรรทัด · **ประเภท:** append

**คำอธิบาย:** ตารางเก็บข้อมูล หนึ่งปิด/เปิดค้างรายบรรทัด; หนึ่งแถวมีความหมายตามนี้และอยู่ในเฟส P

| คอลัมน์ | PostgreSQL type | NULL | PK / FK | อ้างอิง | คำอธิบายภาษาไทย |
|---|---|---|---|---|---|
| `id` | `uuid` | ไม่ได้ | PK | — | รหัสหลักภายในของแถวข้อมูล ไม่เปลี่ยนตลอดอายุรายการ; Primary Key ชนิด UUID ห้ามซ้ำหรือเป็น NULL |
| `company_id` | `uuid` | ไม่ได้ | FK | `org.companies.id` | รหัสอ้างอิงบริษัทเจ้าของข้อมูล ไปยัง org.companies.id (บทบาทฟิลด์ company_id) |
| `po_line_id` | `uuid` | ไม่ได้ | FK | `purchasing.po_lines.id` | รหัสอ้างอิง identity รายการ PO คงที่ข้ามรุ่น ไปยัง purchasing.po_lines.id (บทบาทฟิลด์ po_line_id) |
| `document_id` | `uuid` | ไม่ได้ | FK | `platform.documents.id` | รหัสอ้างอิง หนึ่งเอกสารธุรกิจที่เป็น FK กลาง ไปยัง platform.documents.id (บทบาทฟิลด์ document_id) |
| `action` | `text` | ไม่ได้ | — | — | การกระทำที่บันทึก |
| `order_qty` | `numeric(20,6)` | ไม่ได้ | — | — | จำนวนตามหน่วยสั่งซื้อ; เลขทศนิยมแม่นยำ ส่ง API เป็น string ไม่คำนวณด้วย float |
| `reopens_id` | `uuid` | ได้ | FK | `purchasing.po_closures.id` | รหัสอ้างอิง หนึ่งปิด/เปิดค้างรายบรรทัด ไปยัง purchasing.po_closures.id (บทบาทฟิลด์ reopens_id) |
| `approval_request_id` | `uuid` | ไม่ได้ | FK | `platform.approval_requests.id` | รหัสอ้างอิง หนึ่งคำขออนุมัติ snapshot ไปยัง platform.approval_requests.id (บทบาทฟิลด์ approval_request_id) |
| `reason` | `text` | ไม่ได้ | — | — | เหตุผลประกอบการดำเนินการ |
| `created_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่สร้างแถวข้อมูลในระบบ; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |

**Keys / Index:** I(company_id,po_line_id)

**กฎเฉพาะ:** qty>0; REOPEN อ้าง CLOSE เดิมและ sum <= original; approved only contributes

## `purchasing.po_line_progress`

**เฟส:** P · **หนึ่งแถวคือ:** projection สำหรับล็อกยอดต่อ PO line · **ประเภท:** mutable

**คำอธิบาย:** ตารางเก็บข้อมูล projection สำหรับล็อกยอดต่อ PO line; หนึ่งแถวมีความหมายตามนี้และอยู่ในเฟส P

| คอลัมน์ | PostgreSQL type | NULL | PK / FK | อ้างอิง | คำอธิบายภาษาไทย |
|---|---|---|---|---|---|
| `id` | `uuid` | ไม่ได้ | PK | — | รหัสหลักภายในของแถวข้อมูล ไม่เปลี่ยนตลอดอายุรายการ; Primary Key ชนิด UUID ห้ามซ้ำหรือเป็น NULL |
| `company_id` | `uuid` | ไม่ได้ | FK | `org.companies.id` | รหัสอ้างอิงบริษัทเจ้าของข้อมูล ไปยัง org.companies.id (บทบาทฟิลด์ company_id) |
| `po_line_id` | `uuid` | ไม่ได้ | FK | `purchasing.po_lines.id` | รหัสอ้างอิง identity รายการ PO คงที่ข้ามรุ่น ไปยัง purchasing.po_lines.id (บทบาทฟิลด์ po_line_id) |
| `effective_order_qty` | `numeric(20,6)` | ไม่ได้ | — | — | จำนวนสั่งซื้อที่มีผลหลังปรับฉบับเอกสาร; เลขทศนิยมแม่นยำ ส่ง API เป็น string ไม่คำนวณด้วย float |
| `accepted_order_qty` | `numeric(20,6)` | ไม่ได้ | — | — | จำนวนที่ยอมรับตามหน่วยสั่งซื้อ; เลขทศนิยมแม่นยำ ส่ง API เป็น string ไม่คำนวณด้วย float |
| `closed_order_qty` | `numeric(20,6)` | ไม่ได้ | — | — | จำนวนค้างส่งที่ปิดโดยไม่รอส่งต่อ; เลขทศนิยมแม่นยำ ส่ง API เป็น string ไม่คำนวณด้วย float |
| `created_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่สร้างแถวข้อมูลในระบบ; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `updated_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่แก้ไขแถวข้อมูลล่าสุด ต้องอัปเดตทุกช่องทางเขียน; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `version` | `integer` | ไม่ได้ | — | — | เลขรุ่นแถวสำหรับตรวจการแก้ไขพร้อมกัน |

**Keys / Index:** U(company_id,po_line_id)

**กฎเฉพาะ:** rebuildable; ค้าง=ordered-accepted-closed >=0; lock ก่อน confirm/close/revise; ไม่เก็บ stock

## `delivery.confirmations`

**เฟส:** P · **หนึ่งแถวคือ:** หนึ่งรอบส่งมอบหนึ่ง PO · **ประเภท:** mutable

**คำอธิบาย:** ตารางเก็บข้อมูล หนึ่งรอบส่งมอบหนึ่ง PO; หนึ่งแถวมีความหมายตามนี้และอยู่ในเฟส P

| คอลัมน์ | PostgreSQL type | NULL | PK / FK | อ้างอิง | คำอธิบายภาษาไทย |
|---|---|---|---|---|---|
| `id` | `uuid` | ไม่ได้ | PK | — | รหัสหลักภายในของแถวข้อมูล ไม่เปลี่ยนตลอดอายุรายการ; Primary Key ชนิด UUID ห้ามซ้ำหรือเป็น NULL |
| `company_id` | `uuid` | ไม่ได้ | FK | `org.companies.id` | รหัสอ้างอิงบริษัทเจ้าของข้อมูล ไปยัง org.companies.id (บทบาทฟิลด์ company_id) |
| `document_id` | `uuid` | ไม่ได้ | FK | `platform.documents.id` | รหัสอ้างอิง หนึ่งเอกสารธุรกิจที่เป็น FK กลาง ไปยัง platform.documents.id (บทบาทฟิลด์ document_id) |
| `po_id` | `uuid` | ไม่ได้ | FK | `purchasing.purchase_orders.id` | รหัสอ้างอิง หัว PO และตัวชี้รุ่นที่มีผล ไปยัง purchasing.purchase_orders.id (บทบาทฟิลด์ po_id) |
| `po_revision_id` | `uuid` | ไม่ได้ | FK | `purchasing.po_revisions.id` | รหัสอ้างอิง หนึ่งรุ่น PO snapshot ไปยัง purchasing.po_revisions.id (บทบาทฟิลด์ po_revision_id) |
| `supplier_delivery_no` | `text` | ได้ | — | — | เลขใบส่งสินค้าของผู้ขาย |
| `arrived_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่สินค้าส่งมาถึง; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `checked_by` | `uuid` | ได้ | FK | `security.users.id` | รหัสอ้างอิง หนึ่งตัวตนผู้ใช้กลาง ไปยัง security.users.id (บทบาทฟิลด์ checked_by) |
| `legacy_warehouse_state` | `text` | ไม่ได้ | — | — | สถานะการรับเข้าคลังที่อ้างอิงจากระบบเดิม |
| `note` | `text` | ได้ | — | — | หมายเหตุของรายการ |
| `created_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่สร้างแถวข้อมูลในระบบ; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `updated_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่แก้ไขแถวข้อมูลล่าสุด ต้องอัปเดตทุกช่องทางเขียน; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `version` | `integer` | ไม่ได้ | — | — | เลขรุ่นแถวสำหรับตรวจการแก้ไขพร้อมกัน |

**Keys / Index:** U(company_id,document_id); I(company_id,po_id,arrived_at)

**กฎเฉพาะ:** UNKNOWN/ALREADY_STOCKED/NOT_STOCKED; duplicate slip warning ไม่ unique แบบตัดหลายใบที่ใช้เลขเดียวกันโดยไม่ตรวจ

## `delivery.confirmation_lines`

**เฟส:** P · **หนึ่งแถวคือ:** ข้อเท็จจริงหนึ่งสินค้าต่อรอบส่ง · **ประเภท:** mutable

**คำอธิบาย:** ตารางเก็บข้อมูล ข้อเท็จจริงหนึ่งสินค้าต่อรอบส่ง; หนึ่งแถวมีความหมายตามนี้และอยู่ในเฟส P

| คอลัมน์ | PostgreSQL type | NULL | PK / FK | อ้างอิง | คำอธิบายภาษาไทย |
|---|---|---|---|---|---|
| `id` | `uuid` | ไม่ได้ | PK | — | รหัสหลักภายในของแถวข้อมูล ไม่เปลี่ยนตลอดอายุรายการ; Primary Key ชนิด UUID ห้ามซ้ำหรือเป็น NULL |
| `company_id` | `uuid` | ไม่ได้ | FK | `org.companies.id` | รหัสอ้างอิงบริษัทเจ้าของข้อมูล ไปยัง org.companies.id (บทบาทฟิลด์ company_id) |
| `document_line_id` | `uuid` | ไม่ได้ | FK | `platform.document_lines.id` | รหัสอ้างอิง หนึ่ง line identity ในเอกสาร ไปยัง platform.document_lines.id (บทบาทฟิลด์ document_line_id) |
| `confirmation_id` | `uuid` | ไม่ได้ | FK | `delivery.confirmations.id` | รหัสอ้างอิง หนึ่งรอบส่งมอบหนึ่ง PO ไปยัง delivery.confirmations.id (บทบาทฟิลด์ confirmation_id) |
| `po_revision_line_id` | `uuid` | ไม่ได้ | FK | `purchasing.po_revision_lines.id` | รหัสอ้างอิง หนึ่ง line snapshot ต่อ revision ไปยัง purchasing.po_revision_lines.id (บทบาทฟิลด์ po_revision_line_id) |
| `stated_order_qty` | `numeric(20,6)` | ไม่ได้ | — | — | จำนวนที่ผู้ส่งระบุตามหน่วยสั่งซื้อ; เลขทศนิยมแม่นยำ ส่ง API เป็น string ไม่คำนวณด้วย float |
| `observed_order_qty` | `numeric(20,6)` | ไม่ได้ | — | — | จำนวนที่พบจริงตามหน่วยสั่งซื้อ; เลขทศนิยมแม่นยำ ส่ง API เป็น string ไม่คำนวณด้วย float |
| `document_weight_kg` | `numeric(20,6)` | ได้ | — | — | น้ำหนักตามเอกสาร หน่วยกิโลกรัม; เลขทศนิยมแม่นยำ ส่ง API เป็น string ไม่คำนวณด้วย float |
| `document_unit_price` | `numeric(20,6)` | ได้ | — | — | ราคาต่อหน่วยตามเอกสารที่ใช้ตรวจเทียบ; เลขทศนิยมแม่นยำ ส่ง API เป็น string ไม่คำนวณด้วย float |
| `unit_snapshot` | `jsonb` | ไม่ได้ | — | — | สำเนาข้อมูลหน่วย ณ เวลาทำรายการ; ต้องตรวจ schema และจำกัดข้อมูลตามสิทธิ์ |
| `observed_note` | `text` | ได้ | — | — | หมายเหตุสิ่งที่พบจริง |
| `created_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่สร้างแถวข้อมูลในระบบ; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `updated_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่แก้ไขแถวข้อมูลล่าสุด ต้องอัปเดตทุกช่องทางเขียน; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `version` | `integer` | ไม่ได้ | — | — | เลขรุ่นแถวสำหรับตรวจการแก้ไขพร้อมกัน |

**Keys / Index:** U(company_id,document_line_id)

**กฎเฉพาะ:** confirmed facts immutable; accepted/issues แยก ledger; observed excess เก็บได้แต่ยังไม่ accepted

## `delivery.issues`

**เฟส:** P · **หนึ่งแถวคือ:** หนึ่งปัญหา/ส่วนที่กันไว้ของรอบส่ง · **ประเภท:** mutable

**คำอธิบาย:** ตารางเก็บข้อมูล หนึ่งปัญหา/ส่วนที่กันไว้ของรอบส่ง; หนึ่งแถวมีความหมายตามนี้และอยู่ในเฟส P

| คอลัมน์ | PostgreSQL type | NULL | PK / FK | อ้างอิง | คำอธิบายภาษาไทย |
|---|---|---|---|---|---|
| `id` | `uuid` | ไม่ได้ | PK | — | รหัสหลักภายในของแถวข้อมูล ไม่เปลี่ยนตลอดอายุรายการ; Primary Key ชนิด UUID ห้ามซ้ำหรือเป็น NULL |
| `company_id` | `uuid` | ไม่ได้ | FK | `org.companies.id` | รหัสอ้างอิงบริษัทเจ้าของข้อมูล ไปยัง org.companies.id (บทบาทฟิลด์ company_id) |
| `confirmation_line_id` | `uuid` | ไม่ได้ | FK | `delivery.confirmation_lines.id` | รหัสอ้างอิง ข้อเท็จจริงหนึ่งสินค้าต่อรอบส่ง ไปยัง delivery.confirmation_lines.id (บทบาทฟิลด์ confirmation_line_id) |
| `kind` | `text` | ไม่ได้ | — | — | ชนิดรายการตามค่าที่อนุญาตของตาราง |
| `affected_order_qty` | `numeric(20,6)` | ไม่ได้ | — | — | จำนวนตามหน่วยสั่งซื้อที่ได้รับผลกระทบจากปัญหา; เลขทศนิยมแม่นยำ ส่ง API เป็น string ไม่คำนวณด้วย float |
| `status` | `text` | ไม่ได้ | — | — | สถานะรายการตาม state machine ของตาราง |
| `assigned_to` | `uuid` | ได้ | FK | `security.users.id` | รหัสอ้างอิง หนึ่งตัวตนผู้ใช้กลาง ไปยัง security.users.id (บทบาทฟิลด์ assigned_to) |
| `reason` | `text` | ไม่ได้ | — | — | เหตุผลประกอบการดำเนินการ |
| `evidence_file_id` | `uuid` | ได้ | FK | `platform.files.id` | รหัสอ้างอิง หนึ่ง object ส่วนตัว ไปยัง platform.files.id (บทบาทฟิลด์ evidence_file_id) |
| `created_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่สร้างแถวข้อมูลในระบบ; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `updated_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่แก้ไขแถวข้อมูลล่าสุด ต้องอัปเดตทุกช่องทางเขียน; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `version` | `integer` | ไม่ได้ | — | — | เลขรุ่นแถวสำหรับตรวจการแก้ไขพร้อมกัน |

**Keys / Index:** I(company_id,status,created_at)

**กฎเฉพาะ:** SHORT/EXCESS/DAMAGED/WRONG_ITEM/PRICE/UNIT; ไม่เพิ่ม qty โดยปิด issue เฉย ๆ

## `delivery.acceptance_entries`

**เฟส:** P · **หนึ่งแถวคือ:** หนึ่งรายการยืนยัน/ย้อนจำนวนที่ยอมรับ · **ประเภท:** append

**คำอธิบาย:** ตารางเก็บข้อมูล หนึ่งรายการยืนยัน/ย้อนจำนวนที่ยอมรับ; หนึ่งแถวมีความหมายตามนี้และอยู่ในเฟส P

| คอลัมน์ | PostgreSQL type | NULL | PK / FK | อ้างอิง | คำอธิบายภาษาไทย |
|---|---|---|---|---|---|
| `id` | `uuid` | ไม่ได้ | PK | — | รหัสหลักภายในของแถวข้อมูล ไม่เปลี่ยนตลอดอายุรายการ; Primary Key ชนิด UUID ห้ามซ้ำหรือเป็น NULL |
| `company_id` | `uuid` | ไม่ได้ | FK | `org.companies.id` | รหัสอ้างอิงบริษัทเจ้าของข้อมูล ไปยัง org.companies.id (บทบาทฟิลด์ company_id) |
| `confirmation_line_id` | `uuid` | ไม่ได้ | FK | `delivery.confirmation_lines.id` | รหัสอ้างอิง ข้อเท็จจริงหนึ่งสินค้าต่อรอบส่ง ไปยัง delivery.confirmation_lines.id (บทบาทฟิลด์ confirmation_line_id) |
| `issue_id` | `uuid` | ได้ | FK | `delivery.issues.id` | รหัสอ้างอิง หนึ่งปัญหา/ส่วนที่กันไว้ของรอบส่ง ไปยัง delivery.issues.id (บทบาทฟิลด์ issue_id) |
| `action` | `text` | ไม่ได้ | — | — | การกระทำที่บันทึก |
| `order_qty` | `numeric(20,6)` | ไม่ได้ | — | — | จำนวนตามหน่วยสั่งซื้อ; เลขทศนิยมแม่นยำ ส่ง API เป็น string ไม่คำนวณด้วย float |
| `reverses_id` | `uuid` | ได้ | FK | `delivery.acceptance_entries.id` | รหัสอ้างอิง หนึ่งรายการยืนยัน/ย้อนจำนวนที่ยอมรับ ไปยัง delivery.acceptance_entries.id (บทบาทฟิลด์ reverses_id) |
| `confirmed_by` | `uuid` | ไม่ได้ | FK | `security.users.id` | รหัสอ้างอิงผู้ยืนยัน ไปยัง security.users.id (บทบาทฟิลด์ confirmed_by) |
| `confirmed_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่ผู้มีสิทธิ์ยืนยันรายการ; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `reason` | `text` | ได้ | — | — | เหตุผลประกอบการดำเนินการ |
| `settings_snapshot` | `jsonb` | ไม่ได้ | — | — | สำเนาการตั้งค่า ณ เวลาดำเนินการ; ต้องตรวจ schema และจำกัดข้อมูลตามสิทธิ์ |
| `created_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่สร้างแถวข้อมูลในระบบ; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |

**Keys / Index:** I(company_id,confirmation_line_id); U(company_id,id)

**กฎเฉพาะ:** ACCEPT/REVERSE qty>0; ยอมรับสุทธิ <=observed ที่แก้ตรวจแล้ว; ไม่สร้าง stock; reverse ไม่เกิน unused downstream

## `delivery.issue_actions`

**เฟส:** P · **หนึ่งแถวคือ:** หนึ่งการดำเนินการปัญหา · **ประเภท:** append

**คำอธิบาย:** ตารางเก็บข้อมูล หนึ่งการดำเนินการปัญหา; หนึ่งแถวมีความหมายตามนี้และอยู่ในเฟส P

| คอลัมน์ | PostgreSQL type | NULL | PK / FK | อ้างอิง | คำอธิบายภาษาไทย |
|---|---|---|---|---|---|
| `id` | `uuid` | ไม่ได้ | PK | — | รหัสหลักภายในของแถวข้อมูล ไม่เปลี่ยนตลอดอายุรายการ; Primary Key ชนิด UUID ห้ามซ้ำหรือเป็น NULL |
| `company_id` | `uuid` | ไม่ได้ | FK | `org.companies.id` | รหัสอ้างอิงบริษัทเจ้าของข้อมูล ไปยัง org.companies.id (บทบาทฟิลด์ company_id) |
| `issue_id` | `uuid` | ไม่ได้ | FK | `delivery.issues.id` | รหัสอ้างอิง หนึ่งปัญหา/ส่วนที่กันไว้ของรอบส่ง ไปยัง delivery.issues.id (บทบาทฟิลด์ issue_id) |
| `action` | `text` | ไม่ได้ | — | — | การกระทำที่บันทึก |
| `order_qty` | `numeric(20,6)` | ได้ | — | — | จำนวนตามหน่วยสั่งซื้อ; เลขทศนิยมแม่นยำ ส่ง API เป็น string ไม่คำนวณด้วย float |
| `acceptance_entry_id` | `uuid` | ได้ | FK | `delivery.acceptance_entries.id` | รหัสอ้างอิง หนึ่งรายการยืนยัน/ย้อนจำนวนที่ยอมรับ ไปยัง delivery.acceptance_entries.id (บทบาทฟิลด์ acceptance_entry_id) |
| `closure_id` | `uuid` | ได้ | FK | `purchasing.po_closures.id` | รหัสอ้างอิง หนึ่งปิด/เปิดค้างรายบรรทัด ไปยัง purchasing.po_closures.id (บทบาทฟิลด์ closure_id) |
| `actor_id` | `uuid` | ไม่ได้ | FK | `security.users.id` | รหัสอ้างอิงผู้ดำเนินการ ไปยัง security.users.id (บทบาทฟิลด์ actor_id) |
| `note` | `text` | ไม่ได้ | — | — | หมายเหตุของรายการ |
| `created_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่สร้างแถวข้อมูลในระบบ; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |

**Keys / Index:** I(company_id,issue_id)

**กฎเฉพาะ:** ACCEPT_EXISTING/CLOSE_OUTSTANDING/REPLACEMENT/REJECT; replacement ใหม่สร้าง confirmation ใหม่

## `delivery.line_progress`

**เฟส:** P · **หนึ่งแถวคือ:** projection ยอดพร้อมเข้าคลังต่อ confirmation line · **ประเภท:** mutable

**คำอธิบาย:** ตารางเก็บข้อมูล projection ยอดพร้อมเข้าคลังต่อ confirmation line; หนึ่งแถวมีความหมายตามนี้และอยู่ในเฟส P

| คอลัมน์ | PostgreSQL type | NULL | PK / FK | อ้างอิง | คำอธิบายภาษาไทย |
|---|---|---|---|---|---|
| `id` | `uuid` | ไม่ได้ | PK | — | รหัสหลักภายในของแถวข้อมูล ไม่เปลี่ยนตลอดอายุรายการ; Primary Key ชนิด UUID ห้ามซ้ำหรือเป็น NULL |
| `company_id` | `uuid` | ไม่ได้ | FK | `org.companies.id` | รหัสอ้างอิงบริษัทเจ้าของข้อมูล ไปยัง org.companies.id (บทบาทฟิลด์ company_id) |
| `confirmation_line_id` | `uuid` | ไม่ได้ | FK | `delivery.confirmation_lines.id` | รหัสอ้างอิง ข้อเท็จจริงหนึ่งสินค้าต่อรอบส่ง ไปยัง delivery.confirmation_lines.id (บทบาทฟิลด์ confirmation_line_id) |
| `accepted_order_qty` | `numeric(20,6)` | ไม่ได้ | — | — | จำนวนที่ยอมรับตามหน่วยสั่งซื้อ; เลขทศนิยมแม่นยำ ส่ง API เป็น string ไม่คำนวณด้วย float |
| `warehouse_consumed_order_qty` | `numeric(20,6)` | ไม่ได้ | — | — | จำนวนหน่วยสั่งซื้อที่ใช้จัดสรรรับเข้าคลังแล้ว; เลขทศนิยมแม่นยำ ส่ง API เป็น string ไม่คำนวณด้วย float |
| `terminal_order_qty` | `numeric(20,6)` | ไม่ได้ | — | — | จำนวนตามหน่วยสั่งซื้อที่สิ้นสุดกระบวนการโดยไม่เข้าคลัง; เลขทศนิยมแม่นยำ ส่ง API เป็น string ไม่คำนวณด้วย float |
| `created_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่สร้างแถวข้อมูลในระบบ; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `updated_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่แก้ไขแถวข้อมูลล่าสุด ต้องอัปเดตทุกช่องทางเขียน; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `version` | `integer` | ไม่ได้ | — | — | เลขรุ่นแถวสำหรับตรวจการแก้ไขพร้อมกัน |

**Keys / Index:** U(company_id,confirmation_line_id)

**กฎเฉพาะ:** ready=accepted-consumed-terminal >=0; ไม่รวม failed/issues; warehouse counters เริ่มศูนย์และไม่ใช่ stock

## `delivery.terminal_resolutions`

**เฟส:** W · **หนึ่งแถวคือ:** จำนวนที่ยืนยันแล้วแต่ยุติการเข้าคลัง · **ประเภท:** append

**คำอธิบาย:** ตารางเก็บข้อมูล จำนวนที่ยืนยันแล้วแต่ยุติการเข้าคลัง; หนึ่งแถวมีความหมายตามนี้และอยู่ในเฟส W

| คอลัมน์ | PostgreSQL type | NULL | PK / FK | อ้างอิง | คำอธิบายภาษาไทย |
|---|---|---|---|---|---|
| `id` | `uuid` | ไม่ได้ | PK | — | รหัสหลักภายในของแถวข้อมูล ไม่เปลี่ยนตลอดอายุรายการ; Primary Key ชนิด UUID ห้ามซ้ำหรือเป็น NULL |
| `company_id` | `uuid` | ไม่ได้ | FK | `org.companies.id` | รหัสอ้างอิงบริษัทเจ้าของข้อมูล ไปยัง org.companies.id (บทบาทฟิลด์ company_id) |
| `confirmation_line_id` | `uuid` | ไม่ได้ | FK | `delivery.confirmation_lines.id` | รหัสอ้างอิง ข้อเท็จจริงหนึ่งสินค้าต่อรอบส่ง ไปยัง delivery.confirmation_lines.id (บทบาทฟิลด์ confirmation_line_id) |
| `document_id` | `uuid` | ไม่ได้ | FK | `platform.documents.id` | รหัสอ้างอิง หนึ่งเอกสารธุรกิจที่เป็น FK กลาง ไปยัง platform.documents.id (บทบาทฟิลด์ document_id) |
| `order_qty` | `numeric(20,6)` | ไม่ได้ | — | — | จำนวนตามหน่วยสั่งซื้อ; เลขทศนิยมแม่นยำ ส่ง API เป็น string ไม่คำนวณด้วย float |
| `reason` | `text` | ไม่ได้ | — | — | เหตุผลประกอบการดำเนินการ |
| `approval_request_id` | `uuid` | ไม่ได้ | FK | `platform.approval_requests.id` | รหัสอ้างอิง หนึ่งคำขออนุมัติ snapshot ไปยัง platform.approval_requests.id (บทบาทฟิลด์ approval_request_id) |
| `reverses_id` | `uuid` | ได้ | FK | `delivery.terminal_resolutions.id` | รหัสอ้างอิง จำนวนที่ยืนยันแล้วแต่ยุติการเข้าคลัง ไปยัง delivery.terminal_resolutions.id (บทบาทฟิลด์ reverses_id) |
| `created_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่สร้างแถวข้อมูลในระบบ; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |

**Keys / Index:** I(company_id,confirmation_line_id)

**กฎเฉพาะ:** ใช้กับสูญเสีย/ปฏิเสธหลังยืนยันและก่อน stock; ส่งผล claim แต่ไม่เปิด PO ใหม่อัตโนมัติ

## `devices.agents`

**เฟส:** W · **หนึ่งแถวคือ:** หนึ่งเครื่อง Device Agent · **ประเภท:** mutable

**คำอธิบาย:** ตารางเก็บข้อมูล หนึ่งเครื่อง Device Agent; หนึ่งแถวมีความหมายตามนี้และอยู่ในเฟส W

| คอลัมน์ | PostgreSQL type | NULL | PK / FK | อ้างอิง | คำอธิบายภาษาไทย |
|---|---|---|---|---|---|
| `id` | `uuid` | ไม่ได้ | PK | — | รหัสหลักภายในของแถวข้อมูล ไม่เปลี่ยนตลอดอายุรายการ; Primary Key ชนิด UUID ห้ามซ้ำหรือเป็น NULL |
| `company_id` | `uuid` | ไม่ได้ | FK | `org.companies.id` | รหัสอ้างอิงบริษัทเจ้าของข้อมูล ไปยัง org.companies.id (บทบาทฟิลด์ company_id) |
| `branch_id` | `uuid` | ไม่ได้ | FK | `org.branches.id` | รหัสอ้างอิงสาขาเจ้าของรายการ ไปยัง org.branches.id (บทบาทฟิลด์ branch_id) |
| `name` | `text` | ไม่ได้ | — | — | ชื่อรายการสำหรับแสดงผล |
| `credential_hash` | `text` | ไม่ได้ | — | — | ค่าแฮชข้อมูลยืนยันตัวอุปกรณ์ ห้ามเปิดเผยผ่าน API |
| `credential_version` | `integer` | ไม่ได้ | — | — | รุ่นของข้อมูลยืนยันตัวอุปกรณ์ |
| `active` | `boolean` | ไม่ได้ | — | — | สถานะเปิดใช้งาน |
| `last_heartbeat_at` | `timestamptz` | ได้ | — | — | เวลาที่อุปกรณ์แจ้งสถานะล่าสุด; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `created_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่สร้างแถวข้อมูลในระบบ; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `updated_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่แก้ไขแถวข้อมูลล่าสุด ต้องอัปเดตทุกช่องทางเขียน; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `version` | `integer` | ไม่ได้ | — | — | เลขรุ่นแถวสำหรับตรวจการแก้ไขพร้อมกัน |

**Keys / Index:** U(company_id,name)

**กฎเฉพาะ:** secret เก็บ hash/secret reference ไม่ plaintext

## `devices.devices`

**เฟส:** W · **หนึ่งแถวคือ:** หนึ่งเครื่องชั่ง/เครื่องพิมพ์ · **ประเภท:** mutable

**คำอธิบาย:** ตารางเก็บข้อมูล หนึ่งเครื่องชั่ง/เครื่องพิมพ์; หนึ่งแถวมีความหมายตามนี้และอยู่ในเฟส W

| คอลัมน์ | PostgreSQL type | NULL | PK / FK | อ้างอิง | คำอธิบายภาษาไทย |
|---|---|---|---|---|---|
| `id` | `uuid` | ไม่ได้ | PK | — | รหัสหลักภายในของแถวข้อมูล ไม่เปลี่ยนตลอดอายุรายการ; Primary Key ชนิด UUID ห้ามซ้ำหรือเป็น NULL |
| `company_id` | `uuid` | ไม่ได้ | FK | `org.companies.id` | รหัสอ้างอิงบริษัทเจ้าของข้อมูล ไปยัง org.companies.id (บทบาทฟิลด์ company_id) |
| `agent_id` | `uuid` | ไม่ได้ | FK | `devices.agents.id` | รหัสอ้างอิง หนึ่งเครื่อง Device Agent ไปยัง devices.agents.id (บทบาทฟิลด์ agent_id) |
| `warehouse_id` | `uuid` | ไม่ได้ | FK | `org.warehouses.id` | รหัสอ้างอิงคลังที่เกี่ยวข้อง ไปยัง org.warehouses.id (บทบาทฟิลด์ warehouse_id) |
| `kind` | `text` | ไม่ได้ | — | — | ชนิดรายการตามค่าที่อนุญาตของตาราง |
| `serial_no` | `text` | ไม่ได้ | — | — | หมายเลขประจำอุปกรณ์ |
| `model` | `text` | ไม่ได้ | — | — | รุ่นอุปกรณ์ |
| `protocol` | `text` | ไม่ได้ | — | — | รูปแบบการสื่อสารอุปกรณ์ |
| `active` | `boolean` | ไม่ได้ | — | — | สถานะเปิดใช้งาน |
| `calibrated_at` | `timestamptz` | ได้ | — | — | เวลาที่สอบเทียบอุปกรณ์ล่าสุด; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `created_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่สร้างแถวข้อมูลในระบบ; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `updated_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่แก้ไขแถวข้อมูลล่าสุด ต้องอัปเดตทุกช่องทางเขียน; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `version` | `integer` | ไม่ได้ | — | — | เลขรุ่นแถวสำหรับตรวจการแก้ไขพร้อมกัน |

**Keys / Index:** U(company_id,serial_no)

**กฎเฉพาะ:** SCALE/PRINTER; scope branch ตรง agent

## `devices.weighings`

**เฟส:** W · **หนึ่งแถวคือ:** หนึ่ง stable measurement หรือ authorized manual reading · **ประเภท:** append

**คำอธิบาย:** ตารางเก็บข้อมูล หนึ่ง stable measurement หรือ authorized manual reading; หนึ่งแถวมีความหมายตามนี้และอยู่ในเฟส W

| คอลัมน์ | PostgreSQL type | NULL | PK / FK | อ้างอิง | คำอธิบายภาษาไทย |
|---|---|---|---|---|---|
| `id` | `uuid` | ไม่ได้ | PK | — | รหัสหลักภายในของแถวข้อมูล ไม่เปลี่ยนตลอดอายุรายการ; Primary Key ชนิด UUID ห้ามซ้ำหรือเป็น NULL |
| `company_id` | `uuid` | ไม่ได้ | FK | `org.companies.id` | รหัสอ้างอิงบริษัทเจ้าของข้อมูล ไปยัง org.companies.id (บทบาทฟิลด์ company_id) |
| `device_id` | `uuid` | ได้ | FK | `devices.devices.id` | รหัสอ้างอิง หนึ่งเครื่องชั่ง/เครื่องพิมพ์ ไปยัง devices.devices.id (บทบาทฟิลด์ device_id) |
| `agent_event_id` | `text` | ได้ | — | — | รหัสเหตุการณ์จากโปรแกรมประจำเครื่อง ใช้ป้องกันข้อมูลซ้ำ |
| `source` | `text` | ไม่ได้ | — | — | แหล่งกำเนิดข้อมูล |
| `gross_kg` | `numeric(20,6)` | ไม่ได้ | — | — | น้ำหนักรวมภาชนะ หน่วยกิโลกรัม; เลขทศนิยมแม่นยำ ส่ง API เป็น string ไม่คำนวณด้วย float |
| `tare_kg` | `numeric(20,6)` | ไม่ได้ | — | — | น้ำหนักภาชนะที่หักออก หน่วยกิโลกรัม; เลขทศนิยมแม่นยำ ส่ง API เป็น string ไม่คำนวณด้วย float |
| `net_kg` | `numeric(20,6)` | ไม่ได้ | — | — | น้ำหนักสุทธิหลังหักภาชนะ หน่วยกิโลกรัม; เลขทศนิยมแม่นยำ ส่ง API เป็น string ไม่คำนวณด้วย float |
| `stable` | `boolean` | ไม่ได้ | — | — | ระบุว่าค่าน้ำหนักนิ่งตามเกณฑ์อุปกรณ์ |
| `observed_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่พบหรือบันทึกเหตุการณ์ต้นทาง; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `received_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่รับตามกระบวนการของตาราง ไม่ถือว่าสต็อกเพิ่มจนกว่าจะ post; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `operator_id` | `uuid` | ไม่ได้ | FK | `security.users.id` | รหัสอ้างอิง หนึ่งตัวตนผู้ใช้กลาง ไปยัง security.users.id (บทบาทฟิลด์ operator_id) |
| `manual_reason` | `text` | ได้ | — | — | เหตุผลที่กรอกหรือแก้ด้วยมือ |
| `override_approval_request_id` | `uuid` | ได้ | FK | `platform.approval_requests.id` | รหัสอ้างอิง หนึ่งคำขออนุมัติ snapshot ไปยัง platform.approval_requests.id (บทบาทฟิลด์ override_approval_request_id) |
| `raw_payload` | `jsonb` | ได้ | — | — | ข้อมูลดิบจากอุปกรณ์หรือระบบต้นทาง; ต้องตรวจ schema และจำกัดข้อมูลตามสิทธิ์ |
| `created_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่สร้างแถวข้อมูลในระบบ; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |

**Keys / Index:** partial U(company_id,device_id,agent_event_id) WHERE device_id IS NOT NULL

**กฎเฉพาะ:** net=gross-tare >=0; stable required except explicit manual override; scope and replay/staleness checked

## `receiving.receipts`

**เฟส:** W · **หนึ่งแถวคือ:** หนึ่งใบชั่งรับเข้าคลัง · **ประเภท:** mutable

**คำอธิบาย:** ตารางเก็บข้อมูล หนึ่งใบชั่งรับเข้าคลัง; หนึ่งแถวมีความหมายตามนี้และอยู่ในเฟส W

| คอลัมน์ | PostgreSQL type | NULL | PK / FK | อ้างอิง | คำอธิบายภาษาไทย |
|---|---|---|---|---|---|
| `id` | `uuid` | ไม่ได้ | PK | — | รหัสหลักภายในของแถวข้อมูล ไม่เปลี่ยนตลอดอายุรายการ; Primary Key ชนิด UUID ห้ามซ้ำหรือเป็น NULL |
| `company_id` | `uuid` | ไม่ได้ | FK | `org.companies.id` | รหัสอ้างอิงบริษัทเจ้าของข้อมูล ไปยัง org.companies.id (บทบาทฟิลด์ company_id) |
| `document_id` | `uuid` | ไม่ได้ | FK | `platform.documents.id` | รหัสอ้างอิง หนึ่งเอกสารธุรกิจที่เป็น FK กลาง ไปยัง platform.documents.id (บทบาทฟิลด์ document_id) |
| `warehouse_id` | `uuid` | ไม่ได้ | FK | `org.warehouses.id` | รหัสอ้างอิงคลังที่เกี่ยวข้อง ไปยัง org.warehouses.id (บทบาทฟิลด์ warehouse_id) |
| `confirmation_id` | `uuid` | ไม่ได้ | FK | `delivery.confirmations.id` | รหัสอ้างอิง หนึ่งรอบส่งมอบหนึ่ง PO ไปยัง delivery.confirmations.id (บทบาทฟิลด์ confirmation_id) |
| `received_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่รับตามกระบวนการของตาราง ไม่ถือว่าสต็อกเพิ่มจนกว่าจะ post; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `posted_at` | `timestamptz` | ได้ | — | — | เวลาที่ลงรายการบัญชีสต็อกสำเร็จ; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `settings_snapshot` | `jsonb` | ไม่ได้ | — | — | สำเนาการตั้งค่า ณ เวลาดำเนินการ; ต้องตรวจ schema และจำกัดข้อมูลตามสิทธิ์ |
| `created_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่สร้างแถวข้อมูลในระบบ; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `updated_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่แก้ไขแถวข้อมูลล่าสุด ต้องอัปเดตทุกช่องทางเขียน; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `version` | `integer` | ไม่ได้ | — | — | เลขรุ่นแถวสำหรับตรวจการแก้ไขพร้อมกัน |

**Keys / Index:** U(company_id,document_id)

**กฎเฉพาะ:** warehouse branch ตรง confirmation/PO; ไม่สร้างตรงจาก PO ข้าม delivery gate

## `receiving.receipt_lines`

**เฟส:** W · **หนึ่งแถวคือ:** หนึ่งรายละเอียดชั่งรับสินค้า · **ประเภท:** mutable

**คำอธิบาย:** ตารางเก็บข้อมูล หนึ่งรายละเอียดชั่งรับสินค้า; หนึ่งแถวมีความหมายตามนี้และอยู่ในเฟส W

| คอลัมน์ | PostgreSQL type | NULL | PK / FK | อ้างอิง | คำอธิบายภาษาไทย |
|---|---|---|---|---|---|
| `id` | `uuid` | ไม่ได้ | PK | — | รหัสหลักภายในของแถวข้อมูล ไม่เปลี่ยนตลอดอายุรายการ; Primary Key ชนิด UUID ห้ามซ้ำหรือเป็น NULL |
| `company_id` | `uuid` | ไม่ได้ | FK | `org.companies.id` | รหัสอ้างอิงบริษัทเจ้าของข้อมูล ไปยัง org.companies.id (บทบาทฟิลด์ company_id) |
| `document_line_id` | `uuid` | ไม่ได้ | FK | `platform.document_lines.id` | รหัสอ้างอิง หนึ่ง line identity ในเอกสาร ไปยัง platform.document_lines.id (บทบาทฟิลด์ document_line_id) |
| `receipt_id` | `uuid` | ไม่ได้ | FK | `receiving.receipts.id` | รหัสอ้างอิง หนึ่งใบชั่งรับเข้าคลัง ไปยัง receiving.receipts.id (บทบาทฟิลด์ receipt_id) |
| `confirmation_line_id` | `uuid` | ไม่ได้ | FK | `delivery.confirmation_lines.id` | รหัสอ้างอิง ข้อเท็จจริงหนึ่งสินค้าต่อรอบส่ง ไปยัง delivery.confirmation_lines.id (บทบาทฟิลด์ confirmation_line_id) |
| `product_id` | `uuid` | ไม่ได้ | FK | `catalog.products.id` | รหัสอ้างอิงสินค้าในรายการ ไปยัง catalog.products.id (บทบาทฟิลด์ product_id) |
| `accepted_order_qty_used` | `numeric(20,6)` | ไม่ได้ | — | — | จำนวนที่ยอมรับซึ่งถูกใช้ไปแล้วตามหน่วยสั่งซื้อ; เลขทศนิยมแม่นยำ ส่ง API เป็น string ไม่คำนวณด้วย float |
| `stock_qty` | `numeric(20,6)` | ไม่ได้ | — | — | จำนวนในหน่วยสต็อกของสินค้า; เลขทศนิยมแม่นยำ ส่ง API เป็น string ไม่คำนวณด้วย float |
| `net_weight_kg` | `numeric(20,6)` | ได้ | — | — | น้ำหนักสุทธิ หน่วยกิโลกรัม; เลขทศนิยมแม่นยำ ส่ง API เป็น string ไม่คำนวณด้วย float |
| `price_basis` | `text` | ไม่ได้ | — | — | ฐานหน่วยที่ใช้คิดราคา |
| `unit_price` | `numeric(20,6)` | ไม่ได้ | — | — | ราคาต่อหน่วยตามหน่วยและสกุลเงินในรายการ; เลขทศนิยมแม่นยำ ส่ง API เป็น string ไม่คำนวณด้วย float |
| `net_amount` | `numeric(20,2)` | ไม่ได้ | — | — | จำนวนเงินสุทธิตามสูตรเอกสาร; เลขทศนิยมแม่นยำ ส่ง API เป็น string ไม่คำนวณด้วย float |
| `tax_amount` | `numeric(20,2)` | ไม่ได้ | — | — | จำนวนเงินภาษี; เลขทศนิยมแม่นยำ ส่ง API เป็น string ไม่คำนวณด้วย float |
| `inventory_value` | `numeric(20,6)` | ไม่ได้ | — | — | มูลค่าสินค้าคงเหลือ; เลขทศนิยมแม่นยำ ส่ง API เป็น string ไม่คำนวณด้วย float |
| `conversion_snapshot` | `jsonb` | ไม่ได้ | — | — | สำเนากฎแปลงหน่วย ณ เวลาทำรายการ; ต้องตรวจ schema และจำกัดข้อมูลตามสิทธิ์ |
| `quality_status` | `text` | ไม่ได้ | — | — | สถานะคุณภาพสินค้าตามค่าที่อนุญาต |
| `created_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่สร้างแถวข้อมูลในระบบ; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `updated_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่แก้ไขแถวข้อมูลล่าสุด ต้องอัปเดตทุกช่องทางเขียน; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `version` | `integer` | ไม่ได้ | — | — | เลขรุ่นแถวสำหรับตรวจการแก้ไขพร้อมกัน |

**Keys / Index:** U(company_id,document_line_id)

**กฎเฉพาะ:** consume order units vs measured stock units independent; nonnegative; exact record final warehouse facts

## `receiving.receipt_weighings`

**เฟส:** W · **หนึ่งแถวคือ:** หนึ่ง measurement ที่ใช้ใน line · **ประเภท:** mutable

**คำอธิบาย:** ตารางเก็บข้อมูล หนึ่ง measurement ที่ใช้ใน line; หนึ่งแถวมีความหมายตามนี้และอยู่ในเฟส W

| คอลัมน์ | PostgreSQL type | NULL | PK / FK | อ้างอิง | คำอธิบายภาษาไทย |
|---|---|---|---|---|---|
| `id` | `uuid` | ไม่ได้ | PK | — | รหัสหลักภายในของแถวข้อมูล ไม่เปลี่ยนตลอดอายุรายการ; Primary Key ชนิด UUID ห้ามซ้ำหรือเป็น NULL |
| `company_id` | `uuid` | ไม่ได้ | FK | `org.companies.id` | รหัสอ้างอิงบริษัทเจ้าของข้อมูล ไปยัง org.companies.id (บทบาทฟิลด์ company_id) |
| `receipt_line_id` | `uuid` | ไม่ได้ | FK | `receiving.receipt_lines.id` | รหัสอ้างอิง หนึ่งรายละเอียดชั่งรับสินค้า ไปยัง receiving.receipt_lines.id (บทบาทฟิลด์ receipt_line_id) |
| `weighing_id` | `uuid` | ไม่ได้ | FK | `devices.weighings.id` | รหัสอ้างอิง หนึ่ง stable measurement หรือ authorized manual reading ไปยัง devices.weighings.id (บทบาทฟิลด์ weighing_id) |
| `created_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่สร้างแถวข้อมูลในระบบ; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `updated_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่แก้ไขแถวข้อมูลล่าสุด ต้องอัปเดตทุกช่องทางเขียน; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `version` | `integer` | ไม่ได้ | — | — | เลขรุ่นแถวสำหรับตรวจการแก้ไขพร้อมกัน |

**Keys / Index:** U(company_id,weighing_id)

**กฎเฉพาะ:** ไม่ reuse measurement ใน receipt ใหม่; reversal เก็บ mapping เดิม

## `receiving.receipt_lots`

**เฟส:** W · **หนึ่งแถวคือ:** หนึ่งการแบ่ง line เข้า lot/package/location · **ประเภท:** mutable

**คำอธิบาย:** ตารางเก็บข้อมูล หนึ่งการแบ่ง line เข้า lot/package/location; หนึ่งแถวมีความหมายตามนี้และอยู่ในเฟส W

| คอลัมน์ | PostgreSQL type | NULL | PK / FK | อ้างอิง | คำอธิบายภาษาไทย |
|---|---|---|---|---|---|
| `id` | `uuid` | ไม่ได้ | PK | — | รหัสหลักภายในของแถวข้อมูล ไม่เปลี่ยนตลอดอายุรายการ; Primary Key ชนิด UUID ห้ามซ้ำหรือเป็น NULL |
| `company_id` | `uuid` | ไม่ได้ | FK | `org.companies.id` | รหัสอ้างอิงบริษัทเจ้าของข้อมูล ไปยัง org.companies.id (บทบาทฟิลด์ company_id) |
| `receipt_line_id` | `uuid` | ไม่ได้ | FK | `receiving.receipt_lines.id` | รหัสอ้างอิง หนึ่งรายละเอียดชั่งรับสินค้า ไปยัง receiving.receipt_lines.id (บทบาทฟิลด์ receipt_line_id) |
| `lot_id` | `uuid` | ไม่ได้ | FK | `inventory.lots.id` | รหัสอ้างอิง หนึ่ง lot คุณภาพ/อายุเดียวกัน ไปยัง inventory.lots.id (บทบาทฟิลด์ lot_id) |
| `package_id` | `uuid` | ได้ | FK | `inventory.packages.id` | รหัสอ้างอิง หนึ่งหน่วยห่อ/ภาชนะที่ trace ได้ ไปยัง inventory.packages.id (บทบาทฟิลด์ package_id) |
| `location_id` | `uuid` | ไม่ได้ | FK | `org.locations.id` | รหัสอ้างอิง หนึ่งโหนดสถานที่จริง ไปยัง org.locations.id (บทบาทฟิลด์ location_id) |
| `stock_qty` | `numeric(20,6)` | ไม่ได้ | — | — | จำนวนในหน่วยสต็อกของสินค้า; เลขทศนิยมแม่นยำ ส่ง API เป็น string ไม่คำนวณด้วย float |
| `weight_kg` | `numeric(20,6)` | ได้ | — | — | น้ำหนัก หน่วยกิโลกรัม; เลขทศนิยมแม่นยำ ส่ง API เป็น string ไม่คำนวณด้วย float |
| `inventory_value` | `numeric(20,6)` | ไม่ได้ | — | — | มูลค่าสินค้าคงเหลือ; เลขทศนิยมแม่นยำ ส่ง API เป็น string ไม่คำนวณด้วย float |
| `created_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่สร้างแถวข้อมูลในระบบ; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `updated_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่แก้ไขแถวข้อมูลล่าสุด ต้องอัปเดตทุกช่องทางเขียน; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `version` | `integer` | ไม่ได้ | — | — | เลขรุ่นแถวสำหรับตรวจการแก้ไขพร้อมกัน |

**Keys / Index:** I(company_id,receipt_line_id)

**กฎเฉพาะ:** sum splits = line quantities/value; receipt lot creation+posting atomic

## `receiving.variances`

**เฟส:** W · **หนึ่งแถวคือ:** หนึ่งข้อแตกต่างตอนชั่ง/รับจริง · **ประเภท:** mutable

**คำอธิบาย:** ตารางเก็บข้อมูล หนึ่งข้อแตกต่างตอนชั่ง/รับจริง; หนึ่งแถวมีความหมายตามนี้และอยู่ในเฟส W

| คอลัมน์ | PostgreSQL type | NULL | PK / FK | อ้างอิง | คำอธิบายภาษาไทย |
|---|---|---|---|---|---|
| `id` | `uuid` | ไม่ได้ | PK | — | รหัสหลักภายในของแถวข้อมูล ไม่เปลี่ยนตลอดอายุรายการ; Primary Key ชนิด UUID ห้ามซ้ำหรือเป็น NULL |
| `company_id` | `uuid` | ไม่ได้ | FK | `org.companies.id` | รหัสอ้างอิงบริษัทเจ้าของข้อมูล ไปยัง org.companies.id (บทบาทฟิลด์ company_id) |
| `receipt_line_id` | `uuid` | ไม่ได้ | FK | `receiving.receipt_lines.id` | รหัสอ้างอิง หนึ่งรายละเอียดชั่งรับสินค้า ไปยัง receiving.receipt_lines.id (บทบาทฟิลด์ receipt_line_id) |
| `kind` | `text` | ไม่ได้ | — | — | ชนิดรายการตามค่าที่อนุญาตของตาราง |
| `expected_value` | `numeric(20,6)` | ได้ | — | — | มูลค่าที่คาดหมายตามหลักฐานต้นทาง; เลขทศนิยมแม่นยำ ส่ง API เป็น string ไม่คำนวณด้วย float |
| `actual_value` | `numeric(20,6)` | ได้ | — | — | มูลค่าที่เกิดขึ้นจริง; เลขทศนิยมแม่นยำ ส่ง API เป็น string ไม่คำนวณด้วย float |
| `unit_id` | `uuid` | ได้ | FK | `catalog.units.id` | รหัสอ้างอิง หนึ่งหน่วยในบริษัท ไปยัง catalog.units.id (บทบาทฟิลด์ unit_id) |
| `reason` | `text` | ไม่ได้ | — | — | เหตุผลประกอบการดำเนินการ |
| `status` | `text` | ไม่ได้ | — | — | สถานะรายการตาม state machine ของตาราง |
| `approval_request_id` | `uuid` | ได้ | FK | `platform.approval_requests.id` | รหัสอ้างอิง หนึ่งคำขออนุมัติ snapshot ไปยัง platform.approval_requests.id (บทบาทฟิลด์ approval_request_id) |
| `created_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่สร้างแถวข้อมูลในระบบ; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `updated_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่แก้ไขแถวข้อมูลล่าสุด ต้องอัปเดตทุกช่องทางเขียน; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `version` | `integer` | ไม่ได้ | — | — | เลขรุ่นแถวสำหรับตรวจการแก้ไขพร้อมกัน |

**Keys / Index:** I(company_id,status)

**กฎเฉพาะ:** weight ต่างไม่แก้ delivery qty; เกิน threshold hold ก่อน post

## `receiving.ocr_runs`

**เฟส:** W · **หนึ่งแถวคือ:** หนึ่ง OCR attempt ของไฟล์ · **ประเภท:** mutable

**คำอธิบาย:** ตารางเก็บข้อมูล หนึ่ง OCR attempt ของไฟล์; หนึ่งแถวมีความหมายตามนี้และอยู่ในเฟส W

| คอลัมน์ | PostgreSQL type | NULL | PK / FK | อ้างอิง | คำอธิบายภาษาไทย |
|---|---|---|---|---|---|
| `id` | `uuid` | ไม่ได้ | PK | — | รหัสหลักภายในของแถวข้อมูล ไม่เปลี่ยนตลอดอายุรายการ; Primary Key ชนิด UUID ห้ามซ้ำหรือเป็น NULL |
| `company_id` | `uuid` | ไม่ได้ | FK | `org.companies.id` | รหัสอ้างอิงบริษัทเจ้าของข้อมูล ไปยัง org.companies.id (บทบาทฟิลด์ company_id) |
| `document_id` | `uuid` | ไม่ได้ | FK | `platform.documents.id` | รหัสอ้างอิง หนึ่งเอกสารธุรกิจที่เป็น FK กลาง ไปยัง platform.documents.id (บทบาทฟิลด์ document_id) |
| `file_id` | `uuid` | ไม่ได้ | FK | `platform.files.id` | รหัสอ้างอิง หนึ่ง object ส่วนตัว ไปยัง platform.files.id (บทบาทฟิลด์ file_id) |
| `provider` | `text` | ไม่ได้ | — | — | ชื่อผู้ให้บริการภายนอก |
| `status` | `text` | ไม่ได้ | — | — | สถานะรายการตาม state machine ของตาราง |
| `raw_extraction` | `jsonb` | ได้ | — | — | ผลอ่านข้อมูลดิบก่อนผู้ใช้ตรวจยืนยัน; ต้องตรวจ schema และจำกัดข้อมูลตามสิทธิ์ |
| `confidence` | `jsonb` | ได้ | — | — | คะแนนความมั่นใจในการอ่านข้อมูล ต้องกำหนดสเกลในสัญญาข้อมูล; ต้องตรวจ schema และจำกัดข้อมูลตามสิทธิ์ |
| `confirmed_values` | `jsonb` | ได้ | — | — | ค่าที่ผู้ใช้ตรวจและยืนยันแล้ว; ต้องตรวจ schema และจำกัดข้อมูลตามสิทธิ์ |
| `reviewed_by` | `uuid` | ได้ | FK | `security.users.id` | รหัสอ้างอิงผู้ตรวจทาน ไปยัง security.users.id (บทบาทฟิลด์ reviewed_by) |
| `reviewed_at` | `timestamptz` | ได้ | — | — | เวลาที่ผู้ใช้ตรวจทาน; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `created_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่สร้างแถวข้อมูลในระบบ; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `updated_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่แก้ไขแถวข้อมูลล่าสุด ต้องอัปเดตทุกช่องทางเขียน; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `version` | `integer` | ไม่ได้ | — | — | เลขรุ่นแถวสำหรับตรวจการแก้ไขพร้อมกัน |

**Keys / Index:** I(company_id,document_id)

**กฎเฉพาะ:** raw ไม่ทับ confirmed; human review ก่อนใช้ post; handwriting manual

## `inventory.lots`

**เฟส:** W · **หนึ่งแถวคือ:** หนึ่ง lot คุณภาพ/อายุเดียวกัน · **ประเภท:** mutable

**คำอธิบาย:** ตารางเก็บข้อมูล หนึ่ง lot คุณภาพ/อายุเดียวกัน; หนึ่งแถวมีความหมายตามนี้และอยู่ในเฟส W

| คอลัมน์ | PostgreSQL type | NULL | PK / FK | อ้างอิง | คำอธิบายภาษาไทย |
|---|---|---|---|---|---|
| `id` | `uuid` | ไม่ได้ | PK | — | รหัสหลักภายในของแถวข้อมูล ไม่เปลี่ยนตลอดอายุรายการ; Primary Key ชนิด UUID ห้ามซ้ำหรือเป็น NULL |
| `company_id` | `uuid` | ไม่ได้ | FK | `org.companies.id` | รหัสอ้างอิงบริษัทเจ้าของข้อมูล ไปยัง org.companies.id (บทบาทฟิลด์ company_id) |
| `product_id` | `uuid` | ไม่ได้ | FK | `catalog.products.id` | รหัสอ้างอิงสินค้าในรายการ ไปยัง catalog.products.id (บทบาทฟิลด์ product_id) |
| `lot_code` | `text` | ไม่ได้ | — | — | รหัสล็อตภายในระบบ |
| `supplier_id` | `uuid` | ได้ | FK | `catalog.suppliers.id` | รหัสอ้างอิงผู้ขายในรายการ ไปยัง catalog.suppliers.id (บทบาทฟิลด์ supplier_id) |
| `supplier_lot_code` | `text` | ได้ | — | — | รหัสล็อตที่ผู้ขายระบุ |
| `origin_document_line_id` | `uuid` | ไม่ได้ | FK | `platform.document_lines.id` | รหัสอ้างอิง หนึ่ง line identity ในเอกสาร ไปยัง platform.document_lines.id (บทบาทฟิลด์ origin_document_line_id) |
| `manufactured_at` | `timestamptz` | ได้ | — | — | วันเวลาที่ผลิตตามหลักฐานและนโยบายแปลงวันที่; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `expires_at` | `timestamptz` | ได้ | — | — | เวลาที่สิทธิ์ ข้อมูล หรือสินค้าหมดอายุตามบริบทตาราง; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `received_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่รับตามกระบวนการของตาราง ไม่ถือว่าสต็อกเพิ่มจนกว่าจะ post; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `origin_kind` | `text` | ไม่ได้ | — | — | ประเภทต้นกำเนิดข้อมูล |
| `created_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่สร้างแถวข้อมูลในระบบ; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `updated_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่แก้ไขแถวข้อมูลล่าสุด ต้องอัปเดตทุกช่องทางเขียน; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `version` | `integer` | ไม่ได้ | — | — | เลขรุ่นแถวสำหรับตรวจการแก้ไขพร้อมกัน |

**Keys / Index:** U(company_id,lot_code); I(company_id,product_id,expires_at)

**กฎเฉพาะ:** warehouse ไม่ติดกับ lot เพราะโอนได้; dates immutable หลัง post; nonlot product ใช้ internal lot เพื่อ kernel เดียว

## `inventory.packages`

**เฟส:** W · **หนึ่งแถวคือ:** หนึ่งหน่วยห่อ/ภาชนะที่ trace ได้ · **ประเภท:** mutable

**คำอธิบาย:** ตารางเก็บข้อมูล หนึ่งหน่วยห่อ/ภาชนะที่ trace ได้; หนึ่งแถวมีความหมายตามนี้และอยู่ในเฟส W

| คอลัมน์ | PostgreSQL type | NULL | PK / FK | อ้างอิง | คำอธิบายภาษาไทย |
|---|---|---|---|---|---|
| `id` | `uuid` | ไม่ได้ | PK | — | รหัสหลักภายในของแถวข้อมูล ไม่เปลี่ยนตลอดอายุรายการ; Primary Key ชนิด UUID ห้ามซ้ำหรือเป็น NULL |
| `company_id` | `uuid` | ไม่ได้ | FK | `org.companies.id` | รหัสอ้างอิงบริษัทเจ้าของข้อมูล ไปยัง org.companies.id (บทบาทฟิลด์ company_id) |
| `lot_id` | `uuid` | ไม่ได้ | FK | `inventory.lots.id` | รหัสอ้างอิง หนึ่ง lot คุณภาพ/อายุเดียวกัน ไปยัง inventory.lots.id (บทบาทฟิลด์ lot_id) |
| `package_code` | `text` | ไม่ได้ | — | — | รหัสบรรจุภัณฑ์หรือหน่วยติดตามเฉพาะ |
| `parent_package_id` | `uuid` | ได้ | FK | `inventory.packages.id` | รหัสอ้างอิง หนึ่งหน่วยห่อ/ภาชนะที่ trace ได้ ไปยัง inventory.packages.id (บทบาทฟิลด์ parent_package_id) |
| `initial_stock_qty` | `numeric(20,6)` | ไม่ได้ | — | — | จำนวนสต็อกตั้งต้นของรายการ; เลขทศนิยมแม่นยำ ส่ง API เป็น string ไม่คำนวณด้วย float |
| `initial_weight_kg` | `numeric(20,6)` | ได้ | — | — | น้ำหนักตั้งต้น หน่วยกิโลกรัม; เลขทศนิยมแม่นยำ ส่ง API เป็น string ไม่คำนวณด้วย float |
| `expires_at` | `timestamptz` | ได้ | — | — | เวลาที่สิทธิ์ ข้อมูล หรือสินค้าหมดอายุตามบริบทตาราง; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `status` | `text` | ไม่ได้ | — | — | สถานะรายการตาม state machine ของตาราง |
| `created_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่สร้างแถวข้อมูลในระบบ; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `updated_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่แก้ไขแถวข้อมูลล่าสุด ต้องอัปเดตทุกช่องทางเขียน; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `version` | `integer` | ไม่ได้ | — | — | เลขรุ่นแถวสำหรับตรวจการแก้ไขพร้อมกัน |

**Keys / Index:** U(company_id,package_code)

**กฎเฉพาะ:** remaining มาจาก ledger ไม่แก้ initial; split/repack ผ่าน document+genealogy ไม่สร้าง stock ฟรี

## `inventory.barcodes`

**เฟส:** W · **หนึ่งแถวคือ:** หนึ่งรหัส lot หรือ package · **ประเภท:** mutable

**คำอธิบาย:** ตารางเก็บข้อมูล หนึ่งรหัส lot หรือ package; หนึ่งแถวมีความหมายตามนี้และอยู่ในเฟส W

| คอลัมน์ | PostgreSQL type | NULL | PK / FK | อ้างอิง | คำอธิบายภาษาไทย |
|---|---|---|---|---|---|
| `id` | `uuid` | ไม่ได้ | PK | — | รหัสหลักภายในของแถวข้อมูล ไม่เปลี่ยนตลอดอายุรายการ; Primary Key ชนิด UUID ห้ามซ้ำหรือเป็น NULL |
| `company_id` | `uuid` | ไม่ได้ | FK | `org.companies.id` | รหัสอ้างอิงบริษัทเจ้าของข้อมูล ไปยัง org.companies.id (บทบาทฟิลด์ company_id) |
| `code` | `text` | ไม่ได้ | — | — | รหัสธุรกิจของรายการตามขอบเขต Unique ของตาราง |
| `lot_id` | `uuid` | ได้ | FK | `inventory.lots.id` | รหัสอ้างอิง หนึ่ง lot คุณภาพ/อายุเดียวกัน ไปยัง inventory.lots.id (บทบาทฟิลด์ lot_id) |
| `package_id` | `uuid` | ได้ | FK | `inventory.packages.id` | รหัสอ้างอิง หนึ่งหน่วยห่อ/ภาชนะที่ trace ได้ ไปยัง inventory.packages.id (บทบาทฟิลด์ package_id) |
| `active` | `boolean` | ไม่ได้ | — | — | สถานะเปิดใช้งาน |
| `created_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่สร้างแถวข้อมูลในระบบ; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `updated_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่แก้ไขแถวข้อมูลล่าสุด ต้องอัปเดตทุกช่องทางเขียน; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `version` | `integer` | ไม่ได้ | — | — | เลขรุ่นแถวสำหรับตรวจการแก้ไขพร้อมกัน |

**Keys / Index:** U(code)

**กฎเฉพาะ:** exactly one target; global code opaque ไม่รวม PII; API ยังตรวจ tenant

## `inventory.lot_genealogy`

**เฟส:** O · **หนึ่งแถวคือ:** หนึ่งส่วนเชื่อม lot ต้นทาง/ผลลัพธ์ · **ประเภท:** append

**คำอธิบาย:** ตารางเก็บข้อมูล หนึ่งส่วนเชื่อม lot ต้นทาง/ผลลัพธ์; หนึ่งแถวมีความหมายตามนี้และอยู่ในเฟส O

| คอลัมน์ | PostgreSQL type | NULL | PK / FK | อ้างอิง | คำอธิบายภาษาไทย |
|---|---|---|---|---|---|
| `id` | `uuid` | ไม่ได้ | PK | — | รหัสหลักภายในของแถวข้อมูล ไม่เปลี่ยนตลอดอายุรายการ; Primary Key ชนิด UUID ห้ามซ้ำหรือเป็น NULL |
| `company_id` | `uuid` | ไม่ได้ | FK | `org.companies.id` | รหัสอ้างอิงบริษัทเจ้าของข้อมูล ไปยัง org.companies.id (บทบาทฟิลด์ company_id) |
| `parent_lot_id` | `uuid` | ไม่ได้ | FK | `inventory.lots.id` | รหัสอ้างอิง หนึ่ง lot คุณภาพ/อายุเดียวกัน ไปยัง inventory.lots.id (บทบาทฟิลด์ parent_lot_id) |
| `child_lot_id` | `uuid` | ไม่ได้ | FK | `inventory.lots.id` | รหัสอ้างอิง หนึ่ง lot คุณภาพ/อายุเดียวกัน ไปยัง inventory.lots.id (บทบาทฟิลด์ child_lot_id) |
| `document_id` | `uuid` | ไม่ได้ | FK | `platform.documents.id` | รหัสอ้างอิง หนึ่งเอกสารธุรกิจที่เป็น FK กลาง ไปยัง platform.documents.id (บทบาทฟิลด์ document_id) |
| `kind` | `text` | ไม่ได้ | — | — | ชนิดรายการตามค่าที่อนุญาตของตาราง |
| `input_stock_qty` | `numeric(20,6)` | ไม่ได้ | — | — | จำนวนวัตถุดิบในหน่วยสต็อก; เลขทศนิยมแม่นยำ ส่ง API เป็น string ไม่คำนวณด้วย float |
| `input_weight_kg` | `numeric(20,6)` | ได้ | — | — | น้ำหนักวัตถุดิบเข้า หน่วยกิโลกรัม; เลขทศนิยมแม่นยำ ส่ง API เป็น string ไม่คำนวณด้วย float |
| `allocated_value` | `numeric(20,6)` | ไม่ได้ | — | — | มูลค่าต้นทุนที่จัดสรรให้รายการ; เลขทศนิยมแม่นยำ ส่ง API เป็น string ไม่คำนวณด้วย float |
| `created_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่สร้างแถวข้อมูลในระบบ; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |

**Keys / Index:** U(company_id,parent_lot_id,child_lot_id,document_id)

**กฎเฉพาะ:** RETURN/PROCESS/REPACK; DAG ไม่มีวงจร; multiple inputs/outputs supported

## `inventory.stock_accounts`

**เฟส:** W · **หนึ่งแถวคือ:** หนึ่ง bucket ที่เป็น endpoint ของ ledger · **ประเภท:** mutable

**คำอธิบาย:** ตารางเก็บข้อมูล หนึ่ง bucket ที่เป็น endpoint ของ ledger; หนึ่งแถวมีความหมายตามนี้และอยู่ในเฟส W

| คอลัมน์ | PostgreSQL type | NULL | PK / FK | อ้างอิง | คำอธิบายภาษาไทย |
|---|---|---|---|---|---|
| `id` | `uuid` | ไม่ได้ | PK | — | รหัสหลักภายในของแถวข้อมูล ไม่เปลี่ยนตลอดอายุรายการ; Primary Key ชนิด UUID ห้ามซ้ำหรือเป็น NULL |
| `company_id` | `uuid` | ไม่ได้ | FK | `org.companies.id` | รหัสอ้างอิงบริษัทเจ้าของข้อมูล ไปยัง org.companies.id (บทบาทฟิลด์ company_id) |
| `product_id` | `uuid` | ไม่ได้ | FK | `catalog.products.id` | รหัสอ้างอิงสินค้าในรายการ ไปยัง catalog.products.id (บทบาทฟิลด์ product_id) |
| `lot_id` | `uuid` | ได้ | FK | `inventory.lots.id` | รหัสอ้างอิง หนึ่ง lot คุณภาพ/อายุเดียวกัน ไปยัง inventory.lots.id (บทบาทฟิลด์ lot_id) |
| `package_id` | `uuid` | ได้ | FK | `inventory.packages.id` | รหัสอ้างอิง หนึ่งหน่วยห่อ/ภาชนะที่ trace ได้ ไปยัง inventory.packages.id (บทบาทฟิลด์ package_id) |
| `kind` | `text` | ไม่ได้ | — | — | ชนิดรายการตามค่าที่อนุญาตของตาราง |
| `location_id` | `uuid` | ได้ | FK | `org.locations.id` | รหัสอ้างอิง หนึ่งโหนดสถานที่จริง ไปยัง org.locations.id (บทบาทฟิลด์ location_id) |
| `custody_document_line_id` | `uuid` | ได้ | FK | `platform.document_lines.id` | รหัสอ้างอิง หนึ่ง line identity ในเอกสาร ไปยัง platform.document_lines.id (บทบาทฟิลด์ custody_document_line_id) |
| `stock_status` | `text` | ไม่ได้ | — | — | สถานะสต็อก เช่นพร้อมใช้หรือกักกัน |
| `created_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่สร้างแถวข้อมูลในระบบ; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `updated_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่แก้ไขแถวข้อมูลล่าสุด ต้องอัปเดตทุกช่องทางเขียน; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `version` | `integer` | ไม่ได้ | — | — | เลขรุ่นแถวสำหรับตรวจการแก้ไขพร้อมกัน |

**Keys / Index:** U NULLS NOT DISTINCT(company_id,product_id,lot_id,package_id,kind,location_id,custody_document_line_id,stock_status)

**กฎเฉพาะ:** WAREHOUSE/TRANSIT/CUSTODY/EXTERNAL; warehouse ต้อง location+lot; transit/custody ต้อง doc line+lot; external ไม่ใช้ location; package lot/product consistency

## `inventory.postings`

**เฟส:** W · **หนึ่งแถวคือ:** หนึ่ง ledger posting ต่อ source action · **ประเภท:** append

**คำอธิบาย:** ตารางเก็บข้อมูล หนึ่ง ledger posting ต่อ source action; หนึ่งแถวมีความหมายตามนี้และอยู่ในเฟส W

| คอลัมน์ | PostgreSQL type | NULL | PK / FK | อ้างอิง | คำอธิบายภาษาไทย |
|---|---|---|---|---|---|
| `id` | `uuid` | ไม่ได้ | PK | — | รหัสหลักภายในของแถวข้อมูล ไม่เปลี่ยนตลอดอายุรายการ; Primary Key ชนิด UUID ห้ามซ้ำหรือเป็น NULL |
| `company_id` | `uuid` | ไม่ได้ | FK | `org.companies.id` | รหัสอ้างอิงบริษัทเจ้าของข้อมูล ไปยัง org.companies.id (บทบาทฟิลด์ company_id) |
| `document_id` | `uuid` | ไม่ได้ | FK | `platform.documents.id` | รหัสอ้างอิง หนึ่งเอกสารธุรกิจที่เป็น FK กลาง ไปยัง platform.documents.id (บทบาทฟิลด์ document_id) |
| `action` | `text` | ไม่ได้ | — | — | การกระทำที่บันทึก |
| `posted_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่ลงรายการบัญชีสต็อกสำเร็จ; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `reverses_posting_id` | `uuid` | ได้ | FK | `inventory.postings.id` | รหัสอ้างอิง หนึ่ง ledger posting ต่อ source action ไปยัง inventory.postings.id (บทบาทฟิลด์ reverses_posting_id) |
| `request_id` | `uuid` | ไม่ได้ | — | — | รหัสติดตามคำขอ API เชื่อม log และ audit |
| `created_by` | `uuid` | ไม่ได้ | FK | `security.users.id` | รหัสอ้างอิงผู้สร้าง ไปยัง security.users.id (บทบาทฟิลด์ created_by) |
| `created_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่สร้างแถวข้อมูลในระบบ; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |

**Keys / Index:** U(company_id,document_id,action); U(company_id,reverses_posting_id)

**กฎเฉพาะ:** immutable append; correction ใช้ document ใหม่และ inverse entries

## `inventory.ledger_entries`

**เฟส:** W · **หนึ่งแถวคือ:** หนึ่ง signed delta ต่อ stock account · **ประเภท:** append

**คำอธิบาย:** ตารางเก็บข้อมูล หนึ่ง signed delta ต่อ stock account; หนึ่งแถวมีความหมายตามนี้และอยู่ในเฟส W

| คอลัมน์ | PostgreSQL type | NULL | PK / FK | อ้างอิง | คำอธิบายภาษาไทย |
|---|---|---|---|---|---|
| `id` | `uuid` | ไม่ได้ | PK | — | รหัสหลักภายในของแถวข้อมูล ไม่เปลี่ยนตลอดอายุรายการ; Primary Key ชนิด UUID ห้ามซ้ำหรือเป็น NULL |
| `company_id` | `uuid` | ไม่ได้ | FK | `org.companies.id` | รหัสอ้างอิงบริษัทเจ้าของข้อมูล ไปยัง org.companies.id (บทบาทฟิลด์ company_id) |
| `posting_id` | `uuid` | ไม่ได้ | FK | `inventory.postings.id` | รหัสอ้างอิง หนึ่ง ledger posting ต่อ source action ไปยัง inventory.postings.id (บทบาทฟิลด์ posting_id) |
| `account_id` | `uuid` | ไม่ได้ | FK | `inventory.stock_accounts.id` | รหัสอ้างอิง หนึ่ง bucket ที่เป็น endpoint ของ ledger ไปยัง inventory.stock_accounts.id (บทบาทฟิลด์ account_id) |
| `document_line_id` | `uuid` | ไม่ได้ | FK | `platform.document_lines.id` | รหัสอ้างอิง หนึ่ง line identity ในเอกสาร ไปยัง platform.document_lines.id (บทบาทฟิลด์ document_line_id) |
| `stock_qty_delta` | `numeric(20,6)` | ไม่ได้ | — | — | ผลต่างจำนวนในหน่วยสต็อก มีเครื่องหมายเพิ่มหรือลด; เลขทศนิยมแม่นยำ ส่ง API เป็น string ไม่คำนวณด้วย float |
| `weight_kg_delta` | `numeric(20,6)` | ได้ | — | — | ผลต่างน้ำหนักกิโลกรัม มีเครื่องหมายเพิ่มหรือลด; เลขทศนิยมแม่นยำ ส่ง API เป็น string ไม่คำนวณด้วย float |
| `value_delta` | `numeric(20,6)` | ไม่ได้ | — | — | ผลต่างมูลค่า มีเครื่องหมายเพิ่มหรือลด; เลขทศนิยมแม่นยำ ส่ง API เป็น string ไม่คำนวณด้วย float |
| `entry_no` | `integer` | ไม่ได้ | — | — | ลำดับบรรทัดบันทึก |
| `created_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่สร้างแถวข้อมูลในระบบ; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |

**Keys / Index:** U(company_id,posting_id,entry_no); I(company_id,account_id,created_at)

**กฎเฉพาะ:** product/unit ตาม account; immutable; zero qty allowed เฉพาะ cost adjustment; balanced contra entries

## `inventory.balances`

**เฟส:** W · **หนึ่งแถวคือ:** projection ยอดปัจจุบันต่อ account · **ประเภท:** mutable

**คำอธิบาย:** ตารางเก็บข้อมูล projection ยอดปัจจุบันต่อ account; หนึ่งแถวมีความหมายตามนี้และอยู่ในเฟส W

| คอลัมน์ | PostgreSQL type | NULL | PK / FK | อ้างอิง | คำอธิบายภาษาไทย |
|---|---|---|---|---|---|
| `id` | `uuid` | ไม่ได้ | PK | — | รหัสหลักภายในของแถวข้อมูล ไม่เปลี่ยนตลอดอายุรายการ; Primary Key ชนิด UUID ห้ามซ้ำหรือเป็น NULL |
| `company_id` | `uuid` | ไม่ได้ | FK | `org.companies.id` | รหัสอ้างอิงบริษัทเจ้าของข้อมูล ไปยัง org.companies.id (บทบาทฟิลด์ company_id) |
| `account_id` | `uuid` | ไม่ได้ | FK | `inventory.stock_accounts.id` | รหัสอ้างอิง หนึ่ง bucket ที่เป็น endpoint ของ ledger ไปยัง inventory.stock_accounts.id (บทบาทฟิลด์ account_id) |
| `stock_qty` | `numeric(20,6)` | ไม่ได้ | — | — | จำนวนในหน่วยสต็อกของสินค้า; เลขทศนิยมแม่นยำ ส่ง API เป็น string ไม่คำนวณด้วย float |
| `weight_kg` | `numeric(20,6)` | ได้ | — | — | น้ำหนัก หน่วยกิโลกรัม; เลขทศนิยมแม่นยำ ส่ง API เป็น string ไม่คำนวณด้วย float |
| `inventory_value` | `numeric(20,6)` | ไม่ได้ | — | — | มูลค่าสินค้าคงเหลือ; เลขทศนิยมแม่นยำ ส่ง API เป็น string ไม่คำนวณด้วย float |
| `last_entry_id` | `uuid` | ได้ | FK | `inventory.ledger_entries.id` | รหัสอ้างอิง หนึ่ง signed delta ต่อ stock account ไปยัง inventory.ledger_entries.id (บทบาทฟิลด์ last_entry_id) |
| `created_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่สร้างแถวข้อมูลในระบบ; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `updated_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่แก้ไขแถวข้อมูลล่าสุด ต้องอัปเดตทุกช่องทางเขียน; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `version` | `integer` | ไม่ได้ | — | — | เลขรุ่นแถวสำหรับตรวจการแก้ไขพร้อมกัน |

**Keys / Index:** U(company_id,account_id)

**กฎเฉพาะ:** WAREHOUSE/TRANSIT/CUSTODY nonnegative; EXTERNAL contra signed allowed; rebuild from ledger

## `inventory.reservations`

**เฟส:** W · **หนึ่งแถวคือ:** หนึ่งการกันยอดของ source line/account · **ประเภท:** mutable

**คำอธิบาย:** ตารางเก็บข้อมูล หนึ่งการกันยอดของ source line/account; หนึ่งแถวมีความหมายตามนี้และอยู่ในเฟส W

| คอลัมน์ | PostgreSQL type | NULL | PK / FK | อ้างอิง | คำอธิบายภาษาไทย |
|---|---|---|---|---|---|
| `id` | `uuid` | ไม่ได้ | PK | — | รหัสหลักภายในของแถวข้อมูล ไม่เปลี่ยนตลอดอายุรายการ; Primary Key ชนิด UUID ห้ามซ้ำหรือเป็น NULL |
| `company_id` | `uuid` | ไม่ได้ | FK | `org.companies.id` | รหัสอ้างอิงบริษัทเจ้าของข้อมูล ไปยัง org.companies.id (บทบาทฟิลด์ company_id) |
| `document_line_id` | `uuid` | ไม่ได้ | FK | `platform.document_lines.id` | รหัสอ้างอิง หนึ่ง line identity ในเอกสาร ไปยัง platform.document_lines.id (บทบาทฟิลด์ document_line_id) |
| `account_id` | `uuid` | ไม่ได้ | FK | `inventory.stock_accounts.id` | รหัสอ้างอิง หนึ่ง bucket ที่เป็น endpoint ของ ledger ไปยัง inventory.stock_accounts.id (บทบาทฟิลด์ account_id) |
| `stock_qty` | `numeric(20,6)` | ไม่ได้ | — | — | จำนวนในหน่วยสต็อกของสินค้า; เลขทศนิยมแม่นยำ ส่ง API เป็น string ไม่คำนวณด้วย float |
| `weight_kg` | `numeric(20,6)` | ได้ | — | — | น้ำหนัก หน่วยกิโลกรัม; เลขทศนิยมแม่นยำ ส่ง API เป็น string ไม่คำนวณด้วย float |
| `status` | `text` | ไม่ได้ | — | — | สถานะรายการตาม state machine ของตาราง |
| `expires_at` | `timestamptz` | ได้ | — | — | เวลาที่สิทธิ์ ข้อมูล หรือสินค้าหมดอายุตามบริบทตาราง; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `created_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่สร้างแถวข้อมูลในระบบ; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `updated_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่แก้ไขแถวข้อมูลล่าสุด ต้องอัปเดตทุกช่องทางเขียน; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `version` | `integer` | ไม่ได้ | — | — | เลขรุ่นแถวสำหรับตรวจการแก้ไขพร้อมกัน |

**Keys / Index:** I(company_id,account_id,status); U(company_id,document_line_id,account_id)

**กฎเฉพาะ:** HELD/CONSUMED/RELEASED/EXPIRED; available=balance-held; no double deduction

## `inventory.cost_layers`

**เฟส:** W · **หนึ่งแถวคือ:** หนึ่งต้นทุนรับเข้า/ผลผลิตของ lot · **ประเภท:** mutable

**คำอธิบาย:** ตารางเก็บข้อมูล หนึ่งต้นทุนรับเข้า/ผลผลิตของ lot; หนึ่งแถวมีความหมายตามนี้และอยู่ในเฟส W

| คอลัมน์ | PostgreSQL type | NULL | PK / FK | อ้างอิง | คำอธิบายภาษาไทย |
|---|---|---|---|---|---|
| `id` | `uuid` | ไม่ได้ | PK | — | รหัสหลักภายในของแถวข้อมูล ไม่เปลี่ยนตลอดอายุรายการ; Primary Key ชนิด UUID ห้ามซ้ำหรือเป็น NULL |
| `company_id` | `uuid` | ไม่ได้ | FK | `org.companies.id` | รหัสอ้างอิงบริษัทเจ้าของข้อมูล ไปยัง org.companies.id (บทบาทฟิลด์ company_id) |
| `lot_id` | `uuid` | ไม่ได้ | FK | `inventory.lots.id` | รหัสอ้างอิง หนึ่ง lot คุณภาพ/อายุเดียวกัน ไปยัง inventory.lots.id (บทบาทฟิลด์ lot_id) |
| `source_line_id` | `uuid` | ไม่ได้ | FK | `platform.document_lines.id` | รหัสอ้างอิง หนึ่ง line identity ในเอกสาร ไปยัง platform.document_lines.id (บทบาทฟิลด์ source_line_id) |
| `original_stock_qty` | `numeric(20,6)` | ไม่ได้ | — | — | จำนวนสต็อกต้นฉบับก่อนปรับ; เลขทศนิยมแม่นยำ ส่ง API เป็น string ไม่คำนวณด้วย float |
| `original_value` | `numeric(20,6)` | ไม่ได้ | — | — | มูลค่าต้นฉบับก่อนปรับ; เลขทศนิยมแม่นยำ ส่ง API เป็น string ไม่คำนวณด้วย float |
| `cost_method` | `text` | ไม่ได้ | — | — | วิธีคำนวณต้นทุนที่ใช้กับรายการ |
| `created_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่สร้างแถวข้อมูลในระบบ; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `updated_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่แก้ไขแถวข้อมูลล่าสุด ต้องอัปเดตทุกช่องทางเขียน; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `version` | `integer` | ไม่ได้ | — | — | เลขรุ่นแถวสำหรับตรวจการแก้ไขพร้อมกัน |

**Keys / Index:** U(company_id,source_line_id,lot_id)

**กฎเฉพาะ:** proposed SPECIFIC_LOT basis; ราคาซื้อ/ภาษีที่ reclaim ได้ไม่ปนต้นทุน; decisions ระบุ

## `inventory.cost_allocations`

**เฟส:** W · **หนึ่งแถวคือ:** หนึ่งต้นทุนที่ออก/คืนจาก layer · **ประเภท:** append

**คำอธิบาย:** ตารางเก็บข้อมูล หนึ่งต้นทุนที่ออก/คืนจาก layer; หนึ่งแถวมีความหมายตามนี้และอยู่ในเฟส W

| คอลัมน์ | PostgreSQL type | NULL | PK / FK | อ้างอิง | คำอธิบายภาษาไทย |
|---|---|---|---|---|---|
| `id` | `uuid` | ไม่ได้ | PK | — | รหัสหลักภายในของแถวข้อมูล ไม่เปลี่ยนตลอดอายุรายการ; Primary Key ชนิด UUID ห้ามซ้ำหรือเป็น NULL |
| `company_id` | `uuid` | ไม่ได้ | FK | `org.companies.id` | รหัสอ้างอิงบริษัทเจ้าของข้อมูล ไปยัง org.companies.id (บทบาทฟิลด์ company_id) |
| `layer_id` | `uuid` | ไม่ได้ | FK | `inventory.cost_layers.id` | รหัสอ้างอิง หนึ่งต้นทุนรับเข้า/ผลผลิตของ lot ไปยัง inventory.cost_layers.id (บทบาทฟิลด์ layer_id) |
| `ledger_entry_id` | `uuid` | ไม่ได้ | FK | `inventory.ledger_entries.id` | รหัสอ้างอิง หนึ่ง signed delta ต่อ stock account ไปยัง inventory.ledger_entries.id (บทบาทฟิลด์ ledger_entry_id) |
| `stock_qty` | `numeric(20,6)` | ไม่ได้ | — | — | จำนวนในหน่วยสต็อกของสินค้า; เลขทศนิยมแม่นยำ ส่ง API เป็น string ไม่คำนวณด้วย float |
| `value` | `numeric(20,6)` | ไม่ได้ | — | — | มูลค่าหรือค่าข้อมูลตามชนิดและบริบทของตาราง; เลขทศนิยมแม่นยำ ส่ง API เป็น string ไม่คำนวณด้วย float |
| `direction` | `text` | ไม่ได้ | — | — | ทิศทางของรายการตามประเภทงาน |
| `created_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่สร้างแถวข้อมูลในระบบ; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |

**Keys / Index:** U(company_id,layer_id,ledger_entry_id)

**กฎเฉพาะ:** ISSUE/RESTORE; sum not over layer; return restore uses original issue cost

## `inventory.opening_lines`

**เฟส:** W · **หนึ่งแถวคือ:** หนึ่งสต็อกตั้งต้นที่ยืนยัน · **ประเภท:** mutable

**คำอธิบาย:** ตารางเก็บข้อมูล หนึ่งสต็อกตั้งต้นที่ยืนยัน; หนึ่งแถวมีความหมายตามนี้และอยู่ในเฟส W

| คอลัมน์ | PostgreSQL type | NULL | PK / FK | อ้างอิง | คำอธิบายภาษาไทย |
|---|---|---|---|---|---|
| `id` | `uuid` | ไม่ได้ | PK | — | รหัสหลักภายในของแถวข้อมูล ไม่เปลี่ยนตลอดอายุรายการ; Primary Key ชนิด UUID ห้ามซ้ำหรือเป็น NULL |
| `company_id` | `uuid` | ไม่ได้ | FK | `org.companies.id` | รหัสอ้างอิงบริษัทเจ้าของข้อมูล ไปยัง org.companies.id (บทบาทฟิลด์ company_id) |
| `document_line_id` | `uuid` | ไม่ได้ | FK | `platform.document_lines.id` | รหัสอ้างอิง หนึ่ง line identity ในเอกสาร ไปยัง platform.document_lines.id (บทบาทฟิลด์ document_line_id) |
| `account_id` | `uuid` | ไม่ได้ | FK | `inventory.stock_accounts.id` | รหัสอ้างอิง หนึ่ง bucket ที่เป็น endpoint ของ ledger ไปยัง inventory.stock_accounts.id (บทบาทฟิลด์ account_id) |
| `stock_qty` | `numeric(20,6)` | ไม่ได้ | — | — | จำนวนในหน่วยสต็อกของสินค้า; เลขทศนิยมแม่นยำ ส่ง API เป็น string ไม่คำนวณด้วย float |
| `weight_kg` | `numeric(20,6)` | ได้ | — | — | น้ำหนัก หน่วยกิโลกรัม; เลขทศนิยมแม่นยำ ส่ง API เป็น string ไม่คำนวณด้วย float |
| `inventory_value` | `numeric(20,6)` | ไม่ได้ | — | — | มูลค่าสินค้าคงเหลือ; เลขทศนิยมแม่นยำ ส่ง API เป็น string ไม่คำนวณด้วย float |
| `import_row_id` | `uuid` | ได้ | FK | `integration.import_rows.id` | รหัสอ้างอิง หนึ่งแถว staging ไปยัง integration.import_rows.id (บทบาทฟิลด์ import_row_id) |
| `created_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่สร้างแถวข้อมูลในระบบ; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `updated_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่แก้ไขแถวข้อมูลล่าสุด ต้องอัปเดตทุกช่องทางเขียน; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `version` | `integer` | ไม่ได้ | — | — | เลขรุ่นแถวสำหรับตรวจการแก้ไขพร้อมกัน |

**Keys / Index:** U(company_id,document_line_id)

**กฎเฉพาะ:** approved opening doc; ไม่มี fake delivery/PO เพิ่มซ้ำ

## `inventory.status_changes`

**เฟส:** W · **หนึ่งแถวคือ:** หนึ่งการกักกัน/ปล่อย/เปลี่ยน bucket · **ประเภท:** mutable

**คำอธิบาย:** ตารางเก็บข้อมูล หนึ่งการกักกัน/ปล่อย/เปลี่ยน bucket; หนึ่งแถวมีความหมายตามนี้และอยู่ในเฟส W

| คอลัมน์ | PostgreSQL type | NULL | PK / FK | อ้างอิง | คำอธิบายภาษาไทย |
|---|---|---|---|---|---|
| `id` | `uuid` | ไม่ได้ | PK | — | รหัสหลักภายในของแถวข้อมูล ไม่เปลี่ยนตลอดอายุรายการ; Primary Key ชนิด UUID ห้ามซ้ำหรือเป็น NULL |
| `company_id` | `uuid` | ไม่ได้ | FK | `org.companies.id` | รหัสอ้างอิงบริษัทเจ้าของข้อมูล ไปยัง org.companies.id (บทบาทฟิลด์ company_id) |
| `document_line_id` | `uuid` | ไม่ได้ | FK | `platform.document_lines.id` | รหัสอ้างอิง หนึ่ง line identity ในเอกสาร ไปยัง platform.document_lines.id (บทบาทฟิลด์ document_line_id) |
| `from_account_id` | `uuid` | ไม่ได้ | FK | `inventory.stock_accounts.id` | รหัสอ้างอิงบัญชีสต็อกต้นทาง ไปยัง inventory.stock_accounts.id (บทบาทฟิลด์ from_account_id) |
| `to_account_id` | `uuid` | ไม่ได้ | FK | `inventory.stock_accounts.id` | รหัสอ้างอิงบัญชีสต็อกปลายทาง ไปยัง inventory.stock_accounts.id (บทบาทฟิลด์ to_account_id) |
| `stock_qty` | `numeric(20,6)` | ไม่ได้ | — | — | จำนวนในหน่วยสต็อกของสินค้า; เลขทศนิยมแม่นยำ ส่ง API เป็น string ไม่คำนวณด้วย float |
| `weight_kg` | `numeric(20,6)` | ได้ | — | — | น้ำหนัก หน่วยกิโลกรัม; เลขทศนิยมแม่นยำ ส่ง API เป็น string ไม่คำนวณด้วย float |
| `reason` | `text` | ไม่ได้ | — | — | เหตุผลประกอบการดำเนินการ |
| `approval_request_id` | `uuid` | ได้ | FK | `platform.approval_requests.id` | รหัสอ้างอิง หนึ่งคำขออนุมัติ snapshot ไปยัง platform.approval_requests.id (บทบาทฟิลด์ approval_request_id) |
| `created_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่สร้างแถวข้อมูลในระบบ; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `updated_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่แก้ไขแถวข้อมูลล่าสุด ต้องอัปเดตทุกช่องทางเขียน; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `version` | `integer` | ไม่ได้ | — | — | เลขรุ่นแถวสำหรับตรวจการแก้ไขพร้อมกัน |

**Keys / Index:** U(company_id,document_line_id)

**กฎเฉพาะ:** same product lot location; ledger pair; expired blocked by query even before scheduler

## `inventory.cost_adjustment_lines`

**เฟส:** W · **หนึ่งแถวคือ:** หนึ่งแก้ต้นทุนที่ไม่มีการเปลี่ยนจำนวน · **ประเภท:** mutable

**คำอธิบาย:** ตารางเก็บข้อมูล หนึ่งแก้ต้นทุนที่ไม่มีการเปลี่ยนจำนวน; หนึ่งแถวมีความหมายตามนี้และอยู่ในเฟส W

| คอลัมน์ | PostgreSQL type | NULL | PK / FK | อ้างอิง | คำอธิบายภาษาไทย |
|---|---|---|---|---|---|
| `id` | `uuid` | ไม่ได้ | PK | — | รหัสหลักภายในของแถวข้อมูล ไม่เปลี่ยนตลอดอายุรายการ; Primary Key ชนิด UUID ห้ามซ้ำหรือเป็น NULL |
| `company_id` | `uuid` | ไม่ได้ | FK | `org.companies.id` | รหัสอ้างอิงบริษัทเจ้าของข้อมูล ไปยัง org.companies.id (บทบาทฟิลด์ company_id) |
| `document_line_id` | `uuid` | ไม่ได้ | FK | `platform.document_lines.id` | รหัสอ้างอิง หนึ่ง line identity ในเอกสาร ไปยัง platform.document_lines.id (บทบาทฟิลด์ document_line_id) |
| `account_id` | `uuid` | ไม่ได้ | FK | `inventory.stock_accounts.id` | รหัสอ้างอิง หนึ่ง bucket ที่เป็น endpoint ของ ledger ไปยัง inventory.stock_accounts.id (บทบาทฟิลด์ account_id) |
| `cost_layer_id` | `uuid` | ไม่ได้ | FK | `inventory.cost_layers.id` | รหัสอ้างอิง หนึ่งต้นทุนรับเข้า/ผลผลิตของ lot ไปยัง inventory.cost_layers.id (บทบาทฟิลด์ cost_layer_id) |
| `value_delta` | `numeric(20,6)` | ไม่ได้ | — | — | ผลต่างมูลค่า มีเครื่องหมายเพิ่มหรือลด; เลขทศนิยมแม่นยำ ส่ง API เป็น string ไม่คำนวณด้วย float |
| `reason` | `text` | ไม่ได้ | — | — | เหตุผลประกอบการดำเนินการ |
| `approval_request_id` | `uuid` | ไม่ได้ | FK | `platform.approval_requests.id` | รหัสอ้างอิง หนึ่งคำขออนุมัติ snapshot ไปยัง platform.approval_requests.id (บทบาทฟิลด์ approval_request_id) |
| `created_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่สร้างแถวข้อมูลในระบบ; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `updated_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่แก้ไขแถวข้อมูลล่าสุด ต้องอัปเดตทุกช่องทางเขียน; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `version` | `integer` | ไม่ได้ | — | — | เลขรุ่นแถวสำหรับตรวจการแก้ไขพร้อมกัน |

**Keys / Index:** U(company_id,document_line_id)

**กฎเฉพาะ:** qty delta0; remaining stock/cost variance ปันส่วนตาม policy; ไม่ rewrite receipt

## `inventory.repack_lines`

**เฟส:** W · **หนึ่งแถวคือ:** หนึ่งคู่แบ่ง/รวม package ของ lot เดิม · **ประเภท:** mutable

**คำอธิบาย:** ตารางเก็บข้อมูล หนึ่งคู่แบ่ง/รวม package ของ lot เดิม; หนึ่งแถวมีความหมายตามนี้และอยู่ในเฟส W

| คอลัมน์ | PostgreSQL type | NULL | PK / FK | อ้างอิง | คำอธิบายภาษาไทย |
|---|---|---|---|---|---|
| `id` | `uuid` | ไม่ได้ | PK | — | รหัสหลักภายในของแถวข้อมูล ไม่เปลี่ยนตลอดอายุรายการ; Primary Key ชนิด UUID ห้ามซ้ำหรือเป็น NULL |
| `company_id` | `uuid` | ไม่ได้ | FK | `org.companies.id` | รหัสอ้างอิงบริษัทเจ้าของข้อมูล ไปยัง org.companies.id (บทบาทฟิลด์ company_id) |
| `document_line_id` | `uuid` | ไม่ได้ | FK | `platform.document_lines.id` | รหัสอ้างอิง หนึ่ง line identity ในเอกสาร ไปยัง platform.document_lines.id (บทบาทฟิลด์ document_line_id) |
| `from_account_id` | `uuid` | ไม่ได้ | FK | `inventory.stock_accounts.id` | รหัสอ้างอิงบัญชีสต็อกต้นทาง ไปยัง inventory.stock_accounts.id (บทบาทฟิลด์ from_account_id) |
| `to_account_id` | `uuid` | ไม่ได้ | FK | `inventory.stock_accounts.id` | รหัสอ้างอิงบัญชีสต็อกปลายทาง ไปยัง inventory.stock_accounts.id (บทบาทฟิลด์ to_account_id) |
| `stock_qty` | `numeric(20,6)` | ไม่ได้ | — | — | จำนวนในหน่วยสต็อกของสินค้า; เลขทศนิยมแม่นยำ ส่ง API เป็น string ไม่คำนวณด้วย float |
| `weight_kg` | `numeric(20,6)` | ได้ | — | — | น้ำหนัก หน่วยกิโลกรัม; เลขทศนิยมแม่นยำ ส่ง API เป็น string ไม่คำนวณด้วย float |
| `value` | `numeric(20,6)` | ไม่ได้ | — | — | มูลค่าหรือค่าข้อมูลตามชนิดและบริบทของตาราง; เลขทศนิยมแม่นยำ ส่ง API เป็น string ไม่คำนวณด้วย float |
| `created_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่สร้างแถวข้อมูลในระบบ; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `updated_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่แก้ไขแถวข้อมูลล่าสุด ต้องอัปเดตทุกช่องทางเขียน; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `version` | `integer` | ไม่ได้ | — | — | เลขรุ่นแถวสำหรับตรวจการแก้ไขพร้อมกัน |

**Keys / Index:** U(company_id,document_line_id)

**กฎเฉพาะ:** same product/lot; packages ต่างกันได้; qty/value conserved; package ancestry ต้องไม่มีวงจร

## `inventory.transfers`

**เฟส:** O · **หนึ่งแถวคือ:** หนึ่งเอกสารย้ายภายในบริษัท · **ประเภท:** mutable

**คำอธิบาย:** ตารางเก็บข้อมูล หนึ่งเอกสารย้ายภายในบริษัท; หนึ่งแถวมีความหมายตามนี้และอยู่ในเฟส O

| คอลัมน์ | PostgreSQL type | NULL | PK / FK | อ้างอิง | คำอธิบายภาษาไทย |
|---|---|---|---|---|---|
| `id` | `uuid` | ไม่ได้ | PK | — | รหัสหลักภายในของแถวข้อมูล ไม่เปลี่ยนตลอดอายุรายการ; Primary Key ชนิด UUID ห้ามซ้ำหรือเป็น NULL |
| `company_id` | `uuid` | ไม่ได้ | FK | `org.companies.id` | รหัสอ้างอิงบริษัทเจ้าของข้อมูล ไปยัง org.companies.id (บทบาทฟิลด์ company_id) |
| `document_id` | `uuid` | ไม่ได้ | FK | `platform.documents.id` | รหัสอ้างอิง หนึ่งเอกสารธุรกิจที่เป็น FK กลาง ไปยัง platform.documents.id (บทบาทฟิลด์ document_id) |
| `from_warehouse_id` | `uuid` | ไม่ได้ | FK | `org.warehouses.id` | รหัสอ้างอิง หนึ่งคลังในสาขา ไปยัง org.warehouses.id (บทบาทฟิลด์ from_warehouse_id) |
| `to_warehouse_id` | `uuid` | ไม่ได้ | FK | `org.warehouses.id` | รหัสอ้างอิง หนึ่งคลังในสาขา ไปยัง org.warehouses.id (บทบาทฟิลด์ to_warehouse_id) |
| `dispatched_at` | `timestamptz` | ได้ | — | — | เวลาที่ส่งสินค้าออก; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `closed_at` | `timestamptz` | ได้ | — | — | เวลาที่ปิดรายการ; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `approval_request_id` | `uuid` | ได้ | FK | `platform.approval_requests.id` | รหัสอ้างอิง หนึ่งคำขออนุมัติ snapshot ไปยัง platform.approval_requests.id (บทบาทฟิลด์ approval_request_id) |
| `created_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่สร้างแถวข้อมูลในระบบ; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `updated_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่แก้ไขแถวข้อมูลล่าสุด ต้องอัปเดตทุกช่องทางเขียน; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `version` | `integer` | ไม่ได้ | — | — | เลขรุ่นแถวสำหรับตรวจการแก้ไขพร้อมกัน |

**Keys / Index:** U(company_id,document_id)

**กฎเฉพาะ:** branch scope both ends; inter-company transfers excluded use separate purchase/sale contract

## `inventory.transfer_lines`

**เฟส:** O · **หนึ่งแถวคือ:** หนึ่ง line lot/package ที่ส่ง · **ประเภท:** mutable

**คำอธิบาย:** ตารางเก็บข้อมูล หนึ่ง line lot/package ที่ส่ง; หนึ่งแถวมีความหมายตามนี้และอยู่ในเฟส O

| คอลัมน์ | PostgreSQL type | NULL | PK / FK | อ้างอิง | คำอธิบายภาษาไทย |
|---|---|---|---|---|---|
| `id` | `uuid` | ไม่ได้ | PK | — | รหัสหลักภายในของแถวข้อมูล ไม่เปลี่ยนตลอดอายุรายการ; Primary Key ชนิด UUID ห้ามซ้ำหรือเป็น NULL |
| `company_id` | `uuid` | ไม่ได้ | FK | `org.companies.id` | รหัสอ้างอิงบริษัทเจ้าของข้อมูล ไปยัง org.companies.id (บทบาทฟิลด์ company_id) |
| `document_line_id` | `uuid` | ไม่ได้ | FK | `platform.document_lines.id` | รหัสอ้างอิง หนึ่ง line identity ในเอกสาร ไปยัง platform.document_lines.id (บทบาทฟิลด์ document_line_id) |
| `transfer_id` | `uuid` | ไม่ได้ | FK | `inventory.transfers.id` | รหัสอ้างอิง หนึ่งเอกสารย้ายภายในบริษัท ไปยัง inventory.transfers.id (บทบาทฟิลด์ transfer_id) |
| `from_account_id` | `uuid` | ไม่ได้ | FK | `inventory.stock_accounts.id` | รหัสอ้างอิงบัญชีสต็อกต้นทาง ไปยัง inventory.stock_accounts.id (บทบาทฟิลด์ from_account_id) |
| `dispatched_qty` | `numeric(20,6)` | ไม่ได้ | — | — | จำนวนที่ส่งออกตามหน่วยรายการ; เลขทศนิยมแม่นยำ ส่ง API เป็น string ไม่คำนวณด้วย float |
| `dispatched_weight_kg` | `numeric(20,6)` | ได้ | — | — | น้ำหนักที่ส่งออก หน่วยกิโลกรัม; เลขทศนิยมแม่นยำ ส่ง API เป็น string ไม่คำนวณด้วย float |
| `transit_account_id` | `uuid` | ไม่ได้ | FK | `inventory.stock_accounts.id` | รหัสอ้างอิง หนึ่ง bucket ที่เป็น endpoint ของ ledger ไปยัง inventory.stock_accounts.id (บทบาทฟิลด์ transit_account_id) |
| `created_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่สร้างแถวข้อมูลในระบบ; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `updated_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่แก้ไขแถวข้อมูลล่าสุด ต้องอัปเดตทุกช่องทางเขียน; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `version` | `integer` | ไม่ได้ | — | — | เลขรุ่นแถวสำหรับตรวจการแก้ไขพร้อมกัน |

**Keys / Index:** U(company_id,document_line_id)

**กฎเฉพาะ:** dispatch warehouse -> transit; no destination increase until receive

## `inventory.transfer_receipts`

**เฟส:** O · **หนึ่งแถวคือ:** หนึ่งรอบรับ transfer line · **ประเภท:** mutable

**คำอธิบาย:** ตารางเก็บข้อมูล หนึ่งรอบรับ transfer line; หนึ่งแถวมีความหมายตามนี้และอยู่ในเฟส O

| คอลัมน์ | PostgreSQL type | NULL | PK / FK | อ้างอิง | คำอธิบายภาษาไทย |
|---|---|---|---|---|---|
| `id` | `uuid` | ไม่ได้ | PK | — | รหัสหลักภายในของแถวข้อมูล ไม่เปลี่ยนตลอดอายุรายการ; Primary Key ชนิด UUID ห้ามซ้ำหรือเป็น NULL |
| `company_id` | `uuid` | ไม่ได้ | FK | `org.companies.id` | รหัสอ้างอิงบริษัทเจ้าของข้อมูล ไปยัง org.companies.id (บทบาทฟิลด์ company_id) |
| `document_line_id` | `uuid` | ไม่ได้ | FK | `platform.document_lines.id` | รหัสอ้างอิง หนึ่ง line identity ในเอกสาร ไปยัง platform.document_lines.id (บทบาทฟิลด์ document_line_id) |
| `transfer_line_id` | `uuid` | ไม่ได้ | FK | `inventory.transfer_lines.id` | รหัสอ้างอิง หนึ่ง line lot/package ที่ส่ง ไปยัง inventory.transfer_lines.id (บทบาทฟิลด์ transfer_line_id) |
| `to_account_id` | `uuid` | ไม่ได้ | FK | `inventory.stock_accounts.id` | รหัสอ้างอิงบัญชีสต็อกปลายทาง ไปยัง inventory.stock_accounts.id (บทบาทฟิลด์ to_account_id) |
| `received_qty` | `numeric(20,6)` | ไม่ได้ | — | — | จำนวนที่รับได้จริงตามหน่วยรายการ; เลขทศนิยมแม่นยำ ส่ง API เป็น string ไม่คำนวณด้วย float |
| `received_weight_kg` | `numeric(20,6)` | ได้ | — | — | น้ำหนักที่รับได้จริง หน่วยกิโลกรัม; เลขทศนิยมแม่นยำ ส่ง API เป็น string ไม่คำนวณด้วย float |
| `variance_reason` | `text` | ได้ | — | — | เหตุผลของผลต่างจากยอดอ้างอิง |
| `created_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่สร้างแถวข้อมูลในระบบ; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `updated_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่แก้ไขแถวข้อมูลล่าสุด ต้องอัปเดตทุกช่องทางเขียน; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `version` | `integer` | ไม่ได้ | — | — | เลขรุ่นแถวสำหรับตรวจการแก้ไขพร้อมกัน |

**Keys / Index:** U(company_id,document_line_id)

**กฎเฉพาะ:** receive transit->warehouse; shortage remains transit until approved resolution

## `inventory.count_sessions`

**เฟส:** O · **หนึ่งแถวคือ:** หนึ่งรอบตรวจนับ · **ประเภท:** mutable

**คำอธิบาย:** ตารางเก็บข้อมูล หนึ่งรอบตรวจนับ; หนึ่งแถวมีความหมายตามนี้และอยู่ในเฟส O

| คอลัมน์ | PostgreSQL type | NULL | PK / FK | อ้างอิง | คำอธิบายภาษาไทย |
|---|---|---|---|---|---|
| `id` | `uuid` | ไม่ได้ | PK | — | รหัสหลักภายในของแถวข้อมูล ไม่เปลี่ยนตลอดอายุรายการ; Primary Key ชนิด UUID ห้ามซ้ำหรือเป็น NULL |
| `company_id` | `uuid` | ไม่ได้ | FK | `org.companies.id` | รหัสอ้างอิงบริษัทเจ้าของข้อมูล ไปยัง org.companies.id (บทบาทฟิลด์ company_id) |
| `document_id` | `uuid` | ไม่ได้ | FK | `platform.documents.id` | รหัสอ้างอิง หนึ่งเอกสารธุรกิจที่เป็น FK กลาง ไปยัง platform.documents.id (บทบาทฟิลด์ document_id) |
| `warehouse_id` | `uuid` | ไม่ได้ | FK | `org.warehouses.id` | รหัสอ้างอิงคลังที่เกี่ยวข้อง ไปยัง org.warehouses.id (บทบาทฟิลด์ warehouse_id) |
| `scope_snapshot` | `jsonb` | ไม่ได้ | — | — | สำเนาขอบเขตสิทธิ์หรือขอบเขตงาน ณ เวลาดำเนินการ; ต้องตรวจ schema และจำกัดข้อมูลตามสิทธิ์ |
| `blind_count` | `boolean` | ไม่ได้ | — | — | กำหนดให้นับโดยไม่แสดงยอดตามระบบ |
| `started_at` | `timestamptz` | ได้ | — | — | เวลาที่เริ่มดำเนินการ; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `completed_at` | `timestamptz` | ได้ | — | — | เวลาที่ดำเนินการสำเร็จ; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `freeze_policy` | `text` | ไม่ได้ | — | — | นโยบายระงับการเคลื่อนไหวระหว่างตรวจนับ |
| `created_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่สร้างแถวข้อมูลในระบบ; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `updated_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่แก้ไขแถวข้อมูลล่าสุด ต้องอัปเดตทุกช่องทางเขียน; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `version` | `integer` | ไม่ได้ | — | — | เลขรุ่นแถวสำหรับตรวจการแก้ไขพร้อมกัน |

**Keys / Index:** U(company_id,document_id)

**กฎเฉพาะ:** baseline scope freeze mandatory; no movements in frozen accounts until released

## `inventory.count_scope_locks`

**เฟส:** O · **หนึ่งแถวคือ:** หนึ่ง freeze ที่มีผลต่อ warehouse · **ประเภท:** mutable

**คำอธิบาย:** ตารางเก็บข้อมูล หนึ่ง freeze ที่มีผลต่อ warehouse; หนึ่งแถวมีความหมายตามนี้และอยู่ในเฟส O

| คอลัมน์ | PostgreSQL type | NULL | PK / FK | อ้างอิง | คำอธิบายภาษาไทย |
|---|---|---|---|---|---|
| `id` | `uuid` | ไม่ได้ | PK | — | รหัสหลักภายในของแถวข้อมูล ไม่เปลี่ยนตลอดอายุรายการ; Primary Key ชนิด UUID ห้ามซ้ำหรือเป็น NULL |
| `company_id` | `uuid` | ไม่ได้ | FK | `org.companies.id` | รหัสอ้างอิงบริษัทเจ้าของข้อมูล ไปยัง org.companies.id (บทบาทฟิลด์ company_id) |
| `warehouse_id` | `uuid` | ไม่ได้ | FK | `org.warehouses.id` | รหัสอ้างอิงคลังที่เกี่ยวข้อง ไปยัง org.warehouses.id (บทบาทฟิลด์ warehouse_id) |
| `session_id` | `uuid` | ไม่ได้ | FK | `inventory.count_sessions.id` | รหัสอ้างอิง หนึ่งรอบตรวจนับ ไปยัง inventory.count_sessions.id (บทบาทฟิลด์ session_id) |
| `active` | `boolean` | ไม่ได้ | — | — | สถานะเปิดใช้งาน |
| `released_at` | `timestamptz` | ได้ | — | — | เวลาที่ปลดการระงับหรือคืนสิทธิ์จอง; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `created_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่สร้างแถวข้อมูลในระบบ; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `updated_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่แก้ไขแถวข้อมูลล่าสุด ต้องอัปเดตทุกช่องทางเขียน; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `version` | `integer` | ไม่ได้ | — | — | เลขรุ่นแถวสำหรับตรวจการแก้ไขพร้อมกัน |

**Keys / Index:** partial U(company_id,warehouse_id) WHERE active

**กฎเฉพาะ:** baseline freeze ทั้งwarehouse แม้ count subset; postingและเปิด/ปิดfreezeล็อก warehouse row เดียวกัน

## `inventory.count_lines`

**เฟส:** O · **หนึ่งแถวคือ:** หนึ่ง account snapshot ในรอบนับ · **ประเภท:** mutable

**คำอธิบาย:** ตารางเก็บข้อมูล หนึ่ง account snapshot ในรอบนับ; หนึ่งแถวมีความหมายตามนี้และอยู่ในเฟส O

| คอลัมน์ | PostgreSQL type | NULL | PK / FK | อ้างอิง | คำอธิบายภาษาไทย |
|---|---|---|---|---|---|
| `id` | `uuid` | ไม่ได้ | PK | — | รหัสหลักภายในของแถวข้อมูล ไม่เปลี่ยนตลอดอายุรายการ; Primary Key ชนิด UUID ห้ามซ้ำหรือเป็น NULL |
| `company_id` | `uuid` | ไม่ได้ | FK | `org.companies.id` | รหัสอ้างอิงบริษัทเจ้าของข้อมูล ไปยัง org.companies.id (บทบาทฟิลด์ company_id) |
| `document_line_id` | `uuid` | ไม่ได้ | FK | `platform.document_lines.id` | รหัสอ้างอิง หนึ่ง line identity ในเอกสาร ไปยัง platform.document_lines.id (บทบาทฟิลด์ document_line_id) |
| `session_id` | `uuid` | ไม่ได้ | FK | `inventory.count_sessions.id` | รหัสอ้างอิง หนึ่งรอบตรวจนับ ไปยัง inventory.count_sessions.id (บทบาทฟิลด์ session_id) |
| `account_id` | `uuid` | ไม่ได้ | FK | `inventory.stock_accounts.id` | รหัสอ้างอิง หนึ่ง bucket ที่เป็น endpoint ของ ledger ไปยัง inventory.stock_accounts.id (บทบาทฟิลด์ account_id) |
| `snapshot_qty` | `numeric(20,6)` | ไม่ได้ | — | — | จำนวนตามระบบ ณ เวลาบันทึกฐานตรวจนับ; เลขทศนิยมแม่นยำ ส่ง API เป็น string ไม่คำนวณด้วย float |
| `snapshot_weight_kg` | `numeric(20,6)` | ได้ | — | — | น้ำหนักตามระบบ ณ เวลาบันทึกฐาน หน่วยกิโลกรัม; เลขทศนิยมแม่นยำ ส่ง API เป็น string ไม่คำนวณด้วย float |
| `snapshot_version` | `integer` | ไม่ได้ | — | — | รุ่นข้อมูลที่ใช้เป็นฐานเปรียบเทียบ |
| `counted_qty` | `numeric(20,6)` | ได้ | — | — | จำนวนที่นับได้จริง; เลขทศนิยมแม่นยำ ส่ง API เป็น string ไม่คำนวณด้วย float |
| `counted_weight_kg` | `numeric(20,6)` | ได้ | — | — | น้ำหนักที่นับหรือชั่งได้จริง หน่วยกิโลกรัม; เลขทศนิยมแม่นยำ ส่ง API เป็น string ไม่คำนวณด้วย float |
| `counted_by` | `uuid` | ได้ | FK | `security.users.id` | รหัสอ้างอิง หนึ่งตัวตนผู้ใช้กลาง ไปยัง security.users.id (บทบาทฟิลด์ counted_by) |
| `counted_at` | `timestamptz` | ได้ | — | — | เวลาที่นับสินค้าจริง; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `weighing_id` | `uuid` | ได้ | FK | `devices.weighings.id` | รหัสอ้างอิง หนึ่ง stable measurement หรือ authorized manual reading ไปยัง devices.weighings.id (บทบาทฟิลด์ weighing_id) |
| `created_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่สร้างแถวข้อมูลในระบบ; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `updated_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่แก้ไขแถวข้อมูลล่าสุด ต้องอัปเดตทุกช่องทางเขียน; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `version` | `integer` | ไม่ได้ | — | — | เลขรุ่นแถวสำหรับตรวจการแก้ไขพร้อมกัน |

**Keys / Index:** U(company_id,session_id,account_id); U(company_id,document_line_id)

**กฎเฉพาะ:** unknown stock creates controlled zero snapshot line while freeze active; not loose text

## `inventory.adjustment_lines`

**เฟส:** O · **หนึ่งแถวคือ:** หนึ่งผลปรับยอดที่อนุมัติ · **ประเภท:** mutable

**คำอธิบาย:** ตารางเก็บข้อมูล หนึ่งผลปรับยอดที่อนุมัติ; หนึ่งแถวมีความหมายตามนี้และอยู่ในเฟส O

| คอลัมน์ | PostgreSQL type | NULL | PK / FK | อ้างอิง | คำอธิบายภาษาไทย |
|---|---|---|---|---|---|
| `id` | `uuid` | ไม่ได้ | PK | — | รหัสหลักภายในของแถวข้อมูล ไม่เปลี่ยนตลอดอายุรายการ; Primary Key ชนิด UUID ห้ามซ้ำหรือเป็น NULL |
| `company_id` | `uuid` | ไม่ได้ | FK | `org.companies.id` | รหัสอ้างอิงบริษัทเจ้าของข้อมูล ไปยัง org.companies.id (บทบาทฟิลด์ company_id) |
| `document_line_id` | `uuid` | ไม่ได้ | FK | `platform.document_lines.id` | รหัสอ้างอิง หนึ่ง line identity ในเอกสาร ไปยัง platform.document_lines.id (บทบาทฟิลด์ document_line_id) |
| `account_id` | `uuid` | ไม่ได้ | FK | `inventory.stock_accounts.id` | รหัสอ้างอิง หนึ่ง bucket ที่เป็น endpoint ของ ledger ไปยัง inventory.stock_accounts.id (บทบาทฟิลด์ account_id) |
| `count_line_id` | `uuid` | ได้ | FK | `inventory.count_lines.id` | รหัสอ้างอิง หนึ่ง account snapshot ในรอบนับ ไปยัง inventory.count_lines.id (บทบาทฟิลด์ count_line_id) |
| `before_qty` | `numeric(20,6)` | ไม่ได้ | — | — | จำนวนก่อนปรับปรุง; เลขทศนิยมแม่นยำ ส่ง API เป็น string ไม่คำนวณด้วย float |
| `delta_qty` | `numeric(20,6)` | ไม่ได้ | — | — | ผลต่างจำนวน มีเครื่องหมายเพิ่มหรือลด; เลขทศนิยมแม่นยำ ส่ง API เป็น string ไม่คำนวณด้วย float |
| `after_qty` | `numeric(20,6)` | ไม่ได้ | — | — | จำนวนหลังปรับปรุง; เลขทศนิยมแม่นยำ ส่ง API เป็น string ไม่คำนวณด้วย float |
| `delta_weight_kg` | `numeric(20,6)` | ได้ | — | — | ผลต่างน้ำหนักกิโลกรัม มีเครื่องหมายเพิ่มหรือลด; เลขทศนิยมแม่นยำ ส่ง API เป็น string ไม่คำนวณด้วย float |
| `delta_value` | `numeric(20,6)` | ไม่ได้ | — | — | ผลต่างมูลค่า มีเครื่องหมายเพิ่มหรือลด; เลขทศนิยมแม่นยำ ส่ง API เป็น string ไม่คำนวณด้วย float |
| `reason` | `text` | ไม่ได้ | — | — | เหตุผลประกอบการดำเนินการ |
| `approval_request_id` | `uuid` | ไม่ได้ | FK | `platform.approval_requests.id` | รหัสอ้างอิง หนึ่งคำขออนุมัติ snapshot ไปยัง platform.approval_requests.id (บทบาทฟิลด์ approval_request_id) |
| `created_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่สร้างแถวข้อมูลในระบบ; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `updated_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่แก้ไขแถวข้อมูลล่าสุด ต้องอัปเดตทุกช่องทางเขียน; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `version` | `integer` | ไม่ได้ | — | — | เลขรุ่นแถวสำหรับตรวจการแก้ไขพร้อมกัน |

**Keys / Index:** U(company_id,document_line_id); partial U(company_id,count_line_id) WHERE count_line_id IS NOT NULL

**กฎเฉพาะ:** after=before+delta >=0; post version must match frozen snapshot or recount

## `withdrawal.requests`

**เฟส:** O · **หนึ่งแถวคือ:** หนึ่งคำขอเบิก · **ประเภท:** mutable

**คำอธิบาย:** ตารางเก็บข้อมูล หนึ่งคำขอเบิก; หนึ่งแถวมีความหมายตามนี้และอยู่ในเฟส O

| คอลัมน์ | PostgreSQL type | NULL | PK / FK | อ้างอิง | คำอธิบายภาษาไทย |
|---|---|---|---|---|---|
| `id` | `uuid` | ไม่ได้ | PK | — | รหัสหลักภายในของแถวข้อมูล ไม่เปลี่ยนตลอดอายุรายการ; Primary Key ชนิด UUID ห้ามซ้ำหรือเป็น NULL |
| `company_id` | `uuid` | ไม่ได้ | FK | `org.companies.id` | รหัสอ้างอิงบริษัทเจ้าของข้อมูล ไปยัง org.companies.id (บทบาทฟิลด์ company_id) |
| `document_id` | `uuid` | ไม่ได้ | FK | `platform.documents.id` | รหัสอ้างอิง หนึ่งเอกสารธุรกิจที่เป็น FK กลาง ไปยัง platform.documents.id (บทบาทฟิลด์ document_id) |
| `warehouse_id` | `uuid` | ไม่ได้ | FK | `org.warehouses.id` | รหัสอ้างอิงคลังที่เกี่ยวข้อง ไปยัง org.warehouses.id (บทบาทฟิลด์ warehouse_id) |
| `usage_point_id` | `uuid` | ไม่ได้ | FK | `org.usage_points.id` | รหัสอ้างอิง หนึ่งจุดใช้งาน/ครัว ไปยัง org.usage_points.id (บทบาทฟิลด์ usage_point_id) |
| `purpose` | `text` | ไม่ได้ | — | — | วัตถุประสงค์ของรายการ |
| `approval_request_id` | `uuid` | ได้ | FK | `platform.approval_requests.id` | รหัสอ้างอิง หนึ่งคำขออนุมัติ snapshot ไปยัง platform.approval_requests.id (บทบาทฟิลด์ approval_request_id) |
| `created_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่สร้างแถวข้อมูลในระบบ; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `updated_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่แก้ไขแถวข้อมูลล่าสุด ต้องอัปเดตทุกช่องทางเขียน; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `version` | `integer` | ไม่ได้ | — | — | เลขรุ่นแถวสำหรับตรวจการแก้ไขพร้อมกัน |

**Keys / Index:** U(company_id,document_id)

**กฎเฉพาะ:** CONSUMPTION/PROCESSING; mobile creates, management approves

## `withdrawal.request_lines`

**เฟส:** O · **หนึ่งแถวคือ:** หนึ่งสินค้าที่ขอเบิก · **ประเภท:** mutable

**คำอธิบาย:** ตารางเก็บข้อมูล หนึ่งสินค้าที่ขอเบิก; หนึ่งแถวมีความหมายตามนี้และอยู่ในเฟส O

| คอลัมน์ | PostgreSQL type | NULL | PK / FK | อ้างอิง | คำอธิบายภาษาไทย |
|---|---|---|---|---|---|
| `id` | `uuid` | ไม่ได้ | PK | — | รหัสหลักภายในของแถวข้อมูล ไม่เปลี่ยนตลอดอายุรายการ; Primary Key ชนิด UUID ห้ามซ้ำหรือเป็น NULL |
| `company_id` | `uuid` | ไม่ได้ | FK | `org.companies.id` | รหัสอ้างอิงบริษัทเจ้าของข้อมูล ไปยัง org.companies.id (บทบาทฟิลด์ company_id) |
| `document_line_id` | `uuid` | ไม่ได้ | FK | `platform.document_lines.id` | รหัสอ้างอิง หนึ่ง line identity ในเอกสาร ไปยัง platform.document_lines.id (บทบาทฟิลด์ document_line_id) |
| `request_id` | `uuid` | ไม่ได้ | FK | `withdrawal.requests.id` | รหัสอ้างอิงรหัสติดตามคำขอ API เชื่อม log และ audit ไปยัง withdrawal.requests.id (บทบาทฟิลด์ request_id) |
| `product_id` | `uuid` | ไม่ได้ | FK | `catalog.products.id` | รหัสอ้างอิงสินค้าในรายการ ไปยัง catalog.products.id (บทบาทฟิลด์ product_id) |
| `requested_qty` | `numeric(20,6)` | ไม่ได้ | — | — | จำนวนที่ร้องขอ; เลขทศนิยมแม่นยำ ส่ง API เป็น string ไม่คำนวณด้วย float |
| `requested_weight_kg` | `numeric(20,6)` | ได้ | — | — | น้ำหนักที่ร้องขอ หน่วยกิโลกรัม; เลขทศนิยมแม่นยำ ส่ง API เป็น string ไม่คำนวณด้วย float |
| `created_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่สร้างแถวข้อมูลในระบบ; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `updated_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่แก้ไขแถวข้อมูลล่าสุด ต้องอัปเดตทุกช่องทางเขียน; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `version` | `integer` | ไม่ได้ | — | — | เลขรุ่นแถวสำหรับตรวจการแก้ไขพร้อมกัน |

**Keys / Index:** U(company_id,document_line_id)

**กฎเฉพาะ:** requested vs issued separate

## `withdrawal.issue_lines`

**เฟส:** O · **หนึ่งแถวคือ:** หนึ่งการจ่ายจาก lot/package/account · **ประเภท:** mutable

**คำอธิบาย:** ตารางเก็บข้อมูล หนึ่งการจ่ายจาก lot/package/account; หนึ่งแถวมีความหมายตามนี้และอยู่ในเฟส O

| คอลัมน์ | PostgreSQL type | NULL | PK / FK | อ้างอิง | คำอธิบายภาษาไทย |
|---|---|---|---|---|---|
| `id` | `uuid` | ไม่ได้ | PK | — | รหัสหลักภายในของแถวข้อมูล ไม่เปลี่ยนตลอดอายุรายการ; Primary Key ชนิด UUID ห้ามซ้ำหรือเป็น NULL |
| `company_id` | `uuid` | ไม่ได้ | FK | `org.companies.id` | รหัสอ้างอิงบริษัทเจ้าของข้อมูล ไปยัง org.companies.id (บทบาทฟิลด์ company_id) |
| `document_line_id` | `uuid` | ไม่ได้ | FK | `platform.document_lines.id` | รหัสอ้างอิง หนึ่ง line identity ในเอกสาร ไปยัง platform.document_lines.id (บทบาทฟิลด์ document_line_id) |
| `request_line_id` | `uuid` | ไม่ได้ | FK | `withdrawal.request_lines.id` | รหัสอ้างอิง หนึ่งสินค้าที่ขอเบิก ไปยัง withdrawal.request_lines.id (บทบาทฟิลด์ request_line_id) |
| `source_account_id` | `uuid` | ไม่ได้ | FK | `inventory.stock_accounts.id` | รหัสอ้างอิงบัญชีสต็อกต้นทาง ไปยัง inventory.stock_accounts.id (บทบาทฟิลด์ source_account_id) |
| `custody_account_id` | `uuid` | ไม่ได้ | FK | `inventory.stock_accounts.id` | รหัสอ้างอิง หนึ่ง bucket ที่เป็น endpoint ของ ledger ไปยัง inventory.stock_accounts.id (บทบาทฟิลด์ custody_account_id) |
| `issued_qty` | `numeric(20,6)` | ไม่ได้ | — | — | จำนวนที่เบิกจ่ายจริง; เลขทศนิยมแม่นยำ ส่ง API เป็น string ไม่คำนวณด้วย float |
| `issued_weight_kg` | `numeric(20,6)` | ได้ | — | — | น้ำหนักที่เบิกจ่ายจริง หน่วยกิโลกรัม; เลขทศนิยมแม่นยำ ส่ง API เป็น string ไม่คำนวณด้วย float |
| `weighing_id` | `uuid` | ได้ | FK | `devices.weighings.id` | รหัสอ้างอิง หนึ่ง stable measurement หรือ authorized manual reading ไปยัง devices.weighings.id (บทบาทฟิลด์ weighing_id) |
| `fifo_override_reason` | `text` | ได้ | — | — | เหตุผลที่เลือกสินค้าไม่เป็นไปตามลำดับการหยิบปกติ |
| `created_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่สร้างแถวข้อมูลในระบบ; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `updated_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่แก้ไขแถวข้อมูลล่าสุด ต้องอัปเดตทุกช่องทางเขียน; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `version` | `integer` | ไม่ได้ | — | — | เลขรุ่นแถวสำหรับตรวจการแก้ไขพร้อมกัน |

**Keys / Index:** U(company_id,document_line_id)

**กฎเฉพาะ:** warehouse->custody once; choose FEFO locks; record system recommendation in document snapshot

## `withdrawal.consumptions`

**เฟส:** O · **หนึ่งแถวคือ:** หนึ่งปิดใช้จริงจาก custody · **ประเภท:** mutable

**คำอธิบาย:** ตารางเก็บข้อมูล หนึ่งปิดใช้จริงจาก custody; หนึ่งแถวมีความหมายตามนี้และอยู่ในเฟส O

| คอลัมน์ | PostgreSQL type | NULL | PK / FK | อ้างอิง | คำอธิบายภาษาไทย |
|---|---|---|---|---|---|
| `id` | `uuid` | ไม่ได้ | PK | — | รหัสหลักภายในของแถวข้อมูล ไม่เปลี่ยนตลอดอายุรายการ; Primary Key ชนิด UUID ห้ามซ้ำหรือเป็น NULL |
| `company_id` | `uuid` | ไม่ได้ | FK | `org.companies.id` | รหัสอ้างอิงบริษัทเจ้าของข้อมูล ไปยัง org.companies.id (บทบาทฟิลด์ company_id) |
| `document_line_id` | `uuid` | ไม่ได้ | FK | `platform.document_lines.id` | รหัสอ้างอิง หนึ่ง line identity ในเอกสาร ไปยัง platform.document_lines.id (บทบาทฟิลด์ document_line_id) |
| `issue_line_id` | `uuid` | ไม่ได้ | FK | `withdrawal.issue_lines.id` | รหัสอ้างอิง หนึ่งการจ่ายจาก lot/package/account ไปยัง withdrawal.issue_lines.id (บทบาทฟิลด์ issue_line_id) |
| `consumed_qty` | `numeric(20,6)` | ไม่ได้ | — | — | จำนวนที่ใช้จริงตามหน่วยของรายการ; เลขทศนิยมแม่นยำ ส่ง API เป็น string ไม่คำนวณด้วย float |
| `consumed_weight_kg` | `numeric(20,6)` | ได้ | — | — | น้ำหนักที่ใช้จริง หน่วยกิโลกรัม; เลขทศนิยมแม่นยำ ส่ง API เป็น string ไม่คำนวณด้วย float |
| `reason` | `text` | ได้ | — | — | เหตุผลประกอบการดำเนินการ |
| `created_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่สร้างแถวข้อมูลในระบบ; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `updated_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่แก้ไขแถวข้อมูลล่าสุด ต้องอัปเดตทุกช่องทางเขียน; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `version` | `integer` | ไม่ได้ | — | — | เลขรุ่นแถวสำหรับตรวจการแก้ไขพร้อมกัน |

**Keys / Index:** U(company_id,document_line_id)

**กฎเฉพาะ:** custody->external; ไม่ตัด warehouse ซ้ำ; close issued=consumed+returned+processing assigned+waste+remaining

## `inventory.return_lines`

**เฟส:** O · **หนึ่งแถวคือ:** หนึ่งคืนจาก custody เข้า warehouse · **ประเภท:** mutable

**คำอธิบาย:** ตารางเก็บข้อมูล หนึ่งคืนจาก custody เข้า warehouse; หนึ่งแถวมีความหมายตามนี้และอยู่ในเฟส O

| คอลัมน์ | PostgreSQL type | NULL | PK / FK | อ้างอิง | คำอธิบายภาษาไทย |
|---|---|---|---|---|---|
| `id` | `uuid` | ไม่ได้ | PK | — | รหัสหลักภายในของแถวข้อมูล ไม่เปลี่ยนตลอดอายุรายการ; Primary Key ชนิด UUID ห้ามซ้ำหรือเป็น NULL |
| `company_id` | `uuid` | ไม่ได้ | FK | `org.companies.id` | รหัสอ้างอิงบริษัทเจ้าของข้อมูล ไปยัง org.companies.id (บทบาทฟิลด์ company_id) |
| `document_line_id` | `uuid` | ไม่ได้ | FK | `platform.document_lines.id` | รหัสอ้างอิง หนึ่ง line identity ในเอกสาร ไปยัง platform.document_lines.id (บทบาทฟิลด์ document_line_id) |
| `issue_line_id` | `uuid` | ไม่ได้ | FK | `withdrawal.issue_lines.id` | รหัสอ้างอิง หนึ่งการจ่ายจาก lot/package/account ไปยัง withdrawal.issue_lines.id (บทบาทฟิลด์ issue_line_id) |
| `from_account_id` | `uuid` | ไม่ได้ | FK | `inventory.stock_accounts.id` | รหัสอ้างอิงบัญชีสต็อกต้นทาง ไปยัง inventory.stock_accounts.id (บทบาทฟิลด์ from_account_id) |
| `to_account_id` | `uuid` | ไม่ได้ | FK | `inventory.stock_accounts.id` | รหัสอ้างอิงบัญชีสต็อกปลายทาง ไปยัง inventory.stock_accounts.id (บทบาทฟิลด์ to_account_id) |
| `returned_qty` | `numeric(20,6)` | ไม่ได้ | — | — | จำนวนที่ส่งคืน; เลขทศนิยมแม่นยำ ส่ง API เป็น string ไม่คำนวณด้วย float |
| `returned_weight_kg` | `numeric(20,6)` | ได้ | — | — | น้ำหนักที่ส่งคืน หน่วยกิโลกรัม; เลขทศนิยมแม่นยำ ส่ง API เป็น string ไม่คำนวณด้วย float |
| `weighing_id` | `uuid` | ได้ | FK | `devices.weighings.id` | รหัสอ้างอิง หนึ่ง stable measurement หรือ authorized manual reading ไปยัง devices.weighings.id (บทบาทฟิลด์ weighing_id) |
| `new_expiry` | `timestamptz` | ไม่ได้ | — | — | วันเวลาหมดอายุใหม่หลังดำเนินการตามนโยบาย; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `reason` | `text` | ไม่ได้ | — | — | เหตุผลประกอบการดำเนินการ |
| `created_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่สร้างแถวข้อมูลในระบบ; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `updated_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่แก้ไขแถวข้อมูลล่าสุด ต้องอัปเดตทุกช่องทางเขียน; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `version` | `integer` | ไม่ได้ | — | — | เลขรุ่นแถวสำหรับตรวจการแก้ไขพร้อมกัน |

**Keys / Index:** U(company_id,document_line_id)

**กฎเฉพาะ:** child lot/package+genealogy; expiry <= min(original,return+24h); cost from issue; no return>custody

## `processing.process_definitions`

**เฟส:** O · **หนึ่งแถวคือ:** หนึ่งกระบวนการแปรรูป version · **ประเภท:** mutable

**คำอธิบาย:** ตารางเก็บข้อมูล หนึ่งกระบวนการแปรรูป version; หนึ่งแถวมีความหมายตามนี้และอยู่ในเฟส O

| คอลัมน์ | PostgreSQL type | NULL | PK / FK | อ้างอิง | คำอธิบายภาษาไทย |
|---|---|---|---|---|---|
| `id` | `uuid` | ไม่ได้ | PK | — | รหัสหลักภายในของแถวข้อมูล ไม่เปลี่ยนตลอดอายุรายการ; Primary Key ชนิด UUID ห้ามซ้ำหรือเป็น NULL |
| `company_id` | `uuid` | ไม่ได้ | FK | `org.companies.id` | รหัสอ้างอิงบริษัทเจ้าของข้อมูล ไปยัง org.companies.id (บทบาทฟิลด์ company_id) |
| `code` | `text` | ไม่ได้ | — | — | รหัสธุรกิจของรายการตามขอบเขต Unique ของตาราง |
| `revision` | `integer` | ไม่ได้ | — | — | หมายเลขฉบับของข้อมูล |
| `name` | `text` | ไม่ได้ | — | — | ชื่อรายการสำหรับแสดงผล |
| `yield_basis_unit_id` | `uuid` | ไม่ได้ | FK | `catalog.units.id` | รหัสอ้างอิง หนึ่งหน่วยในบริษัท ไปยัง catalog.units.id (บทบาทฟิลด์ yield_basis_unit_id) |
| `standard_yield` | `numeric(9,6)` | ได้ | — | — | อัตราผลผลิตมาตรฐาน; เลขทศนิยมแม่นยำ ส่ง API เป็น string ไม่คำนวณด้วย float |
| `min_yield` | `numeric(9,6)` | ได้ | — | — | อัตราผลผลิตต่ำสุดตามเกณฑ์; เลขทศนิยมแม่นยำ ส่ง API เป็น string ไม่คำนวณด้วย float |
| `max_yield` | `numeric(9,6)` | ได้ | — | — | อัตราผลผลิตสูงสุดตามเกณฑ์; เลขทศนิยมแม่นยำ ส่ง API เป็น string ไม่คำนวณด้วย float |
| `active` | `boolean` | ไม่ได้ | — | — | สถานะเปิดใช้งาน |
| `created_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่สร้างแถวข้อมูลในระบบ; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `updated_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่แก้ไขแถวข้อมูลล่าสุด ต้องอัปเดตทุกช่องทางเขียน; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `version` | `integer` | ไม่ได้ | — | — | เลขรุ่นแถวสำหรับตรวจการแก้ไขพร้อมกัน |

**Keys / Index:** U(company_id,code,revision)

**กฎเฉพาะ:** no BOM planning; only process/yield criteria

## `processing.jobs`

**เฟส:** O · **หนึ่งแถวคือ:** หนึ่งใบงานแปรรูป · **ประเภท:** mutable

**คำอธิบาย:** ตารางเก็บข้อมูล หนึ่งใบงานแปรรูป; หนึ่งแถวมีความหมายตามนี้และอยู่ในเฟส O

| คอลัมน์ | PostgreSQL type | NULL | PK / FK | อ้างอิง | คำอธิบายภาษาไทย |
|---|---|---|---|---|---|
| `id` | `uuid` | ไม่ได้ | PK | — | รหัสหลักภายในของแถวข้อมูล ไม่เปลี่ยนตลอดอายุรายการ; Primary Key ชนิด UUID ห้ามซ้ำหรือเป็น NULL |
| `company_id` | `uuid` | ไม่ได้ | FK | `org.companies.id` | รหัสอ้างอิงบริษัทเจ้าของข้อมูล ไปยัง org.companies.id (บทบาทฟิลด์ company_id) |
| `document_id` | `uuid` | ไม่ได้ | FK | `platform.documents.id` | รหัสอ้างอิง หนึ่งเอกสารธุรกิจที่เป็น FK กลาง ไปยัง platform.documents.id (บทบาทฟิลด์ document_id) |
| `definition_id` | `uuid` | ไม่ได้ | FK | `processing.process_definitions.id` | รหัสอ้างอิง หนึ่งกระบวนการแปรรูป version ไปยัง processing.process_definitions.id (บทบาทฟิลด์ definition_id) |
| `warehouse_id` | `uuid` | ไม่ได้ | FK | `org.warehouses.id` | รหัสอ้างอิงคลังที่เกี่ยวข้อง ไปยัง org.warehouses.id (บทบาทฟิลด์ warehouse_id) |
| `settings_snapshot` | `jsonb` | ไม่ได้ | — | — | สำเนาการตั้งค่า ณ เวลาดำเนินการ; ต้องตรวจ schema และจำกัดข้อมูลตามสิทธิ์ |
| `started_at` | `timestamptz` | ได้ | — | — | เวลาที่เริ่มดำเนินการ; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `completed_at` | `timestamptz` | ได้ | — | — | เวลาที่ดำเนินการสำเร็จ; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `actual_yield` | `numeric(9,6)` | ได้ | — | — | อัตราผลผลิตจริง; เลขทศนิยมแม่นยำ ส่ง API เป็น string ไม่คำนวณด้วย float |
| `yield_basis_input` | `numeric(20,6)` | ได้ | — | — | ปริมาณฐานขาเข้าสำหรับคำนวณผลผลิต; เลขทศนิยมแม่นยำ ส่ง API เป็น string ไม่คำนวณด้วย float |
| `yield_basis_output` | `numeric(20,6)` | ได้ | — | — | ปริมาณฐานขาออกสำหรับคำนวณผลผลิต; เลขทศนิยมแม่นยำ ส่ง API เป็น string ไม่คำนวณด้วย float |
| `approval_request_id` | `uuid` | ได้ | FK | `platform.approval_requests.id` | รหัสอ้างอิง หนึ่งคำขออนุมัติ snapshot ไปยัง platform.approval_requests.id (บทบาทฟิลด์ approval_request_id) |
| `created_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่สร้างแถวข้อมูลในระบบ; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `updated_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่แก้ไขแถวข้อมูลล่าสุด ต้องอัปเดตทุกช่องทางเขียน; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `version` | `integer` | ไม่ได้ | — | — | เลขรุ่นแถวสำหรับตรวจการแก้ไขพร้อมกัน |

**Keys / Index:** U(company_id,document_id)

**กฎเฉพาะ:** null standard ไม่เทียบ alert; output/input gross issued basis explicitly

## `processing.inputs`

**เฟส:** O · **หนึ่งแถวคือ:** หนึ่ง input lot/custody ของ job · **ประเภท:** mutable

**คำอธิบาย:** ตารางเก็บข้อมูล หนึ่ง input lot/custody ของ job; หนึ่งแถวมีความหมายตามนี้และอยู่ในเฟส O

| คอลัมน์ | PostgreSQL type | NULL | PK / FK | อ้างอิง | คำอธิบายภาษาไทย |
|---|---|---|---|---|---|
| `id` | `uuid` | ไม่ได้ | PK | — | รหัสหลักภายในของแถวข้อมูล ไม่เปลี่ยนตลอดอายุรายการ; Primary Key ชนิด UUID ห้ามซ้ำหรือเป็น NULL |
| `company_id` | `uuid` | ไม่ได้ | FK | `org.companies.id` | รหัสอ้างอิงบริษัทเจ้าของข้อมูล ไปยัง org.companies.id (บทบาทฟิลด์ company_id) |
| `document_line_id` | `uuid` | ไม่ได้ | FK | `platform.document_lines.id` | รหัสอ้างอิง หนึ่ง line identity ในเอกสาร ไปยัง platform.document_lines.id (บทบาทฟิลด์ document_line_id) |
| `job_id` | `uuid` | ไม่ได้ | FK | `processing.jobs.id` | รหัสอ้างอิง หนึ่งใบงานแปรรูป ไปยัง processing.jobs.id (บทบาทฟิลด์ job_id) |
| `issue_line_id` | `uuid` | ไม่ได้ | FK | `withdrawal.issue_lines.id` | รหัสอ้างอิง หนึ่งการจ่ายจาก lot/package/account ไปยัง withdrawal.issue_lines.id (บทบาทฟิลด์ issue_line_id) |
| `custody_account_id` | `uuid` | ไม่ได้ | FK | `inventory.stock_accounts.id` | รหัสอ้างอิง หนึ่ง bucket ที่เป็น endpoint ของ ledger ไปยัง inventory.stock_accounts.id (บทบาทฟิลด์ custody_account_id) |
| `input_qty` | `numeric(20,6)` | ไม่ได้ | — | — | จำนวนวัตถุดิบนำเข้ากระบวนการ; เลขทศนิยมแม่นยำ ส่ง API เป็น string ไม่คำนวณด้วย float |
| `input_weight_kg` | `numeric(20,6)` | ได้ | — | — | น้ำหนักวัตถุดิบเข้า หน่วยกิโลกรัม; เลขทศนิยมแม่นยำ ส่ง API เป็น string ไม่คำนวณด้วย float |
| `weighing_id` | `uuid` | ได้ | FK | `devices.weighings.id` | รหัสอ้างอิง หนึ่ง stable measurement หรือ authorized manual reading ไปยัง devices.weighings.id (บทบาทฟิลด์ weighing_id) |
| `input_value` | `numeric(20,6)` | ไม่ได้ | — | — | มูลค่าต้นทุนวัตถุดิบที่ใช้; เลขทศนิยมแม่นยำ ส่ง API เป็น string ไม่คำนวณด้วย float |
| `created_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่สร้างแถวข้อมูลในระบบ; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `updated_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่แก้ไขแถวข้อมูลล่าสุด ต้องอัปเดตทุกช่องทางเขียน; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `version` | `integer` | ไม่ได้ | — | — | เลขรุ่นแถวสำหรับตรวจการแก้ไขพร้อมกัน |

**Keys / Index:** U(company_id,document_line_id)

**กฎเฉพาะ:** allocate from issue custody; not warehouse deduct again

## `processing.outputs`

**เฟส:** O · **หนึ่งแถวคือ:** หนึ่ง output lot/package ของ job · **ประเภท:** mutable

**คำอธิบาย:** ตารางเก็บข้อมูล หนึ่ง output lot/package ของ job; หนึ่งแถวมีความหมายตามนี้และอยู่ในเฟส O

| คอลัมน์ | PostgreSQL type | NULL | PK / FK | อ้างอิง | คำอธิบายภาษาไทย |
|---|---|---|---|---|---|
| `id` | `uuid` | ไม่ได้ | PK | — | รหัสหลักภายในของแถวข้อมูล ไม่เปลี่ยนตลอดอายุรายการ; Primary Key ชนิด UUID ห้ามซ้ำหรือเป็น NULL |
| `company_id` | `uuid` | ไม่ได้ | FK | `org.companies.id` | รหัสอ้างอิงบริษัทเจ้าของข้อมูล ไปยัง org.companies.id (บทบาทฟิลด์ company_id) |
| `document_line_id` | `uuid` | ไม่ได้ | FK | `platform.document_lines.id` | รหัสอ้างอิง หนึ่ง line identity ในเอกสาร ไปยัง platform.document_lines.id (บทบาทฟิลด์ document_line_id) |
| `job_id` | `uuid` | ไม่ได้ | FK | `processing.jobs.id` | รหัสอ้างอิง หนึ่งใบงานแปรรูป ไปยัง processing.jobs.id (บทบาทฟิลด์ job_id) |
| `product_id` | `uuid` | ไม่ได้ | FK | `catalog.products.id` | รหัสอ้างอิงสินค้าในรายการ ไปยัง catalog.products.id (บทบาทฟิลด์ product_id) |
| `lot_id` | `uuid` | ไม่ได้ | FK | `inventory.lots.id` | รหัสอ้างอิง หนึ่ง lot คุณภาพ/อายุเดียวกัน ไปยัง inventory.lots.id (บทบาทฟิลด์ lot_id) |
| `package_id` | `uuid` | ได้ | FK | `inventory.packages.id` | รหัสอ้างอิง หนึ่งหน่วยห่อ/ภาชนะที่ trace ได้ ไปยัง inventory.packages.id (บทบาทฟิลด์ package_id) |
| `to_account_id` | `uuid` | ไม่ได้ | FK | `inventory.stock_accounts.id` | รหัสอ้างอิงบัญชีสต็อกปลายทาง ไปยัง inventory.stock_accounts.id (บทบาทฟิลด์ to_account_id) |
| `output_qty` | `numeric(20,6)` | ไม่ได้ | — | — | จำนวนผลผลิตที่ได้จากกระบวนการ; เลขทศนิยมแม่นยำ ส่ง API เป็น string ไม่คำนวณด้วย float |
| `output_weight_kg` | `numeric(20,6)` | ได้ | — | — | น้ำหนักผลผลิต หน่วยกิโลกรัม; เลขทศนิยมแม่นยำ ส่ง API เป็น string ไม่คำนวณด้วย float |
| `weighing_id` | `uuid` | ได้ | FK | `devices.weighings.id` | รหัสอ้างอิง หนึ่ง stable measurement หรือ authorized manual reading ไปยัง devices.weighings.id (บทบาทฟิลด์ weighing_id) |
| `allocated_value` | `numeric(20,6)` | ไม่ได้ | — | — | มูลค่าต้นทุนที่จัดสรรให้รายการ; เลขทศนิยมแม่นยำ ส่ง API เป็น string ไม่คำนวณด้วย float |
| `created_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่สร้างแถวข้อมูลในระบบ; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `updated_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่แก้ไขแถวข้อมูลล่าสุด ต้องอัปเดตทุกช่องทางเขียน; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `version` | `integer` | ไม่ได้ | — | — | เลขรุ่นแถวสำหรับตรวจการแก้ไขพร้อมกัน |

**Keys / Index:** U(company_id,document_line_id)

**กฎเฉพาะ:** multiple outputs; post cost allocation+genealogy+ledger together

## `inventory.waste_lines`

**เฟส:** O · **หนึ่งแถวคือ:** หนึ่งสูญเสีย/ทิ้งจาก account · **ประเภท:** mutable

**คำอธิบาย:** ตารางเก็บข้อมูล หนึ่งสูญเสีย/ทิ้งจาก account; หนึ่งแถวมีความหมายตามนี้และอยู่ในเฟส O

| คอลัมน์ | PostgreSQL type | NULL | PK / FK | อ้างอิง | คำอธิบายภาษาไทย |
|---|---|---|---|---|---|
| `id` | `uuid` | ไม่ได้ | PK | — | รหัสหลักภายในของแถวข้อมูล ไม่เปลี่ยนตลอดอายุรายการ; Primary Key ชนิด UUID ห้ามซ้ำหรือเป็น NULL |
| `company_id` | `uuid` | ไม่ได้ | FK | `org.companies.id` | รหัสอ้างอิงบริษัทเจ้าของข้อมูล ไปยัง org.companies.id (บทบาทฟิลด์ company_id) |
| `document_line_id` | `uuid` | ไม่ได้ | FK | `platform.document_lines.id` | รหัสอ้างอิง หนึ่ง line identity ในเอกสาร ไปยัง platform.document_lines.id (บทบาทฟิลด์ document_line_id) |
| `account_id` | `uuid` | ไม่ได้ | FK | `inventory.stock_accounts.id` | รหัสอ้างอิง หนึ่ง bucket ที่เป็น endpoint ของ ledger ไปยัง inventory.stock_accounts.id (บทบาทฟิลด์ account_id) |
| `process_input_id` | `uuid` | ได้ | FK | `processing.inputs.id` | รหัสอ้างอิง หนึ่ง input lot/custody ของ job ไปยัง processing.inputs.id (บทบาทฟิลด์ process_input_id) |
| `stock_qty` | `numeric(20,6)` | ไม่ได้ | — | — | จำนวนในหน่วยสต็อกของสินค้า; เลขทศนิยมแม่นยำ ส่ง API เป็น string ไม่คำนวณด้วย float |
| `weight_kg` | `numeric(20,6)` | ได้ | — | — | น้ำหนัก หน่วยกิโลกรัม; เลขทศนิยมแม่นยำ ส่ง API เป็น string ไม่คำนวณด้วย float |
| `reason` | `text` | ไม่ได้ | — | — | เหตุผลประกอบการดำเนินการ |
| `approval_request_id` | `uuid` | ไม่ได้ | FK | `platform.approval_requests.id` | รหัสอ้างอิง หนึ่งคำขออนุมัติ snapshot ไปยัง platform.approval_requests.id (บทบาทฟิลด์ approval_request_id) |
| `weighing_id` | `uuid` | ได้ | FK | `devices.weighings.id` | รหัสอ้างอิง หนึ่ง stable measurement หรือ authorized manual reading ไปยัง devices.weighings.id (บทบาทฟิลด์ weighing_id) |
| `created_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่สร้างแถวข้อมูลในระบบ; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `updated_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่แก้ไขแถวข้อมูลล่าสุด ต้องอัปเดตทุกช่องทางเขียน; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `version` | `integer` | ไม่ได้ | — | — | เลขรุ่นแถวสำหรับตรวจการแก้ไขพร้อมกัน |

**Keys / Index:** U(company_id,document_line_id)

**กฎเฉพาะ:** warehouse/custody/transit -> external disposal; real loss tracked; require reason/approval

## `processing.input_dispositions`

**เฟส:** O · **หนึ่งแถวคือ:** หนึ่งการจัดสรร input เป็นผลผลิต/เหลือ/สูญเสีย · **ประเภท:** mutable

**คำอธิบาย:** ตารางเก็บข้อมูล หนึ่งการจัดสรร input เป็นผลผลิต/เหลือ/สูญเสีย; หนึ่งแถวมีความหมายตามนี้และอยู่ในเฟส O

| คอลัมน์ | PostgreSQL type | NULL | PK / FK | อ้างอิง | คำอธิบายภาษาไทย |
|---|---|---|---|---|---|
| `id` | `uuid` | ไม่ได้ | PK | — | รหัสหลักภายในของแถวข้อมูล ไม่เปลี่ยนตลอดอายุรายการ; Primary Key ชนิด UUID ห้ามซ้ำหรือเป็น NULL |
| `company_id` | `uuid` | ไม่ได้ | FK | `org.companies.id` | รหัสอ้างอิงบริษัทเจ้าของข้อมูล ไปยัง org.companies.id (บทบาทฟิลด์ company_id) |
| `input_id` | `uuid` | ไม่ได้ | FK | `processing.inputs.id` | รหัสอ้างอิง หนึ่ง input lot/custody ของ job ไปยัง processing.inputs.id (บทบาทฟิลด์ input_id) |
| `output_id` | `uuid` | ได้ | FK | `processing.outputs.id` | รหัสอ้างอิง หนึ่ง output lot/package ของ job ไปยัง processing.outputs.id (บทบาทฟิลด์ output_id) |
| `return_line_id` | `uuid` | ได้ | FK | `inventory.return_lines.id` | รหัสอ้างอิง หนึ่งคืนจาก custody เข้า warehouse ไปยัง inventory.return_lines.id (บทบาทฟิลด์ return_line_id) |
| `waste_line_id` | `uuid` | ได้ | FK | `inventory.waste_lines.id` | รหัสอ้างอิง หนึ่งสูญเสีย/ทิ้งจาก account ไปยัง inventory.waste_lines.id (บทบาทฟิลด์ waste_line_id) |
| `basis_qty` | `numeric(20,6)` | ไม่ได้ | — | — | จำนวนฐานที่ใช้จัดสรรหรือคำนวณ; เลขทศนิยมแม่นยำ ส่ง API เป็น string ไม่คำนวณด้วย float |
| `allocated_value` | `numeric(20,6)` | ไม่ได้ | — | — | มูลค่าต้นทุนที่จัดสรรให้รายการ; เลขทศนิยมแม่นยำ ส่ง API เป็น string ไม่คำนวณด้วย float |
| `created_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่สร้างแถวข้อมูลในระบบ; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `updated_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่แก้ไขแถวข้อมูลล่าสุด ต้องอัปเดตทุกช่องทางเขียน; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `version` | `integer` | ไม่ได้ | — | — | เลขรุ่นแถวสำหรับตรวจการแก้ไขพร้อมกัน |

**Keys / Index:** I(company_id,input_id)

**กฎเฉพาะ:** exactly one target; conserved mass within approved loss; no double consume for returns/waste

## `purchasing.claims`

**เฟส:** O · **หนึ่งแถวคือ:** หนึ่งใบเคลม supplier · **ประเภท:** mutable

**คำอธิบาย:** ตารางเก็บข้อมูล หนึ่งใบเคลม supplier; หนึ่งแถวมีความหมายตามนี้และอยู่ในเฟส O

| คอลัมน์ | PostgreSQL type | NULL | PK / FK | อ้างอิง | คำอธิบายภาษาไทย |
|---|---|---|---|---|---|
| `id` | `uuid` | ไม่ได้ | PK | — | รหัสหลักภายในของแถวข้อมูล ไม่เปลี่ยนตลอดอายุรายการ; Primary Key ชนิด UUID ห้ามซ้ำหรือเป็น NULL |
| `company_id` | `uuid` | ไม่ได้ | FK | `org.companies.id` | รหัสอ้างอิงบริษัทเจ้าของข้อมูล ไปยัง org.companies.id (บทบาทฟิลด์ company_id) |
| `document_id` | `uuid` | ไม่ได้ | FK | `platform.documents.id` | รหัสอ้างอิง หนึ่งเอกสารธุรกิจที่เป็น FK กลาง ไปยัง platform.documents.id (บทบาทฟิลด์ document_id) |
| `supplier_id` | `uuid` | ไม่ได้ | FK | `catalog.suppliers.id` | รหัสอ้างอิงผู้ขายในรายการ ไปยัง catalog.suppliers.id (บทบาทฟิลด์ supplier_id) |
| `reason` | `text` | ไม่ได้ | — | — | เหตุผลประกอบการดำเนินการ |
| `status` | `text` | ไม่ได้ | — | — | สถานะรายการตาม state machine ของตาราง |
| `approval_request_id` | `uuid` | ได้ | FK | `platform.approval_requests.id` | รหัสอ้างอิง หนึ่งคำขออนุมัติ snapshot ไปยัง platform.approval_requests.id (บทบาทฟิลด์ approval_request_id) |
| `created_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่สร้างแถวข้อมูลในระบบ; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `updated_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่แก้ไขแถวข้อมูลล่าสุด ต้องอัปเดตทุกช่องทางเขียน; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `version` | `integer` | ไม่ได้ | — | — | เลขรุ่นแถวสำหรับตรวจการแก้ไขพร้อมกัน |

**Keys / Index:** U(company_id,document_id)

**กฎเฉพาะ:** เปิดจาก delivery issue หรือ receipt variance; financial outcome ไม่ปรับ stock เอง

## `purchasing.claim_lines`

**เฟส:** O · **หนึ่งแถวคือ:** หนึ่งรายการเคลมมีต้นทางชัด · **ประเภท:** mutable

**คำอธิบาย:** ตารางเก็บข้อมูล หนึ่งรายการเคลมมีต้นทางชัด; หนึ่งแถวมีความหมายตามนี้และอยู่ในเฟส O

| คอลัมน์ | PostgreSQL type | NULL | PK / FK | อ้างอิง | คำอธิบายภาษาไทย |
|---|---|---|---|---|---|
| `id` | `uuid` | ไม่ได้ | PK | — | รหัสหลักภายในของแถวข้อมูล ไม่เปลี่ยนตลอดอายุรายการ; Primary Key ชนิด UUID ห้ามซ้ำหรือเป็น NULL |
| `company_id` | `uuid` | ไม่ได้ | FK | `org.companies.id` | รหัสอ้างอิงบริษัทเจ้าของข้อมูล ไปยัง org.companies.id (บทบาทฟิลด์ company_id) |
| `document_line_id` | `uuid` | ไม่ได้ | FK | `platform.document_lines.id` | รหัสอ้างอิง หนึ่ง line identity ในเอกสาร ไปยัง platform.document_lines.id (บทบาทฟิลด์ document_line_id) |
| `claim_id` | `uuid` | ไม่ได้ | FK | `purchasing.claims.id` | รหัสอ้างอิง หนึ่งใบเคลม supplier ไปยัง purchasing.claims.id (บทบาทฟิลด์ claim_id) |
| `delivery_issue_id` | `uuid` | ได้ | FK | `delivery.issues.id` | รหัสอ้างอิง หนึ่งปัญหา/ส่วนที่กันไว้ของรอบส่ง ไปยัง delivery.issues.id (บทบาทฟิลด์ delivery_issue_id) |
| `receipt_variance_id` | `uuid` | ได้ | FK | `receiving.variances.id` | รหัสอ้างอิง หนึ่งข้อแตกต่างตอนชั่ง/รับจริง ไปยัง receiving.variances.id (บทบาทฟิลด์ receipt_variance_id) |
| `claimed_order_qty` | `numeric(20,6)` | ได้ | — | — | จำนวนที่เคลมในหน่วยสั่งซื้อ; เลขทศนิยมแม่นยำ ส่ง API เป็น string ไม่คำนวณด้วย float |
| `claimed_stock_qty` | `numeric(20,6)` | ได้ | — | — | จำนวนที่เคลมในหน่วยสต็อก; เลขทศนิยมแม่นยำ ส่ง API เป็น string ไม่คำนวณด้วย float |
| `claimed_amount` | `numeric(20,2)` | ไม่ได้ | — | — | จำนวนเงินที่ยื่นเคลม; เลขทศนิยมแม่นยำ ส่ง API เป็น string ไม่คำนวณด้วย float |
| `currency` | `char(3)` | ไม่ได้ | — | — | รหัสสกุลเงินของรายการ |
| `created_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่สร้างแถวข้อมูลในระบบ; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `updated_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่แก้ไขแถวข้อมูลล่าสุด ต้องอัปเดตทุกช่องทางเขียน; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `version` | `integer` | ไม่ได้ | — | — | เลขรุ่นแถวสำหรับตรวจการแก้ไขพร้อมกัน |

**Keys / Index:** U(company_id,document_line_id)

**กฎเฉพาะ:** exactly one source; qty basis explicit ห้ามบวก order qty กับ kg

## `purchasing.claim_settlements`

**เฟส:** O · **หนึ่งแถวคือ:** หนึ่งผลตกลงเคลม · **ประเภท:** append

**คำอธิบาย:** ตารางเก็บข้อมูล หนึ่งผลตกลงเคลม; หนึ่งแถวมีความหมายตามนี้และอยู่ในเฟส O

| คอลัมน์ | PostgreSQL type | NULL | PK / FK | อ้างอิง | คำอธิบายภาษาไทย |
|---|---|---|---|---|---|
| `id` | `uuid` | ไม่ได้ | PK | — | รหัสหลักภายในของแถวข้อมูล ไม่เปลี่ยนตลอดอายุรายการ; Primary Key ชนิด UUID ห้ามซ้ำหรือเป็น NULL |
| `company_id` | `uuid` | ไม่ได้ | FK | `org.companies.id` | รหัสอ้างอิงบริษัทเจ้าของข้อมูล ไปยัง org.companies.id (บทบาทฟิลด์ company_id) |
| `claim_line_id` | `uuid` | ไม่ได้ | FK | `purchasing.claim_lines.id` | รหัสอ้างอิง หนึ่งรายการเคลมมีต้นทางชัด ไปยัง purchasing.claim_lines.id (บทบาทฟิลด์ claim_line_id) |
| `kind` | `text` | ไม่ได้ | — | — | ชนิดรายการตามค่าที่อนุญาตของตาราง |
| `amount` | `numeric(20,2)` | ได้ | — | — | จำนวนเงินของรายการตามสกุลเงินที่กำหนด; เลขทศนิยมแม่นยำ ส่ง API เป็น string ไม่คำนวณด้วย float |
| `quantity` | `numeric(20,6)` | ได้ | — | — | จำนวนตามหน่วยที่อ้างอิงในรายการ; เลขทศนิยมแม่นยำ ส่ง API เป็น string ไม่คำนวณด้วย float |
| `unit_id` | `uuid` | ได้ | FK | `catalog.units.id` | รหัสอ้างอิง หนึ่งหน่วยในบริษัท ไปยัง catalog.units.id (บทบาทฟิลด์ unit_id) |
| `replacement_confirmation_line_id` | `uuid` | ได้ | FK | `delivery.confirmation_lines.id` | รหัสอ้างอิง ข้อเท็จจริงหนึ่งสินค้าต่อรอบส่ง ไปยัง delivery.confirmation_lines.id (บทบาทฟิลด์ replacement_confirmation_line_id) |
| `credit_note_file_id` | `uuid` | ได้ | FK | `platform.files.id` | รหัสอ้างอิง หนึ่ง object ส่วนตัว ไปยัง platform.files.id (บทบาทฟิลด์ credit_note_file_id) |
| `external_reference` | `text` | ได้ | — | — | เลขอ้างอิงเอกสารหรือผลจากระบบภายนอก |
| `reason` | `text` | ไม่ได้ | — | — | เหตุผลประกอบการดำเนินการ |
| `created_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่สร้างแถวข้อมูลในระบบ; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |

**Keys / Index:** I(company_id,claim_line_id)

**กฎเฉพาะ:** REFUND/CREDIT/REPLACEMENT/REJECTED; sum bounded; ไม่ใช่ AP/general ledger

## `purchasing.supplier_return_lines`

**เฟส:** O · **หนึ่งแถวคือ:** หนึ่งส่งคืน supplier จากสต็อกจริง · **ประเภท:** mutable

**คำอธิบาย:** ตารางเก็บข้อมูล หนึ่งส่งคืน supplier จากสต็อกจริง; หนึ่งแถวมีความหมายตามนี้และอยู่ในเฟส O

| คอลัมน์ | PostgreSQL type | NULL | PK / FK | อ้างอิง | คำอธิบายภาษาไทย |
|---|---|---|---|---|---|
| `id` | `uuid` | ไม่ได้ | PK | — | รหัสหลักภายในของแถวข้อมูล ไม่เปลี่ยนตลอดอายุรายการ; Primary Key ชนิด UUID ห้ามซ้ำหรือเป็น NULL |
| `company_id` | `uuid` | ไม่ได้ | FK | `org.companies.id` | รหัสอ้างอิงบริษัทเจ้าของข้อมูล ไปยัง org.companies.id (บทบาทฟิลด์ company_id) |
| `document_line_id` | `uuid` | ไม่ได้ | FK | `platform.document_lines.id` | รหัสอ้างอิง หนึ่ง line identity ในเอกสาร ไปยัง platform.document_lines.id (บทบาทฟิลด์ document_line_id) |
| `claim_line_id` | `uuid` | ไม่ได้ | FK | `purchasing.claim_lines.id` | รหัสอ้างอิง หนึ่งรายการเคลมมีต้นทางชัด ไปยัง purchasing.claim_lines.id (บทบาทฟิลด์ claim_line_id) |
| `source_account_id` | `uuid` | ไม่ได้ | FK | `inventory.stock_accounts.id` | รหัสอ้างอิงบัญชีสต็อกต้นทาง ไปยัง inventory.stock_accounts.id (บทบาทฟิลด์ source_account_id) |
| `stock_qty` | `numeric(20,6)` | ไม่ได้ | — | — | จำนวนในหน่วยสต็อกของสินค้า; เลขทศนิยมแม่นยำ ส่ง API เป็น string ไม่คำนวณด้วย float |
| `weight_kg` | `numeric(20,6)` | ได้ | — | — | น้ำหนัก หน่วยกิโลกรัม; เลขทศนิยมแม่นยำ ส่ง API เป็น string ไม่คำนวณด้วย float |
| `value` | `numeric(20,6)` | ไม่ได้ | — | — | มูลค่าหรือค่าข้อมูลตามชนิดและบริบทของตาราง; เลขทศนิยมแม่นยำ ส่ง API เป็น string ไม่คำนวณด้วย float |
| `created_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่สร้างแถวข้อมูลในระบบ; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `updated_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่แก้ไขแถวข้อมูลล่าสุด ต้องอัปเดตทุกช่องทางเขียน; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `version` | `integer` | ไม่ได้ | — | — | เลขรุ่นแถวสำหรับตรวจการแก้ไขพร้อมกัน |

**Keys / Index:** U(company_id,document_line_id)

**กฎเฉพาะ:** ต้องเป็นของรับเข้าสต็อกแล้ว; ก่อน warehouse receipt ใช้ rejection/terminal resolution ไม่มี stock deduction

## `purchasing.price_observations`

**เฟส:** P · **หนึ่งแถวคือ:** หนึ่งราคา snapshot ของ event ต้นทาง · **ประเภท:** append

**คำอธิบาย:** ตารางเก็บข้อมูล หนึ่งราคา snapshot ของ event ต้นทาง; หนึ่งแถวมีความหมายตามนี้และอยู่ในเฟส P

| คอลัมน์ | PostgreSQL type | NULL | PK / FK | อ้างอิง | คำอธิบายภาษาไทย |
|---|---|---|---|---|---|
| `id` | `uuid` | ไม่ได้ | PK | — | รหัสหลักภายในของแถวข้อมูล ไม่เปลี่ยนตลอดอายุรายการ; Primary Key ชนิด UUID ห้ามซ้ำหรือเป็น NULL |
| `company_id` | `uuid` | ไม่ได้ | FK | `org.companies.id` | รหัสอ้างอิงบริษัทเจ้าของข้อมูล ไปยัง org.companies.id (บทบาทฟิลด์ company_id) |
| `source_line_id` | `uuid` | ไม่ได้ | FK | `platform.document_lines.id` | รหัสอ้างอิง หนึ่ง line identity ในเอกสาร ไปยัง platform.document_lines.id (บทบาทฟิลด์ source_line_id) |
| `source_stage` | `text` | ไม่ได้ | — | — | ขั้นตอนต้นทาง เช่น PO ยืนยันส่งมอบ หรือรับเข้าคลัง |
| `source_version` | `integer` | ไม่ได้ | — | — | รุ่นข้อมูลต้นทาง |
| `product_id` | `uuid` | ไม่ได้ | FK | `catalog.products.id` | รหัสอ้างอิงสินค้าในรายการ ไปยัง catalog.products.id (บทบาทฟิลด์ product_id) |
| `supplier_id` | `uuid` | ไม่ได้ | FK | `catalog.suppliers.id` | รหัสอ้างอิงผู้ขายในรายการ ไปยัง catalog.suppliers.id (บทบาทฟิลด์ supplier_id) |
| `observed_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่พบหรือบันทึกเหตุการณ์ต้นทาง; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `quantity` | `numeric(20,6)` | ไม่ได้ | — | — | จำนวนตามหน่วยที่อ้างอิงในรายการ; เลขทศนิยมแม่นยำ ส่ง API เป็น string ไม่คำนวณด้วย float |
| `unit_id` | `uuid` | ไม่ได้ | FK | `catalog.units.id` | รหัสอ้างอิง หนึ่งหน่วยในบริษัท ไปยัง catalog.units.id (บทบาทฟิลด์ unit_id) |
| `unit_price` | `numeric(20,6)` | ไม่ได้ | — | — | ราคาต่อหน่วยตามหน่วยและสกุลเงินในรายการ; เลขทศนิยมแม่นยำ ส่ง API เป็น string ไม่คำนวณด้วย float |
| `currency` | `char(3)` | ไม่ได้ | — | — | รหัสสกุลเงินของรายการ |
| `net_amount` | `numeric(20,2)` | ไม่ได้ | — | — | จำนวนเงินสุทธิตามสูตรเอกสาร; เลขทศนิยมแม่นยำ ส่ง API เป็น string ไม่คำนวณด้วย float |
| `tax_basis` | `text` | ไม่ได้ | — | — | ฐานที่ใช้คำนวณภาษี |
| `normalized_unit_price` | `numeric(20,6)` | ได้ | — | — | ราคาต่อหน่วยหลังแปลงเป็นหน่วยกลางสำหรับเปรียบเทียบ; เลขทศนิยมแม่นยำ ส่ง API เป็น string ไม่คำนวณด้วย float |
| `normalized_unit_id` | `uuid` | ได้ | FK | `catalog.units.id` | รหัสอ้างอิง หนึ่งหน่วยในบริษัท ไปยัง catalog.units.id (บทบาทฟิลด์ normalized_unit_id) |
| `supersedes_id` | `uuid` | ได้ | FK | `purchasing.price_observations.id` | รหัสอ้างอิง หนึ่งราคา snapshot ของ event ต้นทาง ไปยัง purchasing.price_observations.id (บทบาทฟิลด์ supersedes_id) |
| `observation_kind` | `text` | ไม่ได้ | — | — | ชนิดบันทึกราคา เช่นสังเกตราคาหรือยกเลิกผลเดิม |
| `reverses_id` | `uuid` | ได้ | FK | `purchasing.price_observations.id` | รหัสอ้างอิง หนึ่งราคา snapshot ของ event ต้นทาง ไปยัง purchasing.price_observations.id (บทบาทฟิลด์ reverses_id) |
| `created_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่สร้างแถวข้อมูลในระบบ; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |

**Keys / Index:** U(company_id,source_line_id,source_stage,source_version); I(company_id,product_id,supplier_id,observed_at)

**กฎเฉพาะ:** PO/DELIVERY/WAREHOUSE streams ไม่ปนกัน; OBSERVE/VOID; supersedes เป็น snapshot รุ่นใหม่ ไม่รวมทุกรุ่นซ้ำ; source line registry prevents orphan

## `devices.label_templates`

**เฟส:** W · **หนึ่งแถวคือ:** หนึ่งรุ่นฉลาก · **ประเภท:** mutable

**คำอธิบาย:** ตารางเก็บข้อมูล หนึ่งรุ่นฉลาก; หนึ่งแถวมีความหมายตามนี้และอยู่ในเฟส W

| คอลัมน์ | PostgreSQL type | NULL | PK / FK | อ้างอิง | คำอธิบายภาษาไทย |
|---|---|---|---|---|---|
| `id` | `uuid` | ไม่ได้ | PK | — | รหัสหลักภายในของแถวข้อมูล ไม่เปลี่ยนตลอดอายุรายการ; Primary Key ชนิด UUID ห้ามซ้ำหรือเป็น NULL |
| `company_id` | `uuid` | ไม่ได้ | FK | `org.companies.id` | รหัสอ้างอิงบริษัทเจ้าของข้อมูล ไปยัง org.companies.id (บทบาทฟิลด์ company_id) |
| `code` | `text` | ไม่ได้ | — | — | รหัสธุรกิจของรายการตามขอบเขต Unique ของตาราง |
| `revision` | `integer` | ไม่ได้ | — | — | หมายเลขฉบับของข้อมูล |
| `locale` | `text` | ไม่ได้ | — | — | รหัสภาษาที่ใช้แสดงผล |
| `width_mm` | `numeric(10,3)` | ไม่ได้ | — | — | ความกว้างฉลาก หน่วยมิลลิเมตร; เลขทศนิยมแม่นยำ ส่ง API เป็น string ไม่คำนวณด้วย float |
| `height_mm` | `numeric(10,3)` | ไม่ได้ | — | — | ความสูงฉลาก หน่วยมิลลิเมตร; เลขทศนิยมแม่นยำ ส่ง API เป็น string ไม่คำนวณด้วย float |
| `template` | `jsonb` | ไม่ได้ | — | — | โครงสร้างฉลากที่ตรวจรูปแบบแล้ว; ต้องตรวจ schema และจำกัดข้อมูลตามสิทธิ์ |
| `active` | `boolean` | ไม่ได้ | — | — | สถานะเปิดใช้งาน |
| `created_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่สร้างแถวข้อมูลในระบบ; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `updated_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่แก้ไขแถวข้อมูลล่าสุด ต้องอัปเดตทุกช่องทางเขียน; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `version` | `integer` | ไม่ได้ | — | — | เลขรุ่นแถวสำหรับตรวจการแก้ไขพร้อมกัน |

**Keys / Index:** U(company_id,code,revision,locale)

**กฎเฉพาะ:** ใช้กฎ tenant, FK และ audit กลาง

## `devices.print_jobs`

**เฟส:** W · **หนึ่งแถวคือ:** หนึ่งงานพิมพ์/reprint · **ประเภท:** mutable

**คำอธิบาย:** ตารางเก็บข้อมูล หนึ่งงานพิมพ์/reprint; หนึ่งแถวมีความหมายตามนี้และอยู่ในเฟส W

| คอลัมน์ | PostgreSQL type | NULL | PK / FK | อ้างอิง | คำอธิบายภาษาไทย |
|---|---|---|---|---|---|
| `id` | `uuid` | ไม่ได้ | PK | — | รหัสหลักภายในของแถวข้อมูล ไม่เปลี่ยนตลอดอายุรายการ; Primary Key ชนิด UUID ห้ามซ้ำหรือเป็น NULL |
| `company_id` | `uuid` | ไม่ได้ | FK | `org.companies.id` | รหัสอ้างอิงบริษัทเจ้าของข้อมูล ไปยัง org.companies.id (บทบาทฟิลด์ company_id) |
| `template_id` | `uuid` | ไม่ได้ | FK | `devices.label_templates.id` | รหัสอ้างอิง หนึ่งรุ่นฉลาก ไปยัง devices.label_templates.id (บทบาทฟิลด์ template_id) |
| `printer_id` | `uuid` | ไม่ได้ | FK | `devices.devices.id` | รหัสอ้างอิง หนึ่งเครื่องชั่ง/เครื่องพิมพ์ ไปยัง devices.devices.id (บทบาทฟิลด์ printer_id) |
| `package_id` | `uuid` | ได้ | FK | `inventory.packages.id` | รหัสอ้างอิง หนึ่งหน่วยห่อ/ภาชนะที่ trace ได้ ไปยัง inventory.packages.id (บทบาทฟิลด์ package_id) |
| `lot_id` | `uuid` | ได้ | FK | `inventory.lots.id` | รหัสอ้างอิง หนึ่ง lot คุณภาพ/อายุเดียวกัน ไปยัง inventory.lots.id (บทบาทฟิลด์ lot_id) |
| `payload_snapshot` | `jsonb` | ไม่ได้ | — | — | สำเนาเนื้อหา ณ เวลาสร้างงาน; ต้องตรวจ schema และจำกัดข้อมูลตามสิทธิ์ |
| `requested_by` | `uuid` | ไม่ได้ | FK | `security.users.id` | รหัสอ้างอิงผู้ร้องขอ ไปยัง security.users.id (บทบาทฟิลด์ requested_by) |
| `status` | `text` | ไม่ได้ | — | — | สถานะรายการตาม state machine ของตาราง |
| `reprint_of_id` | `uuid` | ได้ | FK | `devices.print_jobs.id` | รหัสอ้างอิง หนึ่งงานพิมพ์/reprint ไปยัง devices.print_jobs.id (บทบาทฟิลด์ reprint_of_id) |
| `reprint_reason` | `text` | ได้ | — | — | เหตุผลที่พิมพ์ฉลากซ้ำ |
| `created_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่สร้างแถวข้อมูลในระบบ; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `updated_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่แก้ไขแถวข้อมูลล่าสุด ต้องอัปเดตทุกช่องทางเขียน; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `version` | `integer` | ไม่ได้ | — | — | เลขรุ่นแถวสำหรับตรวจการแก้ไขพร้อมกัน |

**Keys / Index:** I(company_id,status,created_at)

**กฎเฉพาะ:** exactly one package/lot target; reason required for reprint; retry same job not new barcode

## `devices.print_attempts`

**เฟส:** W · **หนึ่งแถวคือ:** หนึ่ง callback/attempt ของงานพิมพ์ · **ประเภท:** append

**คำอธิบาย:** ตารางเก็บข้อมูล หนึ่ง callback/attempt ของงานพิมพ์; หนึ่งแถวมีความหมายตามนี้และอยู่ในเฟส W

| คอลัมน์ | PostgreSQL type | NULL | PK / FK | อ้างอิง | คำอธิบายภาษาไทย |
|---|---|---|---|---|---|
| `id` | `uuid` | ไม่ได้ | PK | — | รหัสหลักภายในของแถวข้อมูล ไม่เปลี่ยนตลอดอายุรายการ; Primary Key ชนิด UUID ห้ามซ้ำหรือเป็น NULL |
| `company_id` | `uuid` | ไม่ได้ | FK | `org.companies.id` | รหัสอ้างอิงบริษัทเจ้าของข้อมูล ไปยัง org.companies.id (บทบาทฟิลด์ company_id) |
| `print_job_id` | `uuid` | ไม่ได้ | FK | `devices.print_jobs.id` | รหัสอ้างอิง หนึ่งงานพิมพ์/reprint ไปยัง devices.print_jobs.id (บทบาทฟิลด์ print_job_id) |
| `attempt_no` | `integer` | ไม่ได้ | — | — | ลำดับความพยายามดำเนินงาน |
| `agent_event_id` | `text` | ไม่ได้ | — | — | รหัสเหตุการณ์จากโปรแกรมประจำเครื่อง ใช้ป้องกันข้อมูลซ้ำ |
| `status` | `text` | ไม่ได้ | — | — | สถานะรายการตาม state machine ของตาราง |
| `error_code` | `text` | ได้ | — | — | รหัสข้อผิดพลาดที่เปิดเผยได้อย่างปลอดภัย |
| `acknowledged_at` | `timestamptz` | ได้ | — | — | เวลาที่ได้รับการตอบรับ; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `created_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่สร้างแถวข้อมูลในระบบ; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |

**Keys / Index:** U(company_id,print_job_id,attempt_no); U(company_id,agent_event_id)

**กฎเฉพาะ:** unknown result ไม่ auto print ซ้ำไม่จำกัด; print failure ไม่ rollback stock

## `integration.connections`

**เฟส:** F · **หนึ่งแถวคือ:** หนึ่งการเชื่อมระบบภายนอก · **ประเภท:** mutable

**คำอธิบาย:** ตารางเก็บข้อมูล หนึ่งการเชื่อมระบบภายนอก; หนึ่งแถวมีความหมายตามนี้และอยู่ในเฟส F

| คอลัมน์ | PostgreSQL type | NULL | PK / FK | อ้างอิง | คำอธิบายภาษาไทย |
|---|---|---|---|---|---|
| `id` | `uuid` | ไม่ได้ | PK | — | รหัสหลักภายในของแถวข้อมูล ไม่เปลี่ยนตลอดอายุรายการ; Primary Key ชนิด UUID ห้ามซ้ำหรือเป็น NULL |
| `company_id` | `uuid` | ไม่ได้ | FK | `org.companies.id` | รหัสอ้างอิงบริษัทเจ้าของข้อมูล ไปยัง org.companies.id (บทบาทฟิลด์ company_id) |
| `code` | `text` | ไม่ได้ | — | — | รหัสธุรกิจของรายการตามขอบเขต Unique ของตาราง |
| `provider` | `text` | ไม่ได้ | — | — | ชื่อผู้ให้บริการภายนอก |
| `secret_ref` | `text` | ไม่ได้ | — | — | ตำแหน่งอ้างอิง secret ในระบบจัดเก็บที่ปลอดภัย ไม่ใช่ตัว secret |
| `active` | `boolean` | ไม่ได้ | — | — | สถานะเปิดใช้งาน |
| `config` | `jsonb` | ไม่ได้ | — | — | การตั้งค่าที่ตรวจรูปแบบแล้ว ห้ามใส่รหัสผ่านหรือ secret; ต้องตรวจ schema และจำกัดข้อมูลตามสิทธิ์ |
| `created_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่สร้างแถวข้อมูลในระบบ; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `updated_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่แก้ไขแถวข้อมูลล่าสุด ต้องอัปเดตทุกช่องทางเขียน; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `version` | `integer` | ไม่ได้ | — | — | เลขรุ่นแถวสำหรับตรวจการแก้ไขพร้อมกัน |

**Keys / Index:** U(company_id,code)

**กฎเฉพาะ:** ไม่ใส่ secrets ใน config; ERP optional ไม่เป็น owner Master

## `integration.external_mappings`

**เฟส:** P · **หนึ่งแถวคือ:** หนึ่งรหัสต้นทางกับ internal entity · **ประเภท:** mutable

**คำอธิบาย:** ตารางเก็บข้อมูล หนึ่งรหัสต้นทางกับ internal entity; หนึ่งแถวมีความหมายตามนี้และอยู่ในเฟส P

| คอลัมน์ | PostgreSQL type | NULL | PK / FK | อ้างอิง | คำอธิบายภาษาไทย |
|---|---|---|---|---|---|
| `id` | `uuid` | ไม่ได้ | PK | — | รหัสหลักภายในของแถวข้อมูล ไม่เปลี่ยนตลอดอายุรายการ; Primary Key ชนิด UUID ห้ามซ้ำหรือเป็น NULL |
| `company_id` | `uuid` | ไม่ได้ | FK | `org.companies.id` | รหัสอ้างอิงบริษัทเจ้าของข้อมูล ไปยัง org.companies.id (บทบาทฟิลด์ company_id) |
| `connection_id` | `uuid` | ไม่ได้ | FK | `integration.connections.id` | รหัสอ้างอิง หนึ่งการเชื่อมระบบภายนอก ไปยัง integration.connections.id (บทบาทฟิลด์ connection_id) |
| `entity_kind` | `text` | ไม่ได้ | — | — | ชนิดรายการข้อมูลที่เกี่ยวข้อง |
| `external_id` | `text` | ไม่ได้ | — | — | รหัสรายการในระบบภายนอก |
| `internal_id` | `uuid` | ไม่ได้ | — | — | รหัสภายในที่จับคู่ระบบภายนอก ต้องตรวจตาม entity_kind ไม่ใช่ FK หลายตาราง |
| `source_version` | `text` | ได้ | — | — | รุ่นข้อมูลต้นทาง |
| `last_synced_at` | `timestamptz` | ได้ | — | — | เวลาที่เชื่อมข้อมูลสำเร็จล่าสุด; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `created_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่สร้างแถวข้อมูลในระบบ; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `updated_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่แก้ไขแถวข้อมูลล่าสุด ต้องอัปเดตทุกช่องทางเขียน; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `version` | `integer` | ไม่ได้ | — | — | เลขรุ่นแถวสำหรับตรวจการแก้ไขพร้อมกัน |

**Keys / Index:** U(company_id,connection_id,entity_kind,external_id)

**กฎเฉพาะ:** polymorphic mapping validate via allowlisted adapter; internal_id ไม่ใช้เป็น business FK

## `integration.import_batches`

**เฟส:** P · **หนึ่งแถวคือ:** หนึ่งชุดนำเข้า · **ประเภท:** mutable

**คำอธิบาย:** ตารางเก็บข้อมูล หนึ่งชุดนำเข้า; หนึ่งแถวมีความหมายตามนี้และอยู่ในเฟส P

| คอลัมน์ | PostgreSQL type | NULL | PK / FK | อ้างอิง | คำอธิบายภาษาไทย |
|---|---|---|---|---|---|
| `id` | `uuid` | ไม่ได้ | PK | — | รหัสหลักภายในของแถวข้อมูล ไม่เปลี่ยนตลอดอายุรายการ; Primary Key ชนิด UUID ห้ามซ้ำหรือเป็น NULL |
| `company_id` | `uuid` | ไม่ได้ | FK | `org.companies.id` | รหัสอ้างอิงบริษัทเจ้าของข้อมูล ไปยัง org.companies.id (บทบาทฟิลด์ company_id) |
| `document_id` | `uuid` | ได้ | FK | `platform.documents.id` | รหัสอ้างอิง หนึ่งเอกสารธุรกิจที่เป็น FK กลาง ไปยัง platform.documents.id (บทบาทฟิลด์ document_id) |
| `source_file_id` | `uuid` | ไม่ได้ | FK | `platform.files.id` | รหัสอ้างอิง หนึ่ง object ส่วนตัว ไปยัง platform.files.id (บทบาทฟิลด์ source_file_id) |
| `kind` | `text` | ไม่ได้ | — | — | ชนิดรายการตามค่าที่อนุญาตของตาราง |
| `status` | `text` | ไม่ได้ | — | — | สถานะรายการตาม state machine ของตาราง |
| `cutoff_at` | `timestamptz` | ไม่ได้ | — | — | เวลาตัดยอดสำหรับนำเข้าข้อมูล; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `checksum` | `text` | ไม่ได้ | — | — | ค่าตรวจสอบความถูกต้องและความซ้ำของชุดข้อมูล |
| `validated_by` | `uuid` | ได้ | FK | `security.users.id` | รหัสอ้างอิงผู้ตรวจรับ ไปยัง security.users.id (บทบาทฟิลด์ validated_by) |
| `summary` | `jsonb` | ไม่ได้ | — | — | สรุปผลการประมวลผลตาม schema; ต้องตรวจ schema และจำกัดข้อมูลตามสิทธิ์ |
| `created_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่สร้างแถวข้อมูลในระบบ; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `updated_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่แก้ไขแถวข้อมูลล่าสุด ต้องอัปเดตทุกช่องทางเขียน; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `version` | `integer` | ไม่ได้ | — | — | เลขรุ่นแถวสำหรับตรวจการแก้ไขพร้อมกัน |

**Keys / Index:** U(company_id,kind,checksum)

**กฎเฉพาะ:** dry-run/validate ก่อน commit; PO/delivery and stock opening คนละ batch

## `integration.import_rows`

**เฟส:** P · **หนึ่งแถวคือ:** หนึ่งแถว staging · **ประเภท:** mutable

**คำอธิบาย:** ตารางเก็บข้อมูล หนึ่งแถว staging; หนึ่งแถวมีความหมายตามนี้และอยู่ในเฟส P

| คอลัมน์ | PostgreSQL type | NULL | PK / FK | อ้างอิง | คำอธิบายภาษาไทย |
|---|---|---|---|---|---|
| `id` | `uuid` | ไม่ได้ | PK | — | รหัสหลักภายในของแถวข้อมูล ไม่เปลี่ยนตลอดอายุรายการ; Primary Key ชนิด UUID ห้ามซ้ำหรือเป็น NULL |
| `company_id` | `uuid` | ไม่ได้ | FK | `org.companies.id` | รหัสอ้างอิงบริษัทเจ้าของข้อมูล ไปยัง org.companies.id (บทบาทฟิลด์ company_id) |
| `batch_id` | `uuid` | ไม่ได้ | FK | `integration.import_batches.id` | รหัสอ้างอิง หนึ่งชุดนำเข้า ไปยัง integration.import_batches.id (บทบาทฟิลด์ batch_id) |
| `row_no` | `integer` | ไม่ได้ | — | — | ลำดับแถวภายในชุดนำเข้า |
| `external_key` | `text` | ไม่ได้ | — | — | กุญแจอ้างอิงแถวข้อมูลต้นทาง |
| `payload` | `jsonb` | ไม่ได้ | — | — | เนื้อหาข้อมูลตาม schema ที่กำหนด; ต้องตรวจ schema และจำกัดข้อมูลตามสิทธิ์ |
| `errors` | `jsonb` | ได้ | — | — | รายละเอียดข้อผิดพลาดที่ผ่านการกรองข้อมูลลับ; ต้องตรวจ schema และจำกัดข้อมูลตามสิทธิ์ |
| `status` | `text` | ไม่ได้ | — | — | สถานะรายการตาม state machine ของตาราง |
| `target_kind` | `text` | ได้ | — | — | ชนิดรายการปลายทาง |
| `target_id` | `uuid` | ได้ | — | — | รหัสรายการปลายทาง ต้องตรวจคู่กับ target_kind ไม่ใช่ FK หลายตาราง |
| `created_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่สร้างแถวข้อมูลในระบบ; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `updated_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่แก้ไขแถวข้อมูลล่าสุด ต้องอัปเดตทุกช่องทางเขียน; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `version` | `integer` | ไม่ได้ | — | — | เลขรุ่นแถวสำหรับตรวจการแก้ไขพร้อมกัน |

**Keys / Index:** U(company_id,batch_id,row_no); I(company_id,batch_id,status)

**กฎเฉพาะ:** payload untrusted; target registry resolver allowlist; not source of operational totals

## `integration.idempotency_keys`

**เฟส:** F · **หนึ่งแถวคือ:** หนึ่ง command request fingerprint · **ประเภท:** mutable

**คำอธิบาย:** ตารางเก็บข้อมูล หนึ่ง command request fingerprint; หนึ่งแถวมีความหมายตามนี้และอยู่ในเฟส F

| คอลัมน์ | PostgreSQL type | NULL | PK / FK | อ้างอิง | คำอธิบายภาษาไทย |
|---|---|---|---|---|---|
| `id` | `uuid` | ไม่ได้ | PK | — | รหัสหลักภายในของแถวข้อมูล ไม่เปลี่ยนตลอดอายุรายการ; Primary Key ชนิด UUID ห้ามซ้ำหรือเป็น NULL |
| `company_id` | `uuid` | ไม่ได้ | FK | `org.companies.id` | รหัสอ้างอิงบริษัทเจ้าของข้อมูล ไปยัง org.companies.id (บทบาทฟิลด์ company_id) |
| `actor_id` | `uuid` | ไม่ได้ | FK | `security.users.id` | รหัสอ้างอิงผู้ดำเนินการ ไปยัง security.users.id (บทบาทฟิลด์ actor_id) |
| `operation` | `text` | ไม่ได้ | — | — | ชื่อคำสั่งหรือกระบวนการที่ดำเนินการ |
| `key` | `text` | ไม่ได้ | — | — | กุญแจเฉพาะสำหรับระบุรายการตามบริบทตาราง |
| `payload_hash` | `text` | ไม่ได้ | — | — | ค่าแฮชของเนื้อหาที่ใช้ตรวจความซ้ำหรือการเปลี่ยนแปลง |
| `status` | `text` | ไม่ได้ | — | — | สถานะรายการตาม state machine ของตาราง |
| `result_document_id` | `uuid` | ได้ | FK | `platform.documents.id` | รหัสอ้างอิง หนึ่งเอกสารธุรกิจที่เป็น FK กลาง ไปยัง platform.documents.id (บทบาทฟิลด์ result_document_id) |
| `response_snapshot` | `jsonb` | ได้ | — | — | สำเนาผลคำสั่งสำหรับตอบซ้ำ ห้ามเก็บโทเค็นลับ; ต้องตรวจ schema และจำกัดข้อมูลตามสิทธิ์ |
| `lease_until` | `timestamptz` | ได้ | — | — | เวลาสิ้นสุดสิทธิ์ครอบครองงานชั่วคราวของ worker; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `expires_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่สิทธิ์ ข้อมูล หรือสินค้าหมดอายุตามบริบทตาราง; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `created_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่สร้างแถวข้อมูลในระบบ; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `updated_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่แก้ไขแถวข้อมูลล่าสุด ต้องอัปเดตทุกช่องทางเขียน; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `version` | `integer` | ไม่ได้ | — | — | เลขรุ่นแถวสำหรับตรวจการแก้ไขพร้อมกัน |

**Keys / Index:** U(company_id,actor_id,operation,key)

**กฎเฉพาะ:** bootstrap company idempotency แยก global table; no token response persisted

## `security.provision_requests`

**เฟส:** F · **หนึ่งแถวคือ:** หนึ่ง global request สร้างบริษัท · **ประเภท:** mutable

**คำอธิบาย:** ตารางเก็บข้อมูล หนึ่ง global request สร้างบริษัท; หนึ่งแถวมีความหมายตามนี้และอยู่ในเฟส F

| คอลัมน์ | PostgreSQL type | NULL | PK / FK | อ้างอิง | คำอธิบายภาษาไทย |
|---|---|---|---|---|---|
| `id` | `uuid` | ไม่ได้ | PK | — | รหัสหลักภายในของแถวข้อมูล ไม่เปลี่ยนตลอดอายุรายการ; Primary Key ชนิด UUID ห้ามซ้ำหรือเป็น NULL |
| `actor_id` | `uuid` | ไม่ได้ | FK | `security.users.id` | รหัสอ้างอิงผู้ดำเนินการ ไปยัง security.users.id (บทบาทฟิลด์ actor_id) |
| `idempotency_key` | `text` | ไม่ได้ | — | — | กุญแจที่ผู้เรียกส่งมาเพื่อป้องกันทำคำสั่งซ้ำ |
| `payload_hash` | `text` | ไม่ได้ | — | — | ค่าแฮชของเนื้อหาที่ใช้ตรวจความซ้ำหรือการเปลี่ยนแปลง |
| `result_company_id` | `uuid` | ได้ | FK | `org.companies.id` | รหัสอ้างอิง หนึ่งบริษัท ไปยัง org.companies.id (บทบาทฟิลด์ result_company_id) |
| `status` | `text` | ไม่ได้ | — | — | สถานะรายการตาม state machine ของตาราง |
| `expires_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่สิทธิ์ ข้อมูล หรือสินค้าหมดอายุตามบริบทตาราง; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `created_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่สร้างแถวข้อมูลในระบบ; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `updated_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่แก้ไขแถวข้อมูลล่าสุด ต้องอัปเดตทุกช่องทางเขียน; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `version` | `integer` | ไม่ได้ | — | — | เลขรุ่นแถวสำหรับตรวจการแก้ไขพร้อมกัน |

**Keys / Index:** U(actor_id,idempotency_key)

**กฎเฉพาะ:** จำเป็นก่อนมี company_id; explicit provision permission

## `integration.outbox_events`

**เฟส:** F · **หนึ่งแถวคือ:** หนึ่ง durable integration event/job intent · **ประเภท:** mutable

**คำอธิบาย:** ตารางเก็บข้อมูล หนึ่ง durable integration event/job intent; หนึ่งแถวมีความหมายตามนี้และอยู่ในเฟส F

| คอลัมน์ | PostgreSQL type | NULL | PK / FK | อ้างอิง | คำอธิบายภาษาไทย |
|---|---|---|---|---|---|
| `id` | `uuid` | ไม่ได้ | PK | — | รหัสหลักภายในของแถวข้อมูล ไม่เปลี่ยนตลอดอายุรายการ; Primary Key ชนิด UUID ห้ามซ้ำหรือเป็น NULL |
| `company_id` | `uuid` | ไม่ได้ | FK | `org.companies.id` | รหัสอ้างอิงบริษัทเจ้าของข้อมูล ไปยัง org.companies.id (บทบาทฟิลด์ company_id) |
| `event_id` | `uuid` | ไม่ได้ | — | — | รหัสเหตุการณ์ ใช้เชื่อมโยงและป้องกันประมวลผลซ้ำ |
| `event_name` | `text` | ไม่ได้ | — | — | ชื่อเหตุการณ์ธุรกิจ |
| `schema_version` | `integer` | ไม่ได้ | — | — | รุ่นโครงสร้างเนื้อหาข้อมูล |
| `aggregate_kind` | `text` | ไม่ได้ | — | — | ชนิดกลุ่มข้อมูลธุรกิจเจ้าของเหตุการณ์ |
| `aggregate_id` | `uuid` | ไม่ได้ | — | — | รหัสกลุ่มข้อมูลธุรกิจเจ้าของเหตุการณ์ ไม่ใช่ FK แบบหลายตาราง |
| `aggregate_version` | `integer` | ไม่ได้ | — | — | รุ่นของกลุ่มข้อมูลธุรกิจ ณ เวลาเกิดเหตุการณ์ |
| `correlation_id` | `uuid` | ไม่ได้ | — | — | รหัสเชื่อมโยงงานและเหตุการณ์ที่อยู่ในกระบวนการเดียวกัน |
| `occurred_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่เหตุการณ์เกิดขึ้นจริง; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `payload` | `jsonb` | ไม่ได้ | — | — | เนื้อหาข้อมูลตาม schema ที่กำหนด; ต้องตรวจ schema และจำกัดข้อมูลตามสิทธิ์ |
| `status` | `text` | ไม่ได้ | — | — | สถานะรายการตาม state machine ของตาราง |
| `attempts` | `integer` | ไม่ได้ | — | — | จำนวนครั้งที่พยายามดำเนินงาน |
| `next_attempt_at` | `timestamptz` | ไม่ได้ | — | — | เวลานัดหมายให้ลองดำเนินงานครั้งถัดไป; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `lease_until` | `timestamptz` | ได้ | — | — | เวลาสิ้นสุดสิทธิ์ครอบครองงานชั่วคราวของ worker; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `sent_at` | `timestamptz` | ได้ | — | — | เวลาที่ส่งออกสำเร็จ; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `last_error_code` | `text` | ได้ | — | — | รหัสข้อผิดพลาดล่าสุด ห้ามมีข้อมูลลับ |
| `created_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่สร้างแถวข้อมูลในระบบ; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `updated_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่แก้ไขแถวข้อมูลล่าสุด ต้องอัปเดตทุกช่องทางเขียน; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `version` | `integer` | ไม่ได้ | — | — | เลขรุ่นแถวสำหรับตรวจการแก้ไขพร้อมกัน |

**Keys / Index:** U(event_id); partial I(next_attempt_at) WHERE status IN (PENDING,RETRY)

**กฎเฉพาะ:** payload schema checked; persisted with business commit; transport metadata mutable, event identity/payload immutable

## `integration.inbox_events`

**เฟส:** F · **หนึ่งแถวคือ:** หนึ่ง event ต่อ consumer · **ประเภท:** append

**คำอธิบาย:** ตารางเก็บข้อมูล หนึ่ง event ต่อ consumer; หนึ่งแถวมีความหมายตามนี้และอยู่ในเฟส F

| คอลัมน์ | PostgreSQL type | NULL | PK / FK | อ้างอิง | คำอธิบายภาษาไทย |
|---|---|---|---|---|---|
| `id` | `uuid` | ไม่ได้ | PK | — | รหัสหลักภายในของแถวข้อมูล ไม่เปลี่ยนตลอดอายุรายการ; Primary Key ชนิด UUID ห้ามซ้ำหรือเป็น NULL |
| `company_id` | `uuid` | ไม่ได้ | FK | `org.companies.id` | รหัสอ้างอิงบริษัทเจ้าของข้อมูล ไปยัง org.companies.id (บทบาทฟิลด์ company_id) |
| `consumer_name` | `text` | ไม่ได้ | — | — | ชื่อผู้รับประมวลผลเหตุการณ์ |
| `event_id` | `uuid` | ไม่ได้ | — | — | รหัสเหตุการณ์ ใช้เชื่อมโยงและป้องกันประมวลผลซ้ำ |
| `payload_hash` | `text` | ไม่ได้ | — | — | ค่าแฮชของเนื้อหาที่ใช้ตรวจความซ้ำหรือการเปลี่ยนแปลง |
| `processed_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่ประมวลผลสำเร็จ; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `result_reference` | `jsonb` | ได้ | — | — | ข้อมูลอ้างอิงผลประมวลผล; ต้องตรวจ schema และจำกัดข้อมูลตามสิทธิ์ |
| `created_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่สร้างแถวข้อมูลในระบบ; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |

**Keys / Index:** U(company_id,consumer_name,event_id)

**กฎเฉพาะ:** insert+consumer effect same transaction; failed processing rolls back row

## `integration.deliveries`

**เฟส:** R · **หนึ่งแถวคือ:** หนึ่งความพยายามส่งออก ERP/บัญชี · **ประเภท:** mutable

**คำอธิบาย:** ตารางเก็บข้อมูล หนึ่งความพยายามส่งออก ERP/บัญชี; หนึ่งแถวมีความหมายตามนี้และอยู่ในเฟส R

| คอลัมน์ | PostgreSQL type | NULL | PK / FK | อ้างอิง | คำอธิบายภาษาไทย |
|---|---|---|---|---|---|
| `id` | `uuid` | ไม่ได้ | PK | — | รหัสหลักภายในของแถวข้อมูล ไม่เปลี่ยนตลอดอายุรายการ; Primary Key ชนิด UUID ห้ามซ้ำหรือเป็น NULL |
| `company_id` | `uuid` | ไม่ได้ | FK | `org.companies.id` | รหัสอ้างอิงบริษัทเจ้าของข้อมูล ไปยัง org.companies.id (บทบาทฟิลด์ company_id) |
| `connection_id` | `uuid` | ไม่ได้ | FK | `integration.connections.id` | รหัสอ้างอิง หนึ่งการเชื่อมระบบภายนอก ไปยัง integration.connections.id (บทบาทฟิลด์ connection_id) |
| `outbox_event_id` | `uuid` | ไม่ได้ | FK | `integration.outbox_events.id` | รหัสอ้างอิง หนึ่ง durable integration event/job intent ไปยัง integration.outbox_events.id (บทบาทฟิลด์ outbox_event_id) |
| `document_id` | `uuid` | ไม่ได้ | FK | `platform.documents.id` | รหัสอ้างอิง หนึ่งเอกสารธุรกิจที่เป็น FK กลาง ไปยัง platform.documents.id (บทบาทฟิลด์ document_id) |
| `status` | `text` | ไม่ได้ | — | — | สถานะรายการตาม state machine ของตาราง |
| `attempts` | `integer` | ไม่ได้ | — | — | จำนวนครั้งที่พยายามดำเนินงาน |
| `external_reference` | `text` | ได้ | — | — | เลขอ้างอิงเอกสารหรือผลจากระบบภายนอก |
| `request_hash` | `text` | ไม่ได้ | — | — | ค่าแฮชคำขอเพื่อป้องกันเปลี่ยนเนื้อหาระหว่าง retry |
| `last_error_code` | `text` | ได้ | — | — | รหัสข้อผิดพลาดล่าสุด ห้ามมีข้อมูลลับ |
| `next_attempt_at` | `timestamptz` | ได้ | — | — | เวลานัดหมายให้ลองดำเนินงานครั้งถัดไป; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `created_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่สร้างแถวข้อมูลในระบบ; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `updated_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่แก้ไขแถวข้อมูลล่าสุด ต้องอัปเดตทุกช่องทางเขียน; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `version` | `integer` | ไม่ได้ | — | — | เลขรุ่นแถวสำหรับตรวจการแก้ไขพร้อมกัน |

**Keys / Index:** U(company_id,connection_id,outbox_event_id)

**กฎเฉพาะ:** no direct ERP DB write; retry idempotent;ไม่ถือ HTTP202 ว่า provider accepted accounting completed

## `notification.rules`

**เฟส:** R · **หนึ่งแถวคือ:** หนึ่งกฎแจ้งเตือนต่อ scope · **ประเภท:** mutable

**คำอธิบาย:** ตารางเก็บข้อมูล หนึ่งกฎแจ้งเตือนต่อ scope; หนึ่งแถวมีความหมายตามนี้และอยู่ในเฟส R

| คอลัมน์ | PostgreSQL type | NULL | PK / FK | อ้างอิง | คำอธิบายภาษาไทย |
|---|---|---|---|---|---|
| `id` | `uuid` | ไม่ได้ | PK | — | รหัสหลักภายในของแถวข้อมูล ไม่เปลี่ยนตลอดอายุรายการ; Primary Key ชนิด UUID ห้ามซ้ำหรือเป็น NULL |
| `company_id` | `uuid` | ไม่ได้ | FK | `org.companies.id` | รหัสอ้างอิงบริษัทเจ้าของข้อมูล ไปยัง org.companies.id (บทบาทฟิลด์ company_id) |
| `code` | `text` | ไม่ได้ | — | — | รหัสธุรกิจของรายการตามขอบเขต Unique ของตาราง |
| `scope_id` | `uuid` | ไม่ได้ | FK | `security.access_scopes.id` | รหัสอ้างอิง หนึ่งขอบเขตสิทธิ์ ไปยัง security.access_scopes.id (บทบาทฟิลด์ scope_id) |
| `event_type` | `text` | ไม่ได้ | — | — | ประเภทเหตุการณ์ที่กฎนี้รองรับ |
| `config` | `jsonb` | ไม่ได้ | — | — | การตั้งค่าที่ตรวจรูปแบบแล้ว ห้ามใส่รหัสผ่านหรือ secret; ต้องตรวจ schema และจำกัดข้อมูลตามสิทธิ์ |
| `active` | `boolean` | ไม่ได้ | — | — | สถานะเปิดใช้งาน |
| `created_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่สร้างแถวข้อมูลในระบบ; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `updated_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่แก้ไขแถวข้อมูลล่าสุด ต้องอัปเดตทุกช่องทางเขียน; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `version` | `integer` | ไม่ได้ | — | — | เลขรุ่นแถวสำหรับตรวจการแก้ไขพร้อมกัน |

**Keys / Index:** U(company_id,scope_id,code)

**กฎเฉพาะ:** PO overdue/low stock/expiry/yield/claim/integration error

## `notification.notifications`

**เฟส:** R · **หนึ่งแถวคือ:** หนึ่งข้อความต่อ user/event · **ประเภท:** mutable

**คำอธิบาย:** ตารางเก็บข้อมูล หนึ่งข้อความต่อ user/event; หนึ่งแถวมีความหมายตามนี้และอยู่ในเฟส R

| คอลัมน์ | PostgreSQL type | NULL | PK / FK | อ้างอิง | คำอธิบายภาษาไทย |
|---|---|---|---|---|---|
| `id` | `uuid` | ไม่ได้ | PK | — | รหัสหลักภายในของแถวข้อมูล ไม่เปลี่ยนตลอดอายุรายการ; Primary Key ชนิด UUID ห้ามซ้ำหรือเป็น NULL |
| `company_id` | `uuid` | ไม่ได้ | FK | `org.companies.id` | รหัสอ้างอิงบริษัทเจ้าของข้อมูล ไปยัง org.companies.id (บทบาทฟิลด์ company_id) |
| `recipient_id` | `uuid` | ไม่ได้ | FK | `security.users.id` | รหัสอ้างอิง หนึ่งตัวตนผู้ใช้กลาง ไปยัง security.users.id (บทบาทฟิลด์ recipient_id) |
| `outbox_event_id` | `uuid` | ได้ | FK | `integration.outbox_events.id` | รหัสอ้างอิง หนึ่ง durable integration event/job intent ไปยัง integration.outbox_events.id (บทบาทฟิลด์ outbox_event_id) |
| `rule_id` | `uuid` | ได้ | FK | `notification.rules.id` | รหัสอ้างอิง หนึ่งกฎแจ้งเตือนต่อ scope ไปยัง notification.rules.id (บทบาทฟิลด์ rule_id) |
| `dedupe_key` | `text` | ไม่ได้ | — | — | กุญแจป้องกันสร้างรายการซ้ำ |
| `locale` | `text` | ไม่ได้ | — | — | รหัสภาษาที่ใช้แสดงผล |
| `title` | `text` | ไม่ได้ | — | — | หัวข้อข้อความ |
| `body` | `text` | ไม่ได้ | — | — | เนื้อหาข้อความ |
| `document_id` | `uuid` | ได้ | FK | `platform.documents.id` | รหัสอ้างอิง หนึ่งเอกสารธุรกิจที่เป็น FK กลาง ไปยัง platform.documents.id (บทบาทฟิลด์ document_id) |
| `read_at` | `timestamptz` | ได้ | — | — | เวลาที่ผู้รับอ่านข้อความ; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `created_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่สร้างแถวข้อมูลในระบบ; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `updated_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่แก้ไขแถวข้อมูลล่าสุด ต้องอัปเดตทุกช่องทางเขียน; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `version` | `integer` | ไม่ได้ | — | — | เลขรุ่นแถวสำหรับตรวจการแก้ไขพร้อมกัน |

**Keys / Index:** U(company_id,recipient_id,dedupe_key)

**กฎเฉพาะ:** ตรวจสิทธิ์ก่อนแสดง/deep link; no sensitive payload in public push

## `notification.attempts`

**เฟส:** R · **หนึ่งแถวคือ:** หนึ่งการส่ง notification ผ่าน channel · **ประเภท:** append

**คำอธิบาย:** ตารางเก็บข้อมูล หนึ่งการส่ง notification ผ่าน channel; หนึ่งแถวมีความหมายตามนี้และอยู่ในเฟส R

| คอลัมน์ | PostgreSQL type | NULL | PK / FK | อ้างอิง | คำอธิบายภาษาไทย |
|---|---|---|---|---|---|
| `id` | `uuid` | ไม่ได้ | PK | — | รหัสหลักภายในของแถวข้อมูล ไม่เปลี่ยนตลอดอายุรายการ; Primary Key ชนิด UUID ห้ามซ้ำหรือเป็น NULL |
| `company_id` | `uuid` | ไม่ได้ | FK | `org.companies.id` | รหัสอ้างอิงบริษัทเจ้าของข้อมูล ไปยัง org.companies.id (บทบาทฟิลด์ company_id) |
| `notification_id` | `uuid` | ไม่ได้ | FK | `notification.notifications.id` | รหัสอ้างอิง หนึ่งข้อความต่อ user/event ไปยัง notification.notifications.id (บทบาทฟิลด์ notification_id) |
| `channel` | `text` | ไม่ได้ | — | — | ช่องทางการส่งหรือสื่อสาร |
| `attempt_no` | `integer` | ไม่ได้ | — | — | ลำดับความพยายามดำเนินงาน |
| `status` | `text` | ไม่ได้ | — | — | สถานะรายการตาม state machine ของตาราง |
| `provider_message_id` | `text` | ได้ | — | — | รหัสข้อความจากผู้ให้บริการ |
| `error_code` | `text` | ได้ | — | — | รหัสข้อผิดพลาดที่เปิดเผยได้อย่างปลอดภัย |
| `sent_at` | `timestamptz` | ได้ | — | — | เวลาที่ส่งออกสำเร็จ; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `created_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่สร้างแถวข้อมูลในระบบ; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |

**Keys / Index:** U(company_id,notification_id,channel,attempt_no)

**กฎเฉพาะ:** retry/retention; append outcomes

## `reporting.export_jobs`

**เฟส:** R · **หนึ่งแถวคือ:** หนึ่ง export ตามสิทธิ์ ณ เวลาขอ · **ประเภท:** mutable

**คำอธิบาย:** ตารางเก็บข้อมูล หนึ่ง export ตามสิทธิ์ ณ เวลาขอ; หนึ่งแถวมีความหมายตามนี้และอยู่ในเฟส R

| คอลัมน์ | PostgreSQL type | NULL | PK / FK | อ้างอิง | คำอธิบายภาษาไทย |
|---|---|---|---|---|---|
| `id` | `uuid` | ไม่ได้ | PK | — | รหัสหลักภายในของแถวข้อมูล ไม่เปลี่ยนตลอดอายุรายการ; Primary Key ชนิด UUID ห้ามซ้ำหรือเป็น NULL |
| `company_id` | `uuid` | ไม่ได้ | FK | `org.companies.id` | รหัสอ้างอิงบริษัทเจ้าของข้อมูล ไปยัง org.companies.id (บทบาทฟิลด์ company_id) |
| `requested_by` | `uuid` | ไม่ได้ | FK | `security.users.id` | รหัสอ้างอิงผู้ร้องขอ ไปยัง security.users.id (บทบาทฟิลด์ requested_by) |
| `report_code` | `text` | ไม่ได้ | — | — | รหัสรายงานที่ขอประมวลผล |
| `filters` | `jsonb` | ไม่ได้ | — | — | เงื่อนไขกรองข้อมูลที่ตรวจสิทธิ์และรูปแบบแล้ว; ต้องตรวจ schema และจำกัดข้อมูลตามสิทธิ์ |
| `authorized_scope_snapshot` | `jsonb` | ไม่ได้ | — | — | สำเนาขอบเขตข้อมูลที่ผู้ขอได้รับอนุญาต; ต้องตรวจ schema และจำกัดข้อมูลตามสิทธิ์ |
| `status` | `text` | ไม่ได้ | — | — | สถานะรายการตาม state machine ของตาราง |
| `as_of` | `timestamptz` | ได้ | — | — | เวลาที่ข้อมูลสรุปมีผลล่าสุด; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `output_file_id` | `uuid` | ได้ | FK | `platform.files.id` | รหัสอ้างอิง หนึ่ง object ส่วนตัว ไปยัง platform.files.id (บทบาทฟิลด์ output_file_id) |
| `expires_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่สิทธิ์ ข้อมูล หรือสินค้าหมดอายุตามบริบทตาราง; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `error_code` | `text` | ได้ | — | — | รหัสข้อผิดพลาดที่เปิดเผยได้อย่างปลอดภัย |
| `created_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่สร้างแถวข้อมูลในระบบ; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `updated_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่แก้ไขแถวข้อมูลล่าสุด ต้องอัปเดตทุกช่องทางเขียน; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `version` | `integer` | ไม่ได้ | — | — | เลขรุ่นแถวสำหรับตรวจการแก้ไขพร้อมกัน |

**Keys / Index:** I(company_id,requested_by,created_at)

**กฎเฉพาะ:** ตรวจสิทธิ์ซ้ำตอนทำ/ดาวน์โหลด ไม่เชื่อ snapshot เป็น authority ถาวร

## `reporting.refresh_runs`

**เฟส:** R · **หนึ่งแถวคือ:** หนึ่ง aggregate refresh · **ประเภท:** mutable

**คำอธิบาย:** ตารางเก็บข้อมูล หนึ่ง aggregate refresh; หนึ่งแถวมีความหมายตามนี้และอยู่ในเฟส R

| คอลัมน์ | PostgreSQL type | NULL | PK / FK | อ้างอิง | คำอธิบายภาษาไทย |
|---|---|---|---|---|---|
| `id` | `uuid` | ไม่ได้ | PK | — | รหัสหลักภายในของแถวข้อมูล ไม่เปลี่ยนตลอดอายุรายการ; Primary Key ชนิด UUID ห้ามซ้ำหรือเป็น NULL |
| `company_id` | `uuid` | ไม่ได้ | FK | `org.companies.id` | รหัสอ้างอิงบริษัทเจ้าของข้อมูล ไปยัง org.companies.id (บทบาทฟิลด์ company_id) |
| `view_name` | `text` | ไม่ได้ | — | — | ชื่อ view ที่อนุญาตสำหรับอ่านข้อมูล |
| `started_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่เริ่มดำเนินการ; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `finished_at` | `timestamptz` | ได้ | — | — | เวลาที่งานสิ้นสุด; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `watermark` | `timestamptz` | ได้ | — | — | จุดเวลาที่ประมวลผลข้อมูลสรุปครอบคลุมถึง; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `status` | `text` | ไม่ได้ | — | — | สถานะรายการตาม state machine ของตาราง |
| `error_code` | `text` | ได้ | — | — | รหัสข้อผิดพลาดที่เปิดเผยได้อย่างปลอดภัย |
| `created_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่สร้างแถวข้อมูลในระบบ; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `updated_at` | `timestamptz` | ไม่ได้ | — | — | เวลาที่แก้ไขแถวข้อมูลล่าสุด ต้องอัปเดตทุกช่องทางเขียน; เป็นเวลาเหตุการณ์จริง เก็บ UTC ส่ง API เป็น ISO 8601 มี Z แสดงตาม timezone ธุรกิจ เช่น Asia/Bangkok |
| `version` | `integer` | ไม่ได้ | — | — | เลขรุ่นแถวสำหรับตรวจการแก้ไขพร้อมกัน |

**Keys / Index:** I(company_id,view_name,started_at)

**กฎเฉพาะ:** allowlisted view ไม่ dynamic SQL user input; dashboard freshness
