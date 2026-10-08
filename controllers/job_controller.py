import uuid
from datetime import datetime, timezone
from models import job_model

def create_job(title: str, company: str):
    item = {
        "jobId": str(uuid.uuid4()),
        "title": title,
        "company": company,
        "postedAt": datetime.now(timezone.utc).isoformat(),
    }
    return job_model.create_job(item)

def get_job(job_id: str):
    return job_model.get_job(job_id)

def list_jobs():
    return job_model.list_jobs()