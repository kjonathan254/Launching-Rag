from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.models.requests import SeedRequest, AnswerRequest
from app.models.responses import AnswerResponse
from app.services.rag import RAGService
import time

app = FastAPI(
    title="YT-RAG API",
    description="RAG (Retrieval-Augmented Generation) API with Supabase and Multi-AI Support",
    version="1.0.0"
)

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize RAG service
rag_service = RAGService()


@app.get("/healthz")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "timestamp": time.time()}


@app.post("/seed")
async def seed_knowledge_base(request: SeedRequest):
    """
    Seed the knowledge base with documents.
    
    If no documents provided, seeds with default example documents.
    """
    try:
        if not request.docs:
            # Default example documents
            request.docs = [
                {
                    "chunk_id": "policy_returns_v1",
                    "source": "https://help.example.com/returns",
                    "text": (
                        "You can return unworn items within 30 days of purchase. "
                        "Items must be in original condition with tags attached. "
                        "Refunds will be processed to the original payment method within 5-7 business days. "
                        "Sale items are final sale and cannot be returned unless defective."
                    )
                },
                {
                    "chunk_id": "policy_shipping_v1",
                    "source": "https://help.example.com/shipping",
                    "text": (
                        "We offer free standard shipping on orders over $50. "
                        "Standard shipping takes 5-7 business days. "
                        "Express shipping (2-3 business days) is available for $9.99. "
                        "Overnight shipping is available for $19.99. "
                        "We currently ship only within the United States."
                    )
                }
            ]
        
        num_chunks = rag_service.seed_documents(request.docs)
        
        return {
            "message": f"Successfully seeded {num_chunks} chunks",
            "documents_received": len(request.docs)
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/answer", response_model=AnswerResponse)
async def answer_question(request: AnswerRequest):
    """
    Answer a question using RAG.
    
    Retrieves relevant chunks from the knowledge base and generates an answer with citations.
    """
    try:
        result = rag_service.answer_question(request.query, request.top_k)
        return AnswerResponse(**result)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "name": "YT-RAG API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }
