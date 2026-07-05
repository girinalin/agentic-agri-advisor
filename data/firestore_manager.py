"""
Firestore database manager for Krishi Sampark.

Replaces the SQLite db_manager for Cloud Run deployment.
Uses Firestore in Native mode for all farmer data.

Collection Structure:
  /farmers/{farmer_id}
    └── /fields/{field_id}
          └── /plantings/{planting_id}
                ├── /activities/{activity_id}
                ├── /farm_plans/{plan_id}
                ├── /reminders/{reminder_id}
                ├── /escalations/{escalation_id}
                └── /feedbacks/{feedback_id}
    └── /soil_reports/{report_id}
          └── /soil_test_values/{value_id}  (subcollection)
  /regional_outbreaks/{outbreak_id}
  /okf_governance/{content_id}
  /observability_logs/{log_id}
  /privacy_preferences/{user_id}
  /sync_dlq/{dlq_id}

Locally: Falls back to SQLite when FIRESTORE_PROJECT_ID env var is not set.
This allows local development without Firestore credentials.
"""

import os
import uuid
from datetime import datetime
from typing import Optional

# Firestore imports (lazy)
_firestore_client = None
_use_firestore = None


def _should_use_firestore():
    """Determine if we should use Firestore or fall back to SQLite."""
    global _use_firestore
    if _use_firestore is None:
        _use_firestore = bool(
            os.getenv("FIRESTORE_PROJECT_ID")
            or os.getenv("USE_FIRESTORE")
            or os.getenv("FIRESTORE_EMULATOR_HOST")
        )
    return _use_firestore


def _get_firestore():
    """Lazy-initialize the Firestore client."""
    global _firestore_client
    if _firestore_client is None:
        from google.cloud import firestore

        emulator_host = os.getenv("FIRESTORE_EMULATOR_HOST")
        project_id = os.getenv("FIRESTORE_PROJECT_ID") or os.getenv(
            "GOOGLE_CLOUD_PROJECT"
        )

        if emulator_host:
            # Local Firestore Emulator — no credentials needed
            from google.auth.credentials import AnonymousCredentials

            _firestore_client = firestore.Client(
                project=project_id or "emulator-project",
                credentials=AnonymousCredentials(),
            )
            print(f"Using Firestore Emulator at {emulator_host}")
        else:
            # Real GCP Firestore — uses Application Default Credentials
            _firestore_client = firestore.Client(project=project_id)
            print(f"Using GCP Firestore for project: {project_id}")
    return _firestore_client


# ---------------------------------------------------------------------------
# Profile
# ---------------------------------------------------------------------------


