import os
from fastapi import FastAPI 
from routers import auth, job_applications
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

frontend_url = os.getenv("FRONTEND_URL")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[frontend_url],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(job_applications.router)