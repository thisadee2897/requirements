# ER Diagram - Flutter + Supabase Weighing System

## Database Schema Overview

ระบบการชั่งน้ำหนักและการจัดการข้อมูล SKU พร้อม Integration กับ ERP

---

## 1. Core Tables

### 1.1 SKU (Stock Keeping Unit)
```sql
CREATE TABLE sku (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tsmf_part_number VARCHAR(50) UNIQUE NOT NULL,
    customer_part_number VARCHAR(50),
    part_name VARCHAR(255) NOT NULL,
    material_grade VARCHAR(100),
    customer_name VARCHAR(255),
    weight_per_piece DECIMAL(10,4) NOT NULL,
    pcs_per_packaging INTEGER NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    is_active BOOLEAN DEFAULT TRUE
);
```

### 1.2 Container
```sql
CREATE TABLE container (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    container_id VARCHAR(20) UNIQUE NOT NULL, -- S001, B001
    container_name VARCHAR(100),
    weight DECIMAL(8,3) NOT NULL, -- container weight in kg
    container_type VARCHAR(50), -- small, big, custom
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    is_active BOOLEAN DEFAULT TRUE
);
```

### 1.3 User Management
```sql
CREATE TABLE user_profile (
    id UUID PRIMARY KEY REFERENCES auth.users(id),
    name VARCHAR(255) NOT NULL,
    role VARCHAR(20) CHECK (role IN ('operator', 'qc', 'admin', 'supervisor')),
    employee_id VARCHAR(50) UNIQUE,
    department VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    is_active BOOLEAN DEFAULT TRUE
);
```

---

## 2. Transaction & Weighing Tables

