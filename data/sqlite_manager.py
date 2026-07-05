import os
import sqlite3
import uuid
from datetime import datetime

DB_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(DB_DIR, "farm_twin.db")


def get_connection():
    return sqlite3.connect(DB_PATH)


def get_profile_data(farmer_id="user"):
    """
    Fetches the farmer's profile, including all fields and their active crop plantings.
    """
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    try:
        # Get farmer info
        cursor.execute("SELECT * FROM farmers WHERE farmer_id = ?", (farmer_id,))
        farmer = cursor.fetchone()
        if not farmer:
            # Fallback/Auto-create default user
            cursor.execute(
                "INSERT INTO farmers VALUES (?, ?, ?)", (farmer_id, "Farmer", "Hindi")
            )
            conn.commit()
            cursor.execute("SELECT * FROM farmers WHERE farmer_id = ?", (farmer_id,))
            farmer = cursor.fetchone()

        profile = {
            "farmer_id": farmer["farmer_id"],
            "name": farmer["name"],
            "language": farmer["language"],
            "fields": [],
        }

        # Get fields
        cursor.execute("SELECT * FROM fields WHERE farmer_id = ?", (farmer_id,))
        fields = cursor.fetchall()

        for field in fields:
            field_data = {
                "field_id": field["field_id"],
                "name": field["name"],
                "soil_type": field["soil_type"],
                "acres": field["acres"],
                "irrigation_type": field["irrigation_type"],
                "planting": None,
            }

            # Get active crop planting for this field
            cursor.execute(
                "SELECT * FROM plantings WHERE field_id = ?", (field["field_id"],)
            )
            planting = cursor.fetchone()
            if planting:
                field_data["planting"] = {
                    "planting_id": planting["planting_id"],
                    "crop_type": planting["crop_type"],
                    "variety": planting["variety"],
                    "planting_date": planting["planting_date"],
                    "stage": planting["stage"],
                    "nitrogen_ppm": planting["nitrogen_ppm"],
                    "moisture_pct": planting["moisture_pct"],
                    "health_pct": planting["health_pct"],
                }

            profile["fields"].append(field_data)

        return profile
    finally:
        conn.close()


def save_farmer_field(
    farmer_id,
    name,
    soil_type,
    acres,
    irrigation_type,
    crop_type,
    variety="Default",
    stage="germination",
):
    """
    Adds a new field and seeds an initial crop planting record for it.
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        field_id = f"field_{uuid.uuid4().hex[:8]}"
        planting_id = f"planting_{uuid.uuid4().hex[:8]}"
        planting_date = datetime.now().strftime("%Y-%m-%d")

        # Insert Field
        cursor.execute(
            "INSERT INTO fields VALUES (?, ?, ?, ?, ?, ?)",
            (field_id, farmer_id, name, soil_type, float(acres), irrigation_type),
        )

        # Insert Planting
        cursor.execute(
            "INSERT INTO plantings VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                planting_id,
                field_id,
                crop_type,
                variety,
                planting_date,
                stage,
                40.0,
                45.0,
                100.0,
            ),
        )

        conn.commit()
        return {"field_id": field_id, "planting_id": planting_id}
    finally:
        conn.close()


def update_planting_telemetry(planting_id, moisture_pct, health_pct, nitrogen_ppm):
    """
    Updates the physical telemetry readings for a specific crop planting.
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            UPDATE plantings
            SET moisture_pct = ?, health_pct = ?, nitrogen_ppm = ?
            WHERE planting_id = ?
            """,
            (float(moisture_pct), float(health_pct), float(nitrogen_ppm), planting_id),
        )
        conn.commit()
        return True
    finally:
        conn.close()


def log_activity_record(
    planting_id, activity_type, quantity, unit, details, timestamp=None
):
    """
    Logs a new farming activity record (irrigation, fertilization, etc.).
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        activity_id = f"act_{uuid.uuid4().hex[:8]}"
        if not timestamp:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute(
            "INSERT INTO activities VALUES (?, ?, ?, ?, ?, ?, ?, 1)",
            (
                activity_id,
                planting_id,
                activity_type,
                float(quantity),
                unit,
                details,
                timestamp,
            ),
        )
        conn.commit()
        return {"activity_id": activity_id, "status": "success"}
    finally:
        conn.close()


def get_activities_log(planting_id):
    """
    Retrieves logged activities for a specific crop planting.
    """
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT * FROM activities WHERE planting_id = ? ORDER BY timestamp DESC",
            (planting_id,),
        )
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()


def get_daily_plans(planting_id):
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT * FROM farm_plans WHERE planting_id = ? ORDER BY timestamp DESC",
            (planting_id,),
        )
        return [dict(row) for row in cursor.fetchall()]
    finally:
        conn.close()


