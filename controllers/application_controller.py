from datetime import datetime, timezone
from models import application_model

def apply_to_job(user_id: str, job_id: str):
    item = {"status": "applied", "appliedAt": datetime.now(timezone.utc).isoformat()}
    return application_model.create_application(user_id, job_id, item)

def get_application(user_id: str, job_id: str):
    return application_model.get_application(user_id, job_id)

def list_applications(user_id: str):
    return application_model.list_applications_for_user(user_id)

def update_status(user_id: str, job_id: str, status: str):
    return application_model.update_application_status(user_id, job_id, status)

def withdraw(user_id: str, job_id: str):
    application_model.delete_application(user_id, job_id)

def list_applicants(job_id: str):
    return application_model.list_applicants_for_job(job_id)