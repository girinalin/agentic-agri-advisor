"""
Database manager dispatcher for Krishi Sampark.

Automatically routes to Firestore when deployed to Cloud Run (FIRESTORE_PROJECT_ID
or USE_FIRESTORE env var is set), and falls back to SQLite for local development.

This file re-exports all functions from the active backend so that
`from data.db_manager import get_profile_data` works regardless of which
database is active.

Usage:
  Local dev (SQLite):     No env vars needed — SQLite is used automatically
  Cloud Run (Firestore):  Set FIRESTORE_PROJECT_ID=<your-gcp-project> or
                          set USE_FIRESTORE=1 + GOOGLE_CLOUD_PROJECT=<project>
"""

import os

# Determine which backend to use
_USE_FIRESTORE = bool(os.getenv("FIRESTORE_PROJECT_ID") or os.getenv("USE_FIRESTORE"))

if _USE_FIRESTORE:
    # Firestore backend (Cloud Run / production)
    from data.firestore_manager import (
        confirm_outbreak,
        get_activities_log,
        get_connection,
        get_daily_plans,
        get_escalations,
        get_expert_queue,
        get_governance_metadata,
        get_latest_soil_report,
        get_observability_logs,
        get_outbreaks,
        get_profile_data,
        get_reminders,
        get_soil_reports,
        init_soil_tables,
        log_activity_record,
        log_observability_event,
        rollback_governance_version,
        save_escalation_request,
        save_farmer_field,
        save_privacy_preferences,
        save_soil_report,
        seed_default_data,
        update_expert_case_state,
        update_plan_state,
        update_planting_telemetry,
        update_reminder_state,
    )
else:
    # SQLite backend (local development)
    from data.sqlite_manager import (
        confirm_outbreak,
        get_activities_log,
        get_connection,
        get_daily_plans,
        get_escalations,
        get_expert_queue,
        get_governance_metadata,
        get_latest_soil_report,
        get_observability_logs,
        get_outbreaks,
        get_profile_data,
        get_reminders,
        get_soil_reports,
        init_soil_tables,
        log_activity_record,
        log_observability_event,
        rollback_governance_version,
        save_escalation_request,
        save_farmer_field,
        save_privacy_preferences,
        save_soil_report,
        update_expert_case_state,
        update_plan_state,
        update_planting_telemetry,
        update_reminder_state,
    )

# Initialize soil tables (SQLite only; Firestore is no-op)
init_soil_tables()

# If using Firestore, seed default data on first run
if _USE_FIRESTORE:
    try:
        seed_default_data()
    except Exception as e:
        print(f"Warning: Firestore seed failed: {e}")
