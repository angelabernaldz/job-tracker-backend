from fastapi import FastAPI 
from routers import auth, job_applications

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello World"}

app.include_router(auth.router)
app.include_router(job_applications.router)