def get_profile_data(farmer_id="user"):
    """Fetch farmer profile with fields and plantings."""
    if not _should_use_firestore():
        from data.sqlite_manager import get_profile_data as _sqlite_get

        return _sqlite_get(farmer_id)

    db = _get_firestore()
    farmer_ref = db.collection("farmers").document(farmer_id)
    farmer_doc = farmer_ref.get()

    if not farmer_doc.exists:
        # Auto-create default farmer
        farmer_ref.set({"farmer_id": farmer_id, "name": "Farmer", "language": "Hindi"})
        farmer_doc = farmer_ref.get()

    farmer = farmer_doc.to_dict()
    profile = {
        "farmer_id": farmer_id,
        "name": farmer.get("name", "Farmer"),
        "language": farmer.get("language", "Hindi"),
        "fields": [],
    }

    # Get fields
    fields = farmer_ref.collection("fields").stream()
    for field_doc in fields:
        field_data = field_doc.to_dict()
        field_id = field_doc.id
        field = {
            "field_id": field_id,
            "name": field_data.get("name", ""),
            "soil_type": field_data.get("soil_type", ""),
            "acres": field_data.get("acres", 0),
            "irrigation_type": field_data.get("irrigation_type", ""),
            "planting": None,
        }

        # Get active planting
        plantings = field_doc.reference.collection("plantings").limit(1).stream()
        for planting_doc in plantings:
            p = planting_doc.to_dict()
            field["planting"] = {
                "planting_id": planting_doc.id,
                "crop_type": p.get("crop_type", ""),
                "variety": p.get("variety", ""),
                "planting_date": p.get("planting_date", ""),
                "stage": p.get("stage", ""),
                "nitrogen_ppm": p.get("nitrogen_ppm", 0),
                "moisture_pct": p.get("moisture_pct", 0),
                "health_pct": p.get("health_pct", 0),
            }

        profile["fields"].append(field)

    return profile


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
    """Add a new field and seed an initial crop planting."""
    if not _should_use_firestore():
        from data.sqlite_manager import save_farmer_field as _sqlite_save

        return _sqlite_save(
            farmer_id,
            name,
            soil_type,
            acres,
            irrigation_type,
            crop_type,
            variety,
            stage,
        )

    db = _get_firestore()
    field_id = f"field_{uuid.uuid4().hex[:8]}"
    planting_id = f"planting_{uuid.uuid4().hex[:8]}"
    planting_date = datetime.now().strftime("%Y-%m-%d")

    field_ref = (
        db.collection("farmers")
        .document(farmer_id)
        .collection("fields")
        .document(field_id)
    )
    field_ref.set(
        {
            "name": name,
            "soil_type": soil_type,
            "acres": float(acres),
            "irrigation_type": irrigation_type,
        }
    )

    field_ref.collection("plantings").document(planting_id).set(
        {
            "crop_type": crop_type,
            "variety": variety,
            "planting_date": planting_date,
            "stage": stage,
            "nitrogen_ppm": 40.0,
            "moisture_pct": 45.0,
            "health_pct": 100.0,
        }
    )

    return {"field_id": field_id, "planting_id": planting_id}


# ---------------------------------------------------------------------------
# Telemetry
# ---------------------------------------------------------------------------


def update_planting_telemetry(planting_id, moisture_pct, health_pct, nitrogen_ppm):
    """Update planting telemetry values."""
    if not _should_use_firestore():
        from data.sqlite_manager import update_planting_telemetry as _sqlite_update

        return _sqlite_update(planting_id, moisture_pct, health_pct, nitrogen_ppm)

    db = _get_firestore()
    # Search across all farmers/fields for this planting_id
    # In production, we'd index planting_id; for pilot we query the known structure
    farmers = db.collection("farmers").stream()
    for farmer_doc in farmers:
        fields = farmer_doc.reference.collection("fields").stream()
        for field_doc in fields:
            planting_ref = field_doc.reference.collection("plantings").document(
                planting_id
            )
            if planting_ref.get().exists:
                planting_ref.update(
                    {
                        "moisture_pct": float(moisture_pct),
                        "health_pct": float(health_pct),
                        "nitrogen_ppm": float(nitrogen_ppm),
                    }
                )
                return True
    return False


# ---------------------------------------------------------------------------
# Activities
# ---------------------------------------------------------------------------


def log_activity_record(
    planting_id, activity_type, quantity, unit, details, timestamp=None
):
    """Log a farm activity."""
    if not _should_use_firestore():
        from data.sqlite_manager import log_activity_record as _sqlite_log

        return _sqlite_log(
            planting_id, activity_type, quantity, unit, details, timestamp
        )

    db = _get_firestore()
    activity_id = f"act_{uuid.uuid4().hex[:8]}"
    if not timestamp:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Find the planting's parent path
    planting_path = _find_planting_path(db, planting_id)
    if not planting_path:
        return {"status": "error", "message": f"Planting {planting_id} not found"}

    planting_path.collection("activities").document(activity_id).set(
        {
            "activity_type": activity_type,
            "quantity": float(quantity),
            "unit": unit,
            "details": details,
            "timestamp": timestamp,
            "synced": 1,
        }
    )

    return {"activity_id": activity_id, "status": "success"}


