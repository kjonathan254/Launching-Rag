from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any


class SeedRequest(BaseModel):
    docs: List[Dict[str, str]] = Field(
        default_factory=list,
        description="List of documents to seed. Each doc must have chunk_id, source, and text."
    )


class AnswerRequest(BaseModel):
    query: str = Field(..., description="The user's question")
    top_k: int = Field(default=6, ge=1, le=20, description="Number of chunks to retrieve")


class AnswerResponse(BaseModel):
    text: str
    citations: List[str]
    debug: Optional[Dict[str, Any]] = None
