from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from controllers import job_controller
from dependencies.auth import get_current_user_id

# Every job route requires a logged-in user.
# NOTE: there are no admin roles yet, so any logged-in user can POST /jobs.
router = APIRouter(
    prefix="/jobs",
    tags=["jobs"],
    dependencies=[Depends(get_current_user_id)],
)


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
