from __future__ import annotations
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from .models import GenerateRequest, JobStatus
from .queue_runner import JobQueue, PipelineWrapper
import asyncio, os, glob

CHECKPOINTS=os.environ.get('ACE_CHECKPOINTS','checkpoints')
OUTPUTS_DIR=os.path.join(os.getcwd(),'outputs')

app = FastAPI(title="ACE-Step Studio API", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

pipeline = PipelineWrapper(CHECKPOINTS)
queue = JobQueue(pipeline)

@app.get("/ping")
async def ping():
    return {"status":"ok"}

@app.on_event("startup")
async def _startup():
    await queue.start()

@app.post('/api/generate', response_model=JobStatus)
async def api_generate(req: GenerateRequest):
    job_id = await queue.enqueue(req)
    st = queue.get(job_id)
    return st

@app.get('/api/jobs/{job_id}', response_model=JobStatus)
async def api_job(job_id: str):
    st = queue.get(job_id)
    if not st:
        raise HTTPException(404, 'job not found')
    return st

@app.get('/api/outputs')
async def api_outputs(limit: int = 12):
    files = sorted(glob.glob(os.path.join(OUTPUTS_DIR, '*.*')), key=os.path.getmtime, reverse=True)
    return {'files': files[:limit]}

# Serve outputs statically
if not os.path.exists(OUTPUTS_DIR):
    os.makedirs(OUTPUTS_DIR, exist_ok=True)
app.mount('/outputs', StaticFiles(directory=OUTPUTS_DIR), name='outputs')
