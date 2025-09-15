# Project WeWeigh Requirements
### Connect :
- Bluetooth
    - Scale 
    - Printer
- Wi-Fi
    - database to sync data

## Requirement tree
<!-- ```bash
project_wewigh/
├── requirements.md
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── utils.py
│   └── models/
│       ├── __init__.py
│       ├── model_a.py
│       └── model_b.py
├── tests/
│   ├── __init__.py
│   ├── test_main.py
│   └── test_utils.py
└── README.md
``` -->

## Functional Requirements

### Weigh
### SKU
- Show all SKU
- Search SKU by name, barcode
- Add SKU to the system
- Update SKU details
- Delete SKU from the system
### High, Low by SKU
- Show high and low weight SKUs
### Count
- คือแสดงจำนวนนับสินค้านับจากน้ำหนัก
### Label print
- Print labels for SKUs


### Alarm
- ตั้งค่าเลือก เสียงเตือน เมื่อ High, Low, Count ,OFF ,ON
- Auto Record เมื่ออยู่ในช่วง High, Low


### M Plus
- คือการบันทึกแบบแมนวล

### Report and History
- Show history of weighings (เอาตามเดิม)
- เมื่อ Export ให้จัดเรียงจากเก่าไปใหม่ (1 - 20)
- Export history to CSV
- Export history to xlsx

### Mode
    - Auto record when stable
    - Auto record when stable and in controlled range high, low


## Devices 
### Scale
- connect to scale
- list available scales
- previously connected scales

### Printer
- connect to printer
- list available printers
- previously connected printers

### Account Management
- My account data 
- List of users
- Add new user
- Update user details
- Delete user from the system

## Version Control
- Easy Offline Mode
- Easy Online Mode
- Formula Online (Manual) Mode


## Materials
### SKU
- CRUD (Create, Read, Update, Delete) operations for SKU


### 