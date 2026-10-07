from datetime import datetime, timezone
from models import viewed_job_model

def record_view(user_id: str, job_id: str):
    item = {"viewedAt": datetime.now(timezone.utc).isoformat()}
    return viewed_job_model.record_view(user_id, job_id, item)

def list_viewed_jobs(user_id: str):
    return viewed_job_model.list_viewed_jobs(user_id)