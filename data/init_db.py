import os
import sqlite3

DB_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(DB_DIR, "farm_twin.db")


def init_database():
    print(f"Initializing database at: {DB_PATH}")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 1. Create Farmers table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS farmers (
        farmer_id TEXT PRIMARY KEY,
        name TEXT,
        language TEXT
    )
    """)

    # 2. Create Fields table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS fields (
        field_id TEXT PRIMARY KEY,
        farmer_id TEXT,
        name TEXT,
        soil_type TEXT,
        acres REAL,
        irrigation_type TEXT,
        FOREIGN KEY(farmer_id) REFERENCES farmers(farmer_id)
    )
    """)

    # 3. Create Plantings table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS plantings (
        planting_id TEXT PRIMARY KEY,
        field_id TEXT,
        crop_type TEXT,
        variety TEXT,
        planting_date TEXT,
        stage TEXT,
        nitrogen_ppm REAL,
        moisture_pct REAL,
        health_pct REAL,
        FOREIGN KEY(field_id) REFERENCES fields(field_id)
    )
    """)

    # 4. Create Activities table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS activities (
        activity_id TEXT PRIMARY KEY,
        planting_id TEXT,
        activity_type TEXT,
        quantity REAL,
        unit TEXT,
        details TEXT,
        timestamp TEXT,
        synced INTEGER,
        FOREIGN KEY(planting_id) REFERENCES plantings(planting_id)
    )
    """)

    # 5. Create Farm Plans table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS farm_plans (
        plan_id TEXT PRIMARY KEY,
        planting_id TEXT,
        title TEXT,
        reason TEXT,
        urgency TEXT,
        recommended_time TEXT,
        field TEXT,
        source TEXT,
        command_action TEXT,
        state TEXT,
        timestamp TEXT,
        FOREIGN KEY(planting_id) REFERENCES plantings(planting_id)
    )
    """)

    # 6. Create Reminders table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS reminders (
        reminder_id TEXT PRIMARY KEY,
        planting_id TEXT,
        type TEXT,
        title TEXT,
        reason TEXT,
        recommended_time TEXT,
        source TEXT,
        state TEXT,
        timestamp TEXT,
        FOREIGN KEY(planting_id) REFERENCES plantings(planting_id)
    )
    """)

    # 7. Create Escalations table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS escalations (
        escalation_id TEXT PRIMARY KEY,
        planting_id TEXT,
        farmer_question TEXT,
        language TEXT,
        translated_summary TEXT,
        field_context TEXT,
        crop_context TEXT,
        evidence TEXT,
        images TEXT,
        diagnosis_result TEXT,
        confidence REAL,
        safety_flags TEXT,
        recent_activities TEXT,
        state TEXT,
        expert_response TEXT,
        timestamp TEXT,
        FOREIGN KEY(planting_id) REFERENCES plantings(planting_id)
    )
    """)

    # 8. Create Feedbacks table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS feedbacks (
        feedback_id TEXT PRIMARY KEY,
        planting_id TEXT,
        followed_recommendation INTEGER,
        outcome TEXT,
        time_to_outcome TEXT,
        comment TEXT,
        image_path TEXT,
        farmer_confidence REAL,
        timestamp TEXT,
        FOREIGN KEY(planting_id) REFERENCES plantings(planting_id)
    )
    """)

    # 9. Create Regional Outbreaks table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS regional_outbreaks (
        outbreak_id TEXT PRIMARY KEY,
        crop TEXT,
        pest_symptom TEXT,
        region TEXT,
        case_count INTEGER,
        status TEXT, -- signal_detected, under_review, confirmed, dismissed, expired
        expert_verified INTEGER DEFAULT 0,
        timestamp TEXT
    )
    """)

    # 10. Create OKF Governance table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS okf_governance (
        content_id TEXT PRIMARY KEY,
        version INTEGER,
        region TEXT,
        crop TEXT,
        crop_variety TEXT,
        language TEXT,
        source_organization TEXT,
        reviewer TEXT,
        approval_status TEXT, -- draft, review, approved, published, deprecated, withdrawn
        effective_date TEXT,
        expiration_date TEXT,
        safety_category TEXT,
        evidence_references TEXT,
        previous_version_content TEXT
    )
    """)

    # 11. Create Observability Logs table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS observability_logs (
        log_id INTEGER PRIMARY KEY AUTOINCREMENT,
        correlation_id TEXT,
        event_type TEXT,
        screen TEXT,
        agent TEXT,
        tool TEXT,
        route TEXT, -- local, cloud
        safety_decision TEXT,
        latency REAL,
        device_tier TEXT,
        timestamp TEXT
    )
    """)

    # 12. Create Privacy Preferences table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS privacy_preferences (
        user_id TEXT PRIMARY KEY,
        location_sharing INTEGER DEFAULT 1,
        image_retention INTEGER DEFAULT 1,
        voice_retention INTEGER DEFAULT 1,
        expert_consultation_sharing INTEGER DEFAULT 1,
        regional_outbreak_participation INTEGER DEFAULT 1,
        analytics_participation INTEGER DEFAULT 1
    )
    """)

    # 13. Create Sync DLQ table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sync_dlq (
        dlq_id INTEGER PRIMARY KEY AUTOINCREMENT,
        planting_id TEXT,
        payload TEXT,
        error_message TEXT,
        retry_count INTEGER,
        timestamp TEXT
    )
    """)

    # 14. Insert Default Mock Data
    cursor.execute(
        "INSERT OR REPLACE INTO farmers VALUES ('user', 'Nalin Giri', 'Hindi')"
    )

    # Fields
    cursor.execute(
        "INSERT OR REPLACE INTO fields VALUES ('field_1', 'user', 'North Hillside', 'Black Clay (Cotton Soil)', 5.0, 'Drip')"
    )
    cursor.execute(
        "INSERT OR REPLACE INTO fields VALUES ('field_2', 'user', 'Riverbed Meadow', 'Red Sandy Loam', 8.0, 'Sprinkler')"
    )

    # Plantings
    cursor.execute(
        "INSERT OR REPLACE INTO plantings VALUES ('planting_1', 'field_1', 'Corn', 'PMH-1', '2026-06-01', 'germination', 45.0, 40.0, 100.0)"
    )
    cursor.execute(
        "INSERT OR REPLACE INTO plantings VALUES ('planting_2', 'field_2', 'Wheat', 'Lokwan', '2026-06-10', 'vegetative', 55.0, 45.0, 95.0)"
    )

    # Activities
    cursor.execute(
        "INSERT OR REPLACE INTO activities VALUES ('act_1', 'planting_1', 'irrigation', 2.0, 'hours', 'Irrigated North field', '2026-06-25 08:00:00', 1)"
    )
    cursor.execute(
        "INSERT OR REPLACE INTO activities VALUES ('act_2', 'planting_1', 'fertilization', 10.0, 'kg', 'Applied Urea nitrogen fertilizer', '2026-06-26 09:30:00', 1)"
    )

    # Farm Plans
    cursor.execute(
        "INSERT OR REPLACE INTO farm_plans VALUES ('plan_1', 'planting_1', 'Irrigate North Field', 'Soil moisture low (34%)', 'high', 'before 9 AM', 'North Hillside', 'Agronomist Guideline', 'irrigation_planner', 'active', '2026-07-02 06:00:00')"
    )
    cursor.execute(
        "INSERT OR REPLACE INTO farm_plans VALUES ('plan_2', 'planting_2', 'Pest Inspection', 'High risk of Aphids forecast due to temperature rise', 'medium', '2:00 PM', 'Riverbed Meadow', 'Edge AI Diagnosis Model', 'pest_alert', 'active', '2026-07-02 06:00:00')"
    )
    cursor.execute(
        "INSERT OR REPLACE INTO farm_plans VALUES ('plan_3', 'planting_1', 'Postponed Fertilizer Application', 'High wind speed alert (18 km/h) prevents safe chemical spray', 'low', 'evening', 'North Hillside', 'Safety Kernel', 'none', 'active', '2026-07-02 06:00:00')"
    )

    # Reminders
    cursor.execute(
        "INSERT OR REPLACE INTO reminders VALUES ('rem_1', 'planting_1', 'irrigation', 'Water Tomato Crop', 'Fruit development water requirements', '08:00 AM', 'Drip Irrigation Controller', 'active', '2026-07-02 06:00:00')"
    )
    cursor.execute(
        "INSERT OR REPLACE INTO reminders VALUES ('rem_2', 'planting_2', 'pest inspection', 'Check Leaf Spots', 'Common Rust warning from nearby fields', '04:00 PM', 'Agronomist Team', 'active', '2026-07-02 06:00:00')"
    )

    # Seed Regional Outbreaks
    cursor.execute(
        "INSERT OR REPLACE INTO regional_outbreaks VALUES ('out_1', 'Corn', 'yellow margins', 'Nagpur', 4, 'under_review', 0, '2026-07-02 06:00:00')"
    )
    cursor.execute(
        "INSERT OR REPLACE INTO regional_outbreaks VALUES ('out_2', 'Wheat', 'leaf rust', 'Nagpur', 6, 'confirmed', 1, '2026-07-02 06:00:00')"
    )

    # Seed OKF Governance versioning
    cursor.execute("""
    INSERT OR REPLACE INTO okf_governance VALUES (
        'gov_1', 1, 'Nagpur', 'Corn', 'PMH-1', 'Hindi', 'ICAR', 'Dr. Ramesh', 'approved',
        '2026-06-01', '2027-06-01', 'Fertilization', 'ICAR Bulletin 42', '{}'
    )
    """)

    # Seed Privacy Preferences
    cursor.execute(
        "INSERT OR REPLACE INTO privacy_preferences VALUES ('user', 1, 1, 1, 1, 1, 1)"
    )

    conn.commit()
    conn.close()
    print("Database initialization completed successfully.")


if __name__ == "__main__":
    init_database()
