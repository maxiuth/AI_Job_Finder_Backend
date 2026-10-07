from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from controllers import application_controller

router = APIRouter(prefix="/users/{user_id}/applications", tags=["applications"])

class ApplicationUpdate(BaseModel):
    status: str

@router.post("", status_code=201)
def apply(user_id: str, job_id: str):
    return application_controller.apply_to_job(user_id, job_id)

@router.get("/{job_id}")
def get_application(user_id: str, job_id: str):
    app = application_controller.get_application(user_id, job_id)
    if not app:
        raise HTTPException(status_code=404, detail="Application not found")
    return app

@router.get("")
def list_applications(user_id: str):
    return application_controller.list_applications(user_id)

@router.patch("/{job_id}")
def update_status(user_id: str, job_id: str, payload: ApplicationUpdate):
    return application_controller.update_status(user_id, job_id, payload.status)

@router.delete("/{job_id}", status_code=204)
def withdraw(user_id: str, job_id: str):
    application_controller.withdraw(user_id, job_id)