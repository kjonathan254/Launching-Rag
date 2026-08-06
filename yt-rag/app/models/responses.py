from pydantic import BaseModel
from typing import List, Optional, Dict, Any


class AnswerResponse(BaseModel):
    text: str
    citations: List[str]
    debug: Optional[Dict[str, Any]] = None