def get_activities_log(planting_id):
    """Get activities for a planting."""
    if not _should_use_firestore():
        from data.sqlite_manager import get_activities_log as _sqlite_get

        return _sqlite_get(planting_id)

    db = _get_firestore()
    planting_path = _find_planting_path(db, planting_id)
    if not planting_path:
        return []

    docs = (
        planting_path.collection("activities")
        .order_by("timestamp", direction="DESCENDING")
        .limit(50)
        .stream()
    )
    return [doc.to_dict() for doc in docs]


# ---------------------------------------------------------------------------
# Farm Plans
# ---------------------------------------------------------------------------


def get_daily_plans(planting_id):
    """Get farm plans for a planting."""
    if not _should_use_firestore():
        from data.sqlite_manager import get_daily_plans as _sqlite_get

        return _sqlite_get(planting_id)

    db = _get_firestore()
    planting_path = _find_planting_path(db, planting_id)
    if not planting_path:
        return []

    docs = (
        planting_path.collection("farm_plans")
        .order_by("timestamp", direction="DESCENDING")
        .stream()
    )
    return [doc.to_dict() for doc in docs]


def update_plan_state(plan_id, state):
    """Update a farm plan state."""
    if not _should_use_firestore():
        from data.sqlite_manager import update_plan_state as _sqlite_update

        return _sqlite_update(plan_id, state)

    db = _get_firestore()
    # Search across all plantings for this plan_id
    for farmer_doc in db.collection("farmers").stream():
        for field_doc in farmer_doc.reference.collection("fields").stream():
            for planting_doc in field_doc.reference.collection("plantings").stream():
                plan_ref = planting_doc.reference.collection("farm_plans").document(
                    plan_id
                )
                if plan_ref.get().exists:
                    plan_ref.update({"state": state})
                    return True
    return False


# ---------------------------------------------------------------------------
# Reminders
# ---------------------------------------------------------------------------


def get_reminders(planting_id):
    """Get reminders for a planting."""
    if not _should_use_firestore():
        from data.sqlite_manager import get_reminders as _sqlite_get

        return _sqlite_get(planting_id)

    db = _get_firestore()
    planting_path = _find_planting_path(db, planting_id)
    if not planting_path:
        return []

    docs = (
        planting_path.collection("reminders")
        .order_by("timestamp", direction="DESCENDING")
        .stream()
    )
    return [doc.to_dict() for doc in docs]


def update_reminder_state(reminder_id, state):
    """Update a reminder state."""
    if not _should_use_firestore():
        from data.sqlite_manager import update_reminder_state as _sqlite_update

        return _sqlite_update(reminder_id, state)

    db = _get_firestore()
    for farmer_doc in db.collection("farmers").stream():
        for field_doc in farmer_doc.reference.collection("fields").stream():
            for planting_doc in field_doc.reference.collection("plantings").stream():
                rem_ref = planting_doc.reference.collection("reminders").document(
                    reminder_id
                )
                if rem_ref.get().exists:
                    rem_ref.update({"state": state})
                    return True
    return False


# ---------------------------------------------------------------------------
# Escalations
# ---------------------------------------------------------------------------


def save_escalation_request(esc):
    """Save an escalation request."""
    if not _should_use_firestore():
        from data.sqlite_manager import save_escalation_request as _sqlite_save

        return _sqlite_save(esc)

    db = _get_firestore()
    esc_id = esc.get("escalation_id") or f"esc_{uuid.uuid4().hex[:8]}"
    timestamp = esc.get("timestamp") or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    planting_id = esc.get("planting_id", "planting_1")

    planting_path = _find_planting_path(db, planting_id)
    if not planting_path:
        # Store at top-level if planting not found
        db.collection("escalations").document(esc_id).set(
            {**esc, "escalation_id": esc_id, "timestamp": timestamp}
        )
    else:
        planting_path.collection("escalations").document(esc_id).set(
            {**esc, "escalation_id": esc_id, "timestamp": timestamp}
        )

    return {"escalation_id": esc_id, "status": "success"}


