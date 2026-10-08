from fastapi import FastAPI
from routes import user_routes, job_routes, application_routes, viewed_job_routes

app = FastAPI(title="Job Tracker API")

app.include_router(user_routes.router)
app.include_router(job_routes.router)
app.include_router(application_routes.router)
app.include_router(viewed_job_routes.router)