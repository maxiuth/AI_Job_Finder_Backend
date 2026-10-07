from fastapi import APIRouter
from controllers import viewed_job_controller

router = APIRouter(prefix="/users/{user_id}/viewed-jobs", tags=["viewed-jobs"])

@router.post("/{job_id}", status_code=201)
def record_view(user_id: str, job_id: str):
    return viewed_job_controller.record_view(user_id, job_id)

@router.get("")
def list_viewed_jobs(user_id: str):
    return viewed_job_controller.list_viewed_jobs(user_id)