def get_escalations(planting_id):
    """Get escalations for a planting."""
    if not _should_use_firestore():
        from data.sqlite_manager import get_escalations as _sqlite_get

        return _sqlite_get(planting_id)

    db = _get_firestore()
    planting_path = _find_planting_path(db, planting_id)
    if not planting_path:
        return []

    docs = (
        planting_path.collection("escalations")
        .order_by("timestamp", direction="DESCENDING")
        .stream()
    )
    return [doc.to_dict() for doc in docs]


def get_expert_queue():
    """Get all escalations for the agronomist queue."""
    if not _should_use_firestore():
        from data.sqlite_manager import get_expert_queue as _sqlite_get

        return _sqlite_get()

    db = _get_firestore()
    results = []
    for farmer_doc in db.collection("farmers").stream():
        for field_doc in farmer_doc.reference.collection("fields").stream():
            for planting_doc in field_doc.reference.collection("plantings").stream():
                docs = (
                    planting_doc.reference.collection("escalations")
                    .order_by("timestamp", direction="DESCENDING")
                    .stream()
                )
                results.extend([doc.to_dict() for doc in docs])
    return results


def update_expert_case_state(escalation_id, state, expert_response=None):
    """Update escalation state and expert response."""
    if not _should_use_firestore():
        from data.sqlite_manager import update_expert_case_state as _sqlite_update

        return _sqlite_update(escalation_id, state, expert_response)

    db = _get_firestore()
    update_data = {"state": state}
    if expert_response is not None:
        update_data["expert_response"] = expert_response

    for farmer_doc in db.collection("farmers").stream():
        for field_doc in farmer_doc.reference.collection("fields").stream():
            for planting_doc in field_doc.reference.collection("plantings").stream():
                esc_ref = planting_doc.reference.collection("escalations").document(
                    escalation_id
                )
                if esc_ref.get().exists:
                    esc_ref.update(update_data)
                    return {"status": "success"}
    return {"status": "error", "message": "Escalation not found"}


# ---------------------------------------------------------------------------
# Feedback
# ---------------------------------------------------------------------------


def log_outcome_feedback(f):
    """Log outcome feedback."""
    if not _should_use_firestore():
        from data.sqlite_manager import log_outcome_feedback as _sqlite_log

        return _sqlite_log(f)

    db = _get_firestore()
    feedback_id = f.get("feedback_id") or f"feed_{uuid.uuid4().hex[:8]}"
    timestamp = f.get("timestamp") or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    planting_id = f.get("planting_id", "planting_1")

    planting_path = _find_planting_path(db, planting_id)
    if planting_path:
        planting_path.collection("feedbacks").document(feedback_id).set(
            {
                "followed_recommendation": int(f.get("followed_recommendation", 1)),
                "outcome": f.get("outcome", ""),
                "time_to_outcome": f.get("time_to_outcome", ""),
                "comment": f.get("comment", ""),
                "image_path": f.get("image_path", ""),
                "farmer_confidence": float(f.get("farmer_confidence", 1.0)),
                "timestamp": timestamp,
            }
        )

    return {"feedback_id": feedback_id, "status": "success"}


# ---------------------------------------------------------------------------
# Regional Outbreaks
# ---------------------------------------------------------------------------


def get_outbreaks():
    """Get regional outbreaks."""
    if not _should_use_firestore():
        from data.sqlite_manager import get_outbreaks as _sqlite_get

        return _sqlite_get()

    db = _get_firestore()
    docs = (
        db.collection("regional_outbreaks")
        .order_by("timestamp", direction="DESCENDING")
        .stream()
    )
    return [doc.to_dict() for doc in docs]


