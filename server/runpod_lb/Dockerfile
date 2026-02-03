# Runpod Load Balancing worker: FastAPI serving ACE-Step backend
FROM pytorch/pytorch:2.1.0-cuda11.8-cudnn8-runtime
WORKDIR /app
# System deps
RUN apt-get update && apt-get install -y ffmpeg git && rm -rf /var/lib/apt/lists/*
# Python deps (avoid pinning torch here; base image already has GPU torch)
COPY requirements.runpod.txt /app/requirements.txt
RUN pip install -U --no-cache-dir pip wheel setuptools && \
    pip install --no-cache-dir -r /app/requirements.txt && \
    pip install --no-cache-dir --index-url https://download.pytorch.org/whl/cu118 torchvision==0.16.0 torchaudio==2.1.0 && \
    pip install --no-cache-dir hf_transfer
# Copy app code
COPY . /app
ENV HF_HUB_ENABLE_HF_TRANSFER=1 \
    ACE_CHECKPOINTS=/app/checkpoints \
    PORT=80 \
    PYTHONUNBUFFERED=1
# Pre-download models at build (optional); keep at runtime to avoid large images
# RUN python -c "from huggingface_hub import hf_hub_download; import os; os.makedirs('checkpoints',exist_ok=True); hf_hub_download(repo_id='ACE-Step/ACE-Step-v1-3.5B', subfolder='ace_step_transformer', filename='config.json', local_dir='checkpoints')" || true
EXPOSE 80
CMD ["bash", "-lc", "uvicorn studio_backend.app:app --host 0.0.0.0 --port ${PORT}"]
