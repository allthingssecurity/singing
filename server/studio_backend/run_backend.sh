#!/usr/bin/env bash
set -euo pipefail
here=$(cd "$(dirname "$0")" && pwd)
cd "$here/.."
source .venv/bin/activate
export ACE_CHECKPOINTS=checkpoints
exec uvicorn studio_backend.app:app --host 127.0.0.1 --port 8000 --workers 1
