from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from controllers import job_controller

router = APIRouter(prefix="/jobs", tags=["jobs"])

class CreateJob(BaseModel):
    title: str
    company: str

@router.post("", status_code=201)
def create_job(payload: CreateJob):
    return job_controller.create_job(payload.title, payload.company)

@router.get("/{job_id}")
def get_job(job_id: str):
    job = job_controller.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

@router.get("")
def list_jobs():
    return job_controller.list_jobs()