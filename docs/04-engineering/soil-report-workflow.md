# Soil Report Workflow

> **Status:** Active
> **Last Updated:** 2026-07-04
> **Owner:** Engineering

---

## Overview

The Soil Test Report feature allows farmers to input soil test data (from a lab report) and receive color-coded interpretations and fertilizer recommendations.

## User Flow

```
🧪 मिट्टी जांच (Soil Test nav)
    │
    ├── 📄 रिपोर्ट अपलोड करें (Upload Report)
    │     → PDF or photo upload
    │     → (OCR extraction — planned)
    │
    ├── 📷 रिपोर्ट की फोटो लें (Camera Capture)
    │     → Camera viewfinder
    │     → (OCR extraction — planned)
    │
    └── ✏️ मान खुद भरें (Manual Entry)
          → Form with 13 fields
          → Select field from dropdown
          → Fill values
          → Save
                │
                ▼
         Summary Screen
         ├── 🟢/🟡/🔴 Color-coded interpretations
         ├── Expandable details (pH, N, P, K, OC values)
         ├── "खाद सलाह देखें" (Fertilizer Advice) button
         └── "मिट्टी सुधार सुझाव" (Soil Amendment) button
```

## Manual Entry Form

### Fields (13)

| Field | Label (Hindi) | Label (English) | Type | Placeholder |
|-------|---------------|-----------------|------|--------------|
| Field | खेत | Field | Dropdown | खेत चुनें |
| Report Date | रिपोर्ट तारीख | Report Date | Text | पता नहीं |
| Lab Name | लैब का नाम | Lab Name | Text | पता नहीं |
| Soil Type | मिट्टी का प्रकार | Soil Type | Text | पता नहीं |
| pH | pH | pH | Number | पता नहीं |
| EC | EC | EC | Number | पता नहीं |
| Organic Carbon | जैविक कार्बन | Organic Carbon | Number | पता नहीं |
| Nitrogen | नाइट्रोजन | Nitrogen | Number | पता नहीं |
| Phosphorus | फॉस्फोरस | Phosphorus | Number | पता नहीं |
| Potassium | पोटाश | Potassium | Number | पता नहीं |
| Sulfur | सल्फर | Sulfur | Number | पता नहीं |
| Zinc | जिंक | Zinc | Number | पता नहीं |
| Boron | बोरोन | Boron | Number | पता नहीं |
| Iron | आयरन | Iron | Number | पता नहीं |

### Validation

- Field selection is required (shows toast "⚠️ खेत चुनें" if not selected)
- Numeric values are optional (placeholder "पता नहीं" = unknown)
- All values can be left as "पता नहीं" if the lab report doesn't include them

## Interpretation Logic

| Parameter | Low | Normal | High |
|-----------|-----|--------|------|
| pH | <5.5 (अम्लीय) | 5.5–7.5 (संतुलित) | >7.5 (क्षारीय) |
| Nitrogen (kg/ha) | <140 | 140–280 | >280 |
| Phosphorus (kg/ha) | <10 | 10–25 | >25 |
| Potassium (kg/ha) | <110 | 110–280 | >280 |
| Organic Carbon (%) | <0.5 | 0.5–0.75 | >0.75 |

### Color Coding

- 🟢 **Green** — Parameter is in normal range
- 🟡 **Yellow** — Parameter is low (needs amendment)
- 🔴 **Red** — Parameter is critically low or high

## API Endpoints

| Endpoint | Method | Request Body | Response |
|----------|--------|---------------|----------|
| `/api/soil/save` | POST | `{ field_id, sample_date, lab_name, soil_type, values: { ph, ec, ... } }` | `{ report_id, status }` |
| `/api/soil/latest/{field_id}` | GET | — | `{ report_id, sample_date, values, interpretation }` |
| `/api/soil/reports/{field_id}` | GET | — | `[{ report_id, sample_date, values }, ...]` |

## Database Schema

```sql
CREATE TABLE soil_reports (
    report_id TEXT PRIMARY KEY,
    field_id TEXT NOT NULL,
    sample_date TEXT,
    lab_name TEXT,
    soil_type_reported TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (field_id) REFERENCES fields(field_id)
);

CREATE TABLE soil_test_values (
    report_id TEXT PRIMARY KEY,
    ph REAL,
    ec REAL,
    organic_carbon REAL,
    nitrogen REAL,
    phosphorus REAL,
    potassium REAL,
    sulfur REAL,
    zinc REAL,
    boron REAL,
    iron REAL,
    FOREIGN KEY (report_id) REFERENCES soil_reports(report_id)
);
```

## Key Files

| File | Purpose |
|------|---------|
| `ui/agui/dashboard.js` | Soil test screen rendering, form, summary, interpretation |
| `ui/agui/index.html` | Soil test screen HTML (4 sub-screens) |
| `app/fast_api_app.py` | Soil API endpoints (`/api/soil/*`) |
| `data/db_manager.py` | `init_soil_tables()`, `save_soil_report()`, `get_soil_reports()`, `get_latest_soil_report()` |

## Related Documents

- [Development Guide](development-guide.md)
- [Data & Farm Twin Architecture](../02-architecture/data-and-farm-twin-architecture.md)
- [Functional Requirements](../01-product/functional-requirements.md) (REQ-AAA-009)