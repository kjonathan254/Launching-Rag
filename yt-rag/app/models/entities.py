from pydantic import BaseModel
from typing import Optional


class ChunkEntity(BaseModel):
    chunk_id: str
    source: str
    text: str
    embedding: Optional[list] = None
