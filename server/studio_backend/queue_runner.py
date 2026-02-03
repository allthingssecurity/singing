from __future__ import annotations
import asyncio, uuid, time, os, json
from typing import Dict, Any, Optional
from loguru import logger
from .models import GenerateRequest, JobStatus

class PipelineWrapper:
    def __init__(self, checkpoints_dir: str):
        from pipeline_ace_step import ACEStepPipeline
        self.pipeline = ACEStepPipeline(checkpoint_dir=checkpoints_dir)
        self.outputs_dir = os.path.join(os.getcwd(), 'outputs')
        os.makedirs(self.outputs_dir, exist_ok=True)

    def run_generate(self, req: GenerateRequest, progress_cb=None) -> str:
        # The pipeline __call__ already handles many params; we map a subset.
        # It returns list of file paths. We ensure save_path defaults to ./outputs.
        self.pipeline._progress_cb = progress_cb
        result_paths = self.pipeline(
            prompt=req.prompt,
            lyrics=req.lyrics,
            infer_step=req.steps,
            guidance_scale=req.guidance_scale,
            cfg_type=req.cfg_type,
            omega_scale=req.omega_scale,
            guidance_scale_text=req.guidance_scale_text,
            guidance_scale_lyric=req.guidance_scale_lyric,
            audio_duration=req.duration,
        )
        if not result_paths:
            raise RuntimeError("No output generated")
        out = result_paths[0]
        self.pipeline._progress_cb = None
        return out

class JobQueue:
    def __init__(self, pipeline: PipelineWrapper):
        self.pipeline = pipeline
        self.jobs: Dict[str, JobStatus] = {}
        self.queue: asyncio.Queue[tuple[str, GenerateRequest]] = asyncio.Queue()
        self.worker_task: Optional[asyncio.Task] = None

    async def start(self):
        if self.worker_task is None:
            self.worker_task = asyncio.create_task(self._worker())

    async def enqueue(self, req: GenerateRequest) -> str:
        job_id = uuid.uuid4().hex
        self.jobs[job_id] = JobStatus(
            job_id=job_id, status='queued', created_at=time.time(), params=req.model_dump()
        )
        await self.queue.put((job_id, req))
        return job_id

    async def _worker(self):
        while True:
            job_id, req = await self.queue.get()
            st = self.jobs[job_id]
            st.status = 'running'; st.started_at = time.time()
            try:
                path = await asyncio.get_event_loop().run_in_executor(
                    None, self.pipeline.run_generate, req, lambda info: self._update_progress(job_id, info)
                )
                st.output_path = path
                st.status = 'succeeded'; st.ended_at = time.time();
                if st.started_at: st.progress = {'step': st.progress.get('total',0) if st.progress else None, 'total': st.progress.get('total',0) if st.progress else None, 'duration_sec': st.ended_at - st.started_at}
            except Exception as e:
                logger.exception("job failed")
                st.error = str(e)
                st.status = 'failed'; st.ended_at = time.time()
            finally:
                self.queue.task_done()

    def get(self, job_id: str) -> Optional[JobStatus]:
        return self.jobs.get(job_id)
