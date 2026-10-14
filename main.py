import os

from dotenv import load_dotenv

load_dotenv()  # must run before importing anything that reads environment variables

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config.firebase import init_firebase

init_firebase()

from routes import auth_routes, user_routes, job_routes, application_routes, viewed_job_routes

app = FastAPI(title="Job Tracker API (Firebase auth)")

origins = os.environ.get("CORS_ORIGINS", "http://localhost:5173,http://localhost:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in origins],
    allow_methods=["*"],
    allow_headers=["*"],  # includes Authorization
)

app.include_router(auth_routes.router)
app.include_router(user_routes.router)
app.include_router(job_routes.router)
app.include_router(application_routes.router)
app.include_router(viewed_job_routes.router)


@app.get("/")
def health_check():
    return {"status": "ok"}
