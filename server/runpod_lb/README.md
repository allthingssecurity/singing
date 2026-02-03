# ACE-Step Runpod Serverless (Load Balancing) Worker

This builds a FastAPI server exposing the same endpoints as the local backend:
- `POST /api/generate`
- `GET /api/jobs/{job_id}`
- `GET /api/outputs`
- Static `/outputs/*`

## Build locally (optional)

```
docker build -t ace-step-lb -f runpod_lb/Dockerfile .
docker run --rm -p 8000:80 -e PORT=80 ace-step-lb
```

Open http://127.0.0.1:8000/api/outputs

## Deploy on Runpod

- In Runpod Console → Serverless → New Endpoint → Load Balancing.
- Choose “Import from Git” and point to this repo.
- Set build context to repository root.
- Container start command is already baked in Dockerfile.
- Set min workers 0–1, GPU to match model needs (e.g., A10/A100).
- Environment:
  - `ACE_CHECKPOINTS=/app/checkpoints`
  - `HF_HUB_ENABLE_HF_TRANSFER=1`

Once deployed, your endpoint base URL will be:
```
https://ENDPOINT_ID.api.runpod.ai
```
Use it in your frontend `.env.local` as `NEXT_PUBLIC_API_URL`.
