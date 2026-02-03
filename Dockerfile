# Root-level Dockerfile for Runpod Serverless (Load Balancing)
FROM runpod/pytorch:2.1.0-py3.10-cuda11.8
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends ffmpeg git && rm -rf /var/lib/apt/lists/*
# Install Python deps (torch/torchaudio provided by base image)
COPY server/runpod_lb/requirements.runpod.txt /app/requirements.txt
RUN pip install -U --no-cache-dir pip wheel setuptools && \
    pip install --no-cache-dir -r /app/requirements.txt && \
    pip install --no-cache-dir hf_transfer
# Copy backend source
COPY server /app
ENV HF_HUB_ENABLE_HF_TRANSFER=1 \
    ACE_CHECKPOINTS=/app/checkpoints \
    PYTHONUNBUFFERED=1 \
    PORT=80
EXPOSE 80
CMD ["bash","-lc","uvicorn studio_backend.app:app --host 0.0.0.0 --port ${PORT}"]
