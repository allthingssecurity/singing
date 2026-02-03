# ACE-Step Studio Backend (Runpod Serverless)

This repository hosts the FastAPI backend for ACE-Step music generation, ready to deploy on Runpod Serverless (Load Balancing).

- Endpoints:
  - `GET /ping` — health check
  - `POST /api/generate` — create a generation job
  - `GET /api/jobs/{job_id}` — poll job status + output
  - `GET /api/outputs` — list recent files
  - Static downloads under `/outputs/*`

## Deploy to Runpod (Load Balancing)

1) In Runpod Console → Serverless → New Endpoint → Import from Git
   - Repository: this repo
   - Endpoint Type: Load Balancer
   - Environment Variables:
     - `ACE_CHECKPOINTS=/app/checkpoints`
     - `HF_HUB_ENABLE_HF_TRANSFER=1`
   - GPU: A10 or A100 recommended
   - Min workers: 0 or 1

2) The Dockerfile is at `runpod_lb/Dockerfile` and starts uvicorn on `${PORT}` (defaults 80).

3) After deploy, use:
```
https://ENDPOINT_ID.api.runpod.ai/ping
https://ENDPOINT_ID.api.runpod.ai/api/generate
https://ENDPOINT_ID.api.runpod.ai/api/jobs/{job_id}
https://ENDPOINT_ID.api.runpod.ai/api/outputs
```

For large first request, model weights download on demand (cached on the worker). You can also pre-bake weights by extending the Dockerfile if desired.
