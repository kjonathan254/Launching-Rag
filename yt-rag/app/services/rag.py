import time
from typing import List, Dict, Tuple
from app.core.database import get_supabase_client
from app.services.embedding import EmbeddingService, ChatService
from app.services.chunker import Chunker
from app.core.config import settings


class RAGService:
    """Retrieval-Augmented Generation service."""

    def __init__(self):
        self.supabase = get_supabase_client()
        self.embedding_service = EmbeddingService()
        self.chat_service = ChatService()
        self.chunker = Chunker()

    def seed_documents(self, documents: List[Dict[str, str]]) -> int:
        """
        Seed the database with documents.
        
        Each document should have: chunk_id, source, text
        Returns number of chunks inserted.
        """
        # Chunk the documents
        chunks = self.chunker.chunk_documents(documents)
        
        if not chunks:
            return 0
        
        # Generate embeddings for all chunks
        texts = [chunk["text"] for chunk in chunks]
        embeddings = self.embedding_service.get_embeddings(texts)
        
        # Prepare data for insertion
        rows = []
        for i, chunk in enumerate(chunks):
            rows.append({
                "chunk_id": chunk["chunk_id"],
                "source": chunk["source"],
                "text": chunk["text"],
                "embedding": embeddings[i]
            })
        
        # Insert into Supabase
        result = self.supabase.table("rag_chunks").upsert(rows).execute()
        
        return len(rows)

    def search_similar(self, query: str, top_k: int = 6) -> List[Dict]:
        """
        Search for similar chunks using vector similarity.
        
        Returns list of chunks with metadata.
        """
        # Generate embedding for query
        query_embedding = self.embedding_service.get_embedding(query)
        
        # Call RPC function for vector search
        result = self.supabase.rpc(
            "match_chunks",
            {
                "query_embedding": query_embedding,
                "match_count": top_k
            }
        ).execute()
        
        return result.data if result.data else []

    def answer_question(self, query: str, top_k: int = 6) -> Dict:
        """
        Answer a question using RAG.
        
        Returns dict with: text, citations, debug info
        """
        start_time = time.time()
        
        # Retrieve relevant chunks
        chunks = self.search_similar(query, top_k)
        
        if not chunks:
            return {
                "text": "I don't have enough information to answer that question.",
                "citations": [],
                "debug": {"top_doc_ids": [], "latency_ms": int((time.time() - start_time) * 1000)}
            }
        
        # Build context from retrieved chunks
        context_parts = []
        citations = []
        
        for chunk in chunks:
            context_parts.append(f"[{chunk['chunk_id']}]: {chunk['text']}")
            citations.append(chunk["chunk_id"])
        
        context = "\n\n".join(context_parts)
        
        # Build prompt for LLM
        messages = [
            {
                "role": "system",
                "content": (
                    "You are a helpful assistant that answers questions based on the provided context. "
                    "Always cite your sources using the format [chunk_id]. "
                    "If the context doesn't contain enough information, say so clearly."
                )
            },
            {
                "role": "user",
                "content": f"Context:\n{context}\n\nQuestion: {query}\n\nAnswer:"
            }
        ]
        
        # Get answer from LLM
        answer = self.chat_service.chat(messages, temperature=settings.temperature)
        
        latency_ms = int((time.time() - start_time) * 1000)
        
        return {
            "text": answer,
            "citations": citations,
            "debug": {
                "top_doc_ids": [chunk["chunk_id"] for chunk in chunks],
                "latency_ms": latency_ms
            }
        }