### 2.1 Weighing Transaction (Main Log)
```sql
CREATE TABLE weighing_transaction (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    transaction_no VARCHAR(50) UNIQUE NOT NULL, -- WGH-20250915-001
    date_time TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    -- FK References
    sku_id UUID REFERENCES sku(id) NOT NULL,
    container_id UUID REFERENCES container(id) NOT NULL,
    user_id UUID REFERENCES user_profile(id) NOT NULL,
    
    -- Weight Data
    gross_weight DECIMAL(10,3) NOT NULL,
    container_weight DECIMAL(8,3) NOT NULL,
    net_weight DECIMAL(10,3) GENERATED ALWAYS AS (gross_weight - container_weight) STORED,
    calculated_pieces INTEGER GENERATED ALWAYS AS (
        CASE 
            WHEN (SELECT weight_per_piece FROM sku WHERE id = sku_id) > 0 
            THEN ROUND((gross_weight - container_weight) / (SELECT weight_per_piece FROM sku WHERE id = sku_id))
            ELSE 0 
        END
    ) STORED,
    
    -- Production Data
    delivery_date DATE,
    lot_no VARCHAR(50),
    raw_batch VARCHAR(50),
    cic_no VARCHAR(11), -- 11 digits
    
    -- QC Status
    qc_status VARCHAR(20) DEFAULT 'pending' CHECK (qc_status IN ('pending', 'pass', 'fail', 'review')),
    qc_notes TEXT,
    qc_checked_by UUID REFERENCES user_profile(id),
    qc_checked_at TIMESTAMP WITH TIME ZONE,
    
    -- Label Status
    label_printed BOOLEAN DEFAULT FALSE,
    label_printed_at TIMESTAMP WITH TIME ZONE,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

---

## 3. QC & Configuration Tables

### 3.1 QC Configuration
```sql
CREATE TABLE qc_config (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    sku_id UUID REFERENCES sku(id) NOT NULL,
    
    -- Weight Range Check
    weight_tolerance_percent DECIMAL(5,2) DEFAULT 5.0,
    min_weight_per_piece DECIMAL(10,4),
    max_weight_per_piece DECIMAL(10,4),
    
    -- Piece Count Range
    min_pieces_allowed INTEGER,
    max_pieces_allowed INTEGER,
    
    -- Alert Settings
    enable_weight_alert BOOLEAN DEFAULT TRUE,
    enable_piece_alert BOOLEAN DEFAULT TRUE,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    UNIQUE(sku_id)
);
```

### 3.2 Label Template
```sql
CREATE TABLE label_template (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    template_name VARCHAR(100) NOT NULL,
    template_type VARCHAR(50) DEFAULT '10x6cm',
    
    -- Template Content (JSON Format)
    template_json JSONB NOT NULL,
    /* Example JSON:
    {
        "size": {"width": 100, "height": 60},
        "fields": [
            {"type": "text", "label": "Part No:", "field": "tsmf_part_number", "x": 5, "y": 5},
            {"type": "text", "label": "Weight:", "field": "net_weight", "x": 5, "y": 15},
            {"type": "qr", "field": "transaction_id", "x": 70, "y": 5, "size": 25}
        ]
    }
    */
    
    is_default BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

---

## 4. Integration & Audit Tables

### 4.1 Scale Configuration
```sql
CREATE TABLE scale_config (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    scale_name VARCHAR(100) NOT NULL,
    connection_type VARCHAR(20) CHECK (connection_type IN ('serial', 'tcp', 'bluetooth', 'usb')),
    connection_params JSONB, -- {port, baudRate, ip, etc.}
    scale_model VARCHAR(100),
    max_capacity DECIMAL(10,3),
    precision_decimal INTEGER DEFAULT 3,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

### 4.2 System Audit Log
```sql
CREATE TABLE audit_log (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    table_name VARCHAR(100) NOT NULL,
    record_id UUID NOT NULL,
    action VARCHAR(20) CHECK (action IN ('INSERT', 'UPDATE', 'DELETE')),
    old_values JSONB,
    new_values JSONB,
    user_id UUID REFERENCES user_profile(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

### 4.3 ERP Integration Log
```sql
CREATE TABLE erp_sync_log (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    transaction_id UUID REFERENCES weighing_transaction(id),
    sync_type VARCHAR(50), -- 'webhook', 'api_push', 'file_export'
    sync_status VARCHAR(20) DEFAULT 'pending' CHECK (sync_status IN ('pending', 'success', 'failed', 'retry')),
    request_data JSONB,
    response_data JSONB,
    error_message TEXT,
    retry_count INTEGER DEFAULT 0,
    next_retry_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    synced_at TIMESTAMP WITH TIME ZONE
);
```

---

## 5. Indexes & Performance

```sql
-- Performance Indexes
CREATE INDEX idx_weighing_transaction_date ON weighing_transaction(date_time);
CREATE INDEX idx_weighing_transaction_sku ON weighing_transaction(sku_id);
CREATE INDEX idx_weighing_transaction_user ON weighing_transaction(user_id);
CREATE INDEX idx_weighing_transaction_cic ON weighing_transaction(cic_no);
CREATE INDEX idx_sku_part_number ON sku(tsmf_part_number);
CREATE INDEX idx_container_id ON container(container_id);

-- Full-text search
CREATE INDEX idx_sku_search ON sku USING gin(to_tsvector('english', part_name || ' ' || customer_name));
```

---

## 6. Views & Functions

### 6.1 Transaction Summary View
```sql
CREATE VIEW v_transaction_summary AS
SELECT 
    wt.id,
    wt.transaction_no,
    wt.date_time,
    s.tsmf_part_number,
    s.part_name,
    s.customer_name,
    c.container_id,
    wt.gross_weight,
    wt.net_weight,
    wt.calculated_pieces,
    wt.delivery_date,
    wt.lot_no,
    wt.cic_no,
    wt.qc_status,
    up.name as operator_name,
    wt.label_printed
FROM weighing_transaction wt
JOIN sku s ON wt.sku_id = s.id
JOIN container c ON wt.container_id = c.id
JOIN user_profile up ON wt.user_id = up.id
WHERE s.is_active = TRUE;
```

### 6.2 QC Alert Function
```sql
CREATE OR REPLACE FUNCTION check_qc_alerts(transaction_id UUID)
RETURNS TABLE(alert_type VARCHAR, message TEXT) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        'WEIGHT_OUT_OF_RANGE'::VARCHAR,
        'Weight per piece is outside acceptable range'::TEXT
    FROM weighing_transaction wt
    JOIN sku s ON wt.sku_id = s.id
    JOIN qc_config qc ON s.id = qc.sku_id
    WHERE wt.id = transaction_id
    AND (
        (wt.net_weight / wt.calculated_pieces) < qc.min_weight_per_piece
        OR (wt.net_weight / wt.calculated_pieces) > qc.max_weight_per_piece
    );
    
    RETURN QUERY
    SELECT 
        'PIECE_COUNT_ALERT'::VARCHAR,
        'Piece count is outside expected range'::TEXT
    FROM weighing_transaction wt
    JOIN qc_config qc ON wt.sku_id = qc.sku_id
    WHERE wt.id = transaction_id
    AND (
        wt.calculated_pieces < qc.min_pieces_allowed
        OR wt.calculated_pieces > qc.max_pieces_allowed
    );
END;
$$ LANGUAGE plpgsql;
```

---

## 7. Row Level Security (RLS)

```sql
-- Enable RLS
ALTER TABLE weighing_transaction ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_profile ENABLE ROW LEVEL SECURITY;

-- Policies
CREATE POLICY "Users can view own transactions" ON weighing_transaction
    FOR SELECT USING (user_id = auth.uid());

CREATE POLICY "Admins can view all transactions" ON weighing_transaction
    FOR ALL USING (
        EXISTS (
            SELECT 1 FROM user_profile 
            WHERE id = auth.uid() AND role IN ('admin', 'supervisor')
        )
    );
```

---

## 8. ER Diagram Visual Representation

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│      SKU        │    │   CONTAINER     │    │  USER_PROFILE   │
├─────────────────┤    ├─────────────────┤    ├─────────────────┤
│ id (PK)         │    │ id (PK)         │    │ id (PK,FK)      │
│ tsmf_part_no    │    │ container_id    │    │ name            │
│ customer_part   │    │ container_name  │    │ role            │
│ part_name       │    │ weight          │    │ employee_id     │
│ material_grade  │    │ container_type  │    │ department      │
│ customer_name   │    │ is_active       │    │ is_active       │
│ weight_per_piece│    └─────────────────┘    └─────────────────┘
│ pcs_per_pkg     │              │                      │
│ is_active       │              │                      │
└─────────────────┘              │                      │
         │                       │                      │
         │                       │                      │
         ▼                       ▼                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                    WEIGHING_TRANSACTION                         │
├─────────────────────────────────────────────────────────────────┤
│ id (PK)                    │ delivery_date                      │
│ transaction_no             │ lot_no                             │
│ date_time                  │ raw_batch                          │
│ sku_id (FK)               │ cic_no                             │
│ container_id (FK)         │ qc_status                          │
│ user_id (FK)              │ qc_notes                           │
│ gross_weight              │ qc_checked_by (FK)                 │
│ container_weight          │ qc_checked_at                      │
│ net_weight (computed)     │ label_printed                      │
│ calculated_pieces (comp)  │ label_printed_at                   │
└─────────────────────────────────────────────────────────────────┘
         │                       │                      │
         ▼                       ▼                      ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   QC_CONFIG     │    │ LABEL_TEMPLATE  │    │  ERP_SYNC_LOG   │
├─────────────────┤    ├─────────────────┤    ├─────────────────┤
│ id (PK)         │    │ id (PK)         │    │ id (PK)         │
│ sku_id (FK)     │    │ template_name   │    │ transaction_id  │
│ weight_tolerance│    │ template_type   │    │ sync_type       │
│ min_weight      │    │ template_json   │    │ sync_status     │
│ max_weight      │    │ is_default      │    │ request_data    │
│ min_pieces      │    └─────────────────┘    │ response_data   │
│ max_pieces      │                           │ error_message   │
│ enable_alerts   │                           │ retry_count     │
└─────────────────┘                           └─────────────────┘
```

---

## 9. Sample Data Migration

```sql
-- Sample SKU Data
INSERT INTO sku (tsmf_part_number, customer_part_number, part_name, material_grade, customer_name, weight_per_piece, pcs_per_packaging) VALUES
('TSMF-001', 'CUST-A001', 'Bolt M6x20', 'SS304', 'Customer A', 0.025, 100),
('TSMF-002', 'CUST-A002', 'Nut M6', 'SS316', 'Customer A', 0.015, 200),
('TSMF-003', 'CUST-B001', 'Washer 6mm', 'Carbon Steel', 'Customer B', 0.008, 500);

-- Sample Container Data
INSERT INTO container (container_id, container_name, weight, container_type) VALUES
('S001', 'Small Container 1', 0.250, 'small'),
('S002', 'Small Container 2', 0.245, 'small'),
('B001', 'Big Container 1', 0.850, 'big'),
('B002', 'Big Container 2', 0.855, 'big');

-- Sample QC Config
INSERT INTO qc_config (sku_id, weight_tolerance_percent, min_pieces_allowed, max_pieces_allowed) 
SELECT id, 5.0, 50, 150 FROM sku WHERE tsmf_part_number = 'TSMF-001';
```

---

## 10. Development Phases Implementation

### Phase 1: Core Schema ✅
- [x] SKU, Container, User, Transaction tables
- [x] Basic relationships and constraints
- [x] Essential indexes

### Phase 2: QC & Scale Integration
- [ ] QC Config table and functions
- [ ] Scale configuration
- [ ] Alert system implementation

### Phase 3: Reporting & Integration
- [ ] Views and reporting functions
- [ ] ERP sync tables
- [ ] Label template system
- [ ] Audit logging

---

**Next Steps:**
1. สร้าง Supabase project และ run schema นี้
2. ทดสอบ basic CRUD operations
3. เริ่มพัฒนา Flutter app ที่ connect กับ schema นี้