def update_plan_state(plan_id, state):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE farm_plans SET state = ? WHERE plan_id = ?", (state, plan_id)
        )
        conn.commit()
        return True
    finally:
        conn.close()


def get_reminders(planting_id):
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT * FROM reminders WHERE planting_id = ? ORDER BY timestamp DESC",
            (planting_id,),
        )
        return [dict(row) for row in cursor.fetchall()]
    finally:
        conn.close()


def update_reminder_state(reminder_id, state):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE reminders SET state = ? WHERE reminder_id = ?", (state, reminder_id)
        )
        conn.commit()
        return True
    finally:
        conn.close()


def save_escalation_request(esc):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        esc_id = esc.get("escalation_id") or f"esc_{uuid.uuid4().hex[:8]}"
        timestamp = esc.get("timestamp") or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute(
            """
            INSERT OR REPLACE INTO escalations VALUES
            (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                esc_id,
                esc.get("planting_id", "planting_1"),
                esc.get("farmer_question", ""),
                esc.get("language", "English"),
                esc.get("translated_summary", ""),
                esc.get("field_context", ""),
                esc.get("crop_context", ""),
                esc.get("evidence", ""),
                esc.get("images", ""),
                esc.get("diagnosis_result", ""),
                float(esc.get("confidence", 1.0)),
                esc.get("safety_flags", ""),
                esc.get("recent_activities", ""),
                esc.get("state", "draft"),
                esc.get("expert_response", ""),
                timestamp,
            ),
        )
        conn.commit()
        return {"escalation_id": esc_id, "status": "success"}
    finally:
        conn.close()


def get_escalations(planting_id):
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT * FROM escalations WHERE planting_id = ? ORDER BY timestamp DESC",
            (planting_id,),
        )
        return [dict(row) for row in cursor.fetchall()]
    finally:
        conn.close()


def log_outcome_feedback(f):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        feedback_id = f.get("feedback_id") or f"feed_{uuid.uuid4().hex[:8]}"
        timestamp = f.get("timestamp") or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute(
            "INSERT INTO feedbacks VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                feedback_id,
                f.get("planting_id", "planting_1"),
                int(f.get("followed_recommendation", 1)),
                f.get("outcome", ""),
                f.get("time_to_outcome", ""),
                f.get("comment", ""),
                f.get("image_path", ""),
                float(f.get("farmer_confidence", 1.0)),
                timestamp,
            ),
        )
        conn.commit()
        return {"feedback_id": feedback_id, "status": "success"}
    finally:
        conn.close()


# Phase 5 Helpers


def get_expert_queue() -> list:
    """Retrieve all escalations for the agronomist queue."""
    conn = get_connection()
    try:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM escalations ORDER BY timestamp DESC")
        return [dict(row) for row in cursor.fetchall()]
    finally:
        conn.close()


def update_expert_case_state(
    escalation_id: str, state: str, expert_response: str = None
) -> dict:
    """Update state and response of an expert escalation."""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        if expert_response is not None:
            cursor.execute(
                "UPDATE escalations SET state = ?, expert_response = ? WHERE escalation_id = ?",
                (state, expert_response, escalation_id),
            )
        else:
            cursor.execute(
                "UPDATE escalations SET state = ? WHERE escalation_id = ?",
                (state, escalation_id),
            )
        conn.commit()
        return {"status": "success"}
    finally:
        conn.close()


def get_outbreaks() -> list:
    """Retrieve regional outbreaks."""
    conn = get_connection()
    try:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM regional_outbreaks ORDER BY timestamp DESC")
        return [dict(row) for row in cursor.fetchall()]
    finally:
        conn.close()


def confirm_outbreak(outbreak_id: str, status: str) -> dict:
    """Update outbreak verification and status."""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE regional_outbreaks SET status = ?, expert_verified = 1 WHERE outbreak_id = ?",
            (status, outbreak_id),
        )
        conn.commit()
        return {"status": "success"}
    finally:
        conn.close()


def get_governance_metadata() -> list:
    """Retrieve OKF knowledge governance records."""
    conn = get_connection()
    try:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM okf_governance")
        return [dict(row) for row in cursor.fetchall()]
    finally:
        conn.close()


def rollback_governance_version(content_id: str) -> dict:
    """Rollback governance content to previous version."""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        # Simply decrement version or mark as deprecated
        cursor.execute(
            "SELECT version FROM okf_governance WHERE content_id = ?", (content_id,)
        )
        row = cursor.fetchone()
        if row:
            v = row[0]
            if v > 1:
                cursor.execute(
                    "UPDATE okf_governance SET version = ?, approval_status = 'approved' WHERE content_id = ?",
                    (v - 1, content_id),
                )
            else:
                cursor.execute(
                    "UPDATE okf_governance SET approval_status = 'withdrawn' WHERE content_id = ?",
                    (content_id,),
                )
            conn.commit()
            return {"status": "success"}
        return {"status": "error", "message": "Content not found"}
    finally:
        conn.close()


def log_observability_event(
    correlation_id: str,
    event_type: str,
    screen: str = "",
    agent: str = "",
    tool: str = "",
    route: str = "",
    safety_decision: str = "",
    latency: float = 0.0,
    device_tier: str = "",
) -> dict:
    """Save an observability trace log event."""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO observability_logs (correlation_id, event_type, screen, agent, tool, route, safety_decision, latency, device_tier, timestamp) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now'))",
            (
                correlation_id,
                event_type,
                screen,
                agent,
                tool,
                route,
                safety_decision,
                latency,
                device_tier,
            ),
        )
        conn.commit()
        return {"status": "success"}
    finally:
        conn.close()


def get_observability_logs() -> list:
    """Retrieve the latest 50 observability logs."""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT correlation_id, event_type, screen, route, latency, timestamp FROM observability_logs ORDER BY timestamp DESC LIMIT 50"
        )
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]
    finally:
        conn.close()


def save_privacy_preferences(payload: dict) -> dict:
    """Save privacy consent settings."""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT OR REPLACE INTO privacy_preferences VALUES (?, ?, ?, ?, ?, ?, ?)",
            (
                payload.get("user_id", "user"),
                int(payload.get("location_sharing", 1)),
                int(payload.get("image_retention", 1)),
                int(payload.get("voice_retention", 1)),
                int(payload.get("expert_consultation_sharing", 1)),
                int(payload.get("regional_outbreak_participation", 1)),
                int(payload.get("analytics_participation", 1)),
            ),
        )
        conn.commit()
        return {"status": "success"}
    finally:
        conn.close()


def delete_farm_data(user_id: str) -> dict:
    """Purge all personal data for a user across all Twin tables."""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM farmers WHERE farmer_id = ?", (user_id,))
        cursor.execute("DELETE FROM privacy_preferences WHERE user_id = ?", (user_id,))
        # Find plantings for this farmer
        cursor.execute(
            "SELECT planting_id FROM plantings WHERE field_id IN (SELECT field_id FROM fields WHERE farmer_id = ?)",
            (user_id,),
        )
        plantings = [r[0] for r in cursor.fetchall()]
        for p in plantings:
            cursor.execute("DELETE FROM activities WHERE planting_id = ?", (p,))
            cursor.execute("DELETE FROM farm_plans WHERE planting_id = ?", (p,))
            cursor.execute("DELETE FROM reminders WHERE planting_id = ?", (p,))
            cursor.execute("DELETE FROM escalations WHERE planting_id = ?", (p,))
            cursor.execute("DELETE FROM feedbacks WHERE planting_id = ?", (p,))
        cursor.execute(
            "DELETE FROM plantings WHERE field_id IN (SELECT field_id FROM fields WHERE farmer_id = ?)",
            (user_id,),
        )
        cursor.execute("DELETE FROM fields WHERE farmer_id = ?", (user_id,))
        conn.commit()
        return {"status": "success"}
    finally:
        conn.close()


def export_farm_data(user_id: str) -> dict:
    """Retrieve complete structural archive of user farm data."""
    conn = get_connection()
    try:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        data = {}
        cursor.execute("SELECT * FROM farmers WHERE farmer_id = ?", (user_id,))
        data["farmer"] = [dict(r) for r in cursor.fetchall()]
        cursor.execute("SELECT * FROM fields WHERE farmer_id = ?", (user_id,))
        data["fields"] = [dict(r) for r in cursor.fetchall()]
        cursor.execute(
            "SELECT * FROM privacy_preferences WHERE user_id = ?", (user_id,)
        )
        data["privacy"] = [dict(r) for r in cursor.fetchall()]

        # Get plantings
        cursor.execute(
            "SELECT * FROM plantings WHERE field_id IN (SELECT field_id FROM fields WHERE farmer_id = ?)",
            (user_id,),
        )
        plantings = [dict(r) for r in cursor.fetchall()]
        data["plantings"] = plantings

        planting_ids = [p["planting_id"] for p in plantings]
        if planting_ids:
            placeholders = ",".join("?" for _ in planting_ids)
            cursor.execute(
                f"SELECT * FROM activities WHERE planting_id IN ({placeholders})",
                planting_ids,
            )
            data["activities"] = [dict(r) for r in cursor.fetchall()]
            cursor.execute(
                f"SELECT * FROM farm_plans WHERE planting_id IN ({placeholders})",
                planting_ids,
            )
            data["plans"] = [dict(r) for r in cursor.fetchall()]
            cursor.execute(
                f"SELECT * FROM reminders WHERE planting_id IN ({placeholders})",
                planting_ids,
            )
            data["reminders"] = [dict(r) for r in cursor.fetchall()]
            cursor.execute(
                f"SELECT * FROM escalations WHERE planting_id IN ({placeholders})",
                planting_ids,
            )
            data["escalations"] = [dict(r) for r in cursor.fetchall()]
            cursor.execute(
                f"SELECT * FROM feedbacks WHERE planting_id IN ({placeholders})",
                planting_ids,
            )
            data["feedbacks"] = [dict(r) for r in cursor.fetchall()]
        else:
            data["activities"] = []
            data["plans"] = []
            data["reminders"] = []
            data["escalations"] = []
            data["feedbacks"] = []
        return data
    finally:
        conn.close()


# ============================================================
# Soil Test Report — Database Functions
# ============================================================


def init_soil_tables():
    """Create soil_reports and soil_test_values tables if they don't exist."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS soil_reports (
                report_id TEXT PRIMARY KEY,
                farmer_id TEXT,
                field_id TEXT,
                source TEXT,
                file_name TEXT,
                sample_date TEXT,
                lab_name TEXT,
                extraction_confidence REAL,
                confirmed_by_farmer INTEGER,
                created_at TEXT,
                updated_at TEXT
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS soil_test_values (
                value_id TEXT PRIMARY KEY,
                report_id TEXT,
                parameter_name TEXT,
                value TEXT,
                unit TEXT,
                category TEXT,
                source_text TEXT,
                confidence REAL
            )
        """)
        conn.commit()
    finally:
        conn.close()


def save_soil_report(report_data):
    """Save a soil test report with confirmed values."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        report_id = report_data.get("report_id") or f"soil_{uuid.uuid4().hex[:8]}"
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute(
            """
            INSERT OR REPLACE INTO soil_reports
            (report_id, farmer_id, field_id, source, file_name, sample_date,
             lab_name, extraction_confidence, confirmed_by_farmer, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
                report_id,
                report_data.get("farmer_id", "user"),
                report_data.get("field_id", ""),
                report_data.get("source", "manual"),
                report_data.get("file_name", ""),
                report_data.get("sample_date", ""),
                report_data.get("lab_name", ""),
                float(report_data.get("extraction_confidence", 0.0)),
                1 if report_data.get("confirmed_by_farmer", True) else 0,
                report_data.get("created_at", now),
                now,
            ),
        )

        # Clear old values for this report
        cursor.execute("DELETE FROM soil_test_values WHERE report_id = ?", (report_id,))

        # Insert confirmed values
        for val in report_data.get("values", []):
            value_id = f"val_{uuid.uuid4().hex[:8]}"
            cursor.execute(
                """
                INSERT INTO soil_test_values
                (value_id, report_id, parameter_name, value, unit, category, source_text, confidence)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    value_id,
                    report_id,
                    val.get("parameter_name", ""),
                    str(val.get("value", "")),
                    val.get("unit", ""),
                    val.get("category", ""),
                    val.get("source_text", ""),
                    float(val.get("confidence", 1.0)),
                ),
            )

        conn.commit()
        return {"report_id": report_id, "status": "success"}
    finally:
        conn.close()


def get_soil_reports(field_id):
    """Get all soil reports for a specific field."""
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT * FROM soil_reports WHERE field_id = ? ORDER BY updated_at DESC",
            (field_id,),
        )
        reports = []
        for row in cursor.fetchall():
            report = dict(row)
            # Get values for this report
            cursor.execute(
                "SELECT parameter_name, value, unit, category FROM soil_test_values WHERE report_id = ?",
                (report["report_id"],),
            )
            report["values"] = [dict(v) for v in cursor.fetchall()]
            reports.append(report)
        return reports
    finally:
        conn.close()


def get_latest_soil_report(field_id):
    """Get the most recent confirmed soil report for a field."""
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT * FROM soil_reports WHERE field_id = ? AND confirmed_by_farmer = 1 ORDER BY updated_at DESC LIMIT 1",
            (field_id,),
        )
        row = cursor.fetchone()
        if not row:
            return None
        report = dict(row)
        cursor.execute(
            "SELECT parameter_name, value, unit, category FROM soil_test_values WHERE report_id = ?",
            (report["report_id"],),
        )
        report["values"] = [dict(v) for v in cursor.fetchall()]
        return report
    finally:
        conn.close()


# Initialize soil tables on module load
init_soil_tables()
