from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Optional, Literal, Dict, Any
import time

class GenerateRequest(BaseModel):
    prompt: str = Field(..., description="Tags/genre/etc")
    lyrics: str = Field("", description="Optional lyrics text")
    duration: float = Field(-1, description="Seconds; -1 for random 30-240")
    steps: int = Field(60, ge=1, le=200)
    guidance_scale: float = Field(15.0)
    omega_scale: float = Field(10.0)
    guidance_scale_text: float = Field(0.0)
    guidance_scale_lyric: float = Field(0.0)
    cfg_type: Literal['apg','cfg','double','zero_star'] = 'apg'

class JobStatus(BaseModel):
    job_id: str
    status: Literal['queued','running','succeeded','failed']
    created_at: float
    started_at: Optional[float] = None
    ended_at: Optional[float] = None
    progress: Optional[Dict[str, Any]] = None
    output_path: Optional[str] = None
    error: Optional[str] = None
    params: Optional[Dict[str, Any]] = None