def confirm_outbreak(outbreak_id, status):
    """Update outbreak status."""
    if not _should_use_firestore():
        from data.sqlite_manager import confirm_outbreak as _sqlite_update

        return _sqlite_update(outbreak_id, status)

    db = _get_firestore()
    ref = db.collection("regional_outbreaks").document(outbreak_id)
    if ref.get().exists:
        ref.update({"status": status, "expert_verified": 1})
        return {"status": "success"}
    return {"status": "error", "message": "Outbreak not found"}


# ---------------------------------------------------------------------------
# OKF Governance
# ---------------------------------------------------------------------------


def get_governance_metadata():
    """Get OKF governance records."""
    if not _should_use_firestore():
        from data.sqlite_manager import get_governance_metadata as _sqlite_get

        return _sqlite_get()

    db = _get_firestore()
    docs = db.collection("okf_governance").stream()
    return [doc.to_dict() for doc in docs]


def rollback_governance_version(content_id):
    """Rollback governance content to previous version."""
    if not _should_use_firestore():
        from data.sqlite_manager import rollback_governance_version as _sqlite_rollback

        return _sqlite_rollback(content_id)

    db = _get_firestore()
    ref = db.collection("okf_governance").document(content_id)
    doc = ref.get()
    if not doc.exists:
        return {"status": "error", "message": "Content not found"}

    data = doc.to_dict()
    v = data.get("version", 1)
    if v > 1:
        ref.update({"version": v - 1, "approval_status": "approved"})
    else:
        ref.update({"approval_status": "withdrawn"})
    return {"status": "success"}


# ---------------------------------------------------------------------------
# Observability Logs
# ---------------------------------------------------------------------------


def log_observability_event(
    correlation_id,
    event_type,
    screen="",
    agent="",
    tool="",
    route="",
    safety_decision="",
    latency=0.0,
    device_tier="",
):
    """Save an observability trace event."""
    if not _should_use_firestore():
        from data.sqlite_manager import log_observability_event as _sqlite_log

        return _sqlite_log(
            correlation_id,
            event_type,
            screen,
            agent,
            tool,
            route,
            safety_decision,
            latency,
            device_tier,
        )

    db = _get_firestore()
    log_id = f"log_{uuid.uuid4().hex[:12]}"
    db.collection("observability_logs").document(log_id).set(
        {
            "correlation_id": correlation_id,
            "event_type": event_type,
            "screen": screen,
            "agent": agent,
            "tool": tool,
            "route": route,
            "safety_decision": safety_decision,
            "latency": latency,
            "device_tier": device_tier,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
    )
    return {"status": "success"}


def get_observability_logs():
    """Get latest 50 observability logs."""
    if not _should_use_firestore():
        from data.sqlite_manager import get_observability_logs as _sqlite_get

        return _sqlite_get()

    db = _get_firestore()
    docs = (
        db.collection("observability_logs")
        .order_by("timestamp", direction="DESCENDING")
        .limit(50)
        .stream()
    )
    return [doc.to_dict() for doc in docs]


# ---------------------------------------------------------------------------
# Privacy Preferences
# ---------------------------------------------------------------------------


def save_privacy_preferences(payload):
    """Save privacy consent settings."""
    if not _should_use_firestore():
        from data.sqlite_manager import save_privacy_preferences as _sqlite_save

        return _sqlite_save(payload)

    db = _get_firestore()
    user_id = payload.get("user_id", "user")
    db.collection("privacy_preferences").document(user_id).set(
        {
            "location_sharing": int(payload.get("location_sharing", 1)),
            "image_retention": int(payload.get("image_retention", 1)),
            "voice_retention": int(payload.get("voice_retention", 1)),
            "expert_consultation_sharing": int(
                payload.get("expert_consultation_sharing", 1)
            ),
            "regional_outbreak_participation": int(
                payload.get("regional_outbreak_participation", 1)
            ),
            "analytics_participation": int(payload.get("analytics_participation", 1)),
        }
    )
    return {"status": "success"}


# ---------------------------------------------------------------------------
# Soil Reports
# ---------------------------------------------------------------------------


def init_soil_tables():
    """No-op for Firestore — collections are created on demand."""
    if not _should_use_firestore():
        from data.sqlite_manager import init_soil_tables as _sqlite_init

        return _sqlite_init()
    # Firestore creates collections on demand — nothing to do
    pass


def save_soil_report(report_data):
    """Save a soil test report with confirmed values."""
    if not _should_use_firestore():
        from data.sqlite_manager import save_soil_report as _sqlite_save

        return _sqlite_save(report_data)

    db = _get_firestore()
    report_id = report_data.get("report_id") or f"soil_{uuid.uuid4().hex[:8]}"
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    farmer_id = report_data.get("farmer_id", "user")
    field_id = report_data.get("field_id", "")

    report_ref = (
        db.collection("farmers")
        .document(farmer_id)
        .collection("soil_reports")
        .document(report_id)
    )
    report_ref.set(
        {
            "report_id": report_id,
            "field_id": field_id,
            "source": report_data.get("source", "manual"),
            "file_name": report_data.get("file_name", ""),
            "sample_date": report_data.get("sample_date", ""),
            "lab_name": report_data.get("lab_name", ""),
            "extraction_confidence": float(
                report_data.get("extraction_confidence", 0.0)
            ),
            "confirmed_by_farmer": 1
            if report_data.get("confirmed_by_farmer", True)
            else 0,
            "created_at": report_data.get("created_at", now),
            "updated_at": now,
        }
    )

    # Clear old values and set new ones
    values_ref = report_ref.collection("soil_test_values")
    existing = values_ref.stream()
    for doc in existing:
        doc.reference.delete()

    for val in report_data.get("values", []):
        value_id = f"val_{uuid.uuid4().hex[:8]}"
        values_ref.document(value_id).set(
            {
                "parameter_name": val.get("parameter_name", ""),
                "value": str(val.get("value", "")),
                "unit": val.get("unit", ""),
                "category": val.get("category", ""),
                "source_text": val.get("source_text", ""),
                "confidence": float(val.get("confidence", 1.0)),
            }
        )

    return {"report_id": report_id, "status": "success"}


def get_soil_reports(field_id):
    """Get all soil reports for a field."""
    if not _should_use_firestore():
        from data.sqlite_manager import get_soil_reports as _sqlite_get

        return _sqlite_get(field_id)

    db = _get_firestore()
    farmer_id = os.getenv("FARMER_ID", "user")
    reports = []
    docs = (
        db.collection("farmers")
        .document(farmer_id)
        .collection("soil_reports")
        .where("field_id", "==", field_id)
        .order_by("updated_at", direction="DESCENDING")
        .stream()
    )

    for doc in docs:
        report = doc.to_dict()
        values = doc.reference.collection("soil_test_values").stream()
        report["values"] = [v.to_dict() for v in values]
        reports.append(report)
    return reports


def get_latest_soil_report(field_id):
    """Get the most recent confirmed soil report for a field."""
    if not _should_use_firestore():
        from data.sqlite_manager import get_latest_soil_report as _sqlite_get

        return _sqlite_get(field_id)

    db = _get_firestore()
    farmer_id = os.getenv("FARMER_ID", "user")
    docs = (
        db.collection("farmers")
        .document(farmer_id)
        .collection("soil_reports")
        .where("field_id", "==", field_id)
        .where("confirmed_by_farmer", "==", 1)
        .order_by("updated_at", direction="DESCENDING")
        .limit(1)
        .stream()
    )

    for doc in docs:
        report = doc.to_dict()
        values = doc.reference.collection("soil_test_values").stream()
        report["values"] = [v.to_dict() for v in values]
        return report
    return None


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _find_planting_path(db, planting_id):
    """Find the Firestore DocumentReference for a planting by ID."""
    for farmer_doc in db.collection("farmers").stream():
        for field_doc in farmer_doc.reference.collection("fields").stream():
            planting_ref = field_doc.reference.collection("plantings").document(
                planting_id
            )
            if planting_ref.get().exists:
                return planting_ref
    return None


def get_connection():
    """SQLite compatibility — return a sqlite connection for local dev."""
    from data.sqlite_manager import get_connection as _sqlite_conn

    return _sqlite_conn()


# ---------------------------------------------------------------------------
# Seed default data on first run
# ---------------------------------------------------------------------------


def seed_default_data():
    """Seed default farmer data if Firestore is empty (first deploy)."""
    if not _should_use_firestore():
        return

    db = _get_firestore()
    farmer_ref = db.collection("farmers").document("user")
    if not farmer_ref.get().exists:
        farmer_ref.set({"farmer_id": "user", "name": "Nalin Giri", "language": "Hindi"})

        # Field 1
        f1 = farmer_ref.collection("fields").document("field_1")
        f1.set(
            {
                "name": "North Hillside",
                "soil_type": "Black Clay (Cotton Soil)",
                "acres": 5.0,
                "irrigation_type": "Drip",
            }
        )
        f1.collection("plantings").document("planting_1").set(
            {
                "crop_type": "Corn",
                "variety": "PMH-1",
                "planting_date": "2026-06-01",
                "stage": "germination",
                "nitrogen_ppm": 45.0,
                "moisture_pct": 45.5,
                "health_pct": 100.0,
            }
        )

        # Field 2
        f2 = farmer_ref.collection("fields").document("field_2")
        f2.set(
            {
                "name": "Riverbed Meadow",
                "soil_type": "Red Sandy Loam",
                "acres": 8.0,
                "irrigation_type": "Sprinkler",
            }
        )
        f2.collection("plantings").document("planting_2").set(
            {
                "crop_type": "Wheat",
                "variety": "Lokwan",
                "planting_date": "2026-06-10",
                "stage": "vegetative",
                "nitrogen_ppm": 55.0,
                "moisture_pct": 45.0,
                "health_pct": 95.0,
            }
        )

        # Privacy preferences
        db.collection("privacy_preferences").document("user").set(
            {
                "location_sharing": 1,
                "image_retention": 1,
                "voice_retention": 1,
                "expert_consultation_sharing": 1,
                "regional_outbreak_participation": 1,
                "analytics_participation": 1,
            }
        )

        print("Seeded default farmer data to Firestore")
    else:
        # Ensure fields exist
        f1 = farmer_ref.collection("fields").document("field_1")
        if not f1.get().exists:
            f1.set(
                {
                    "name": "North Hillside",
                    "soil_type": "Black Clay (Cotton Soil)",
                    "acres": 5.0,
                    "irrigation_type": "Drip",
                }
            )
            f1.collection("plantings").document("planting_1").set(
                {
                    "crop_type": "Corn",
                    "variety": "PMH-1",
                    "planting_date": "2026-06-01",
                    "stage": "germination",
                    "nitrogen_ppm": 45.0,
                    "moisture_pct": 45.5,
                    "health_pct": 100.0,
                }
            )
        f2 = farmer_ref.collection("fields").document("field_2")
        if not f2.get().exists:
            f2.set(
                {
                    "name": "Riverbed Meadow",
                    "soil_type": "Red Sandy Loam",
                    "acres": 8.0,
                    "irrigation_type": "Sprinkler",
                }
            )
            f2.collection("plantings").document("planting_2").set(
                {
                    "crop_type": "Wheat",
                    "variety": "Lokwan",
                    "planting_date": "2026-06-10",
                    "stage": "vegetative",
                    "nitrogen_ppm": 55.0,
                    "moisture_pct": 45.0,
                    "health_pct": 95.0,
                }
            )


# Auto-seed on module load
try:
    if _should_use_firestore():
        seed_default_data()
except Exception as e:
    print(f"Warning: Could not seed Firestore default data: {e}")
