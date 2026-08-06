import re
from typing import List, Dict
from app.core.config import settings


class Chunker:
    """Service for chunking text into smaller pieces for embedding."""

    def __init__(self):
        self.chunk_size = settings.chunk_size
        self.chunk_overlap = settings.chunk_overlap

    def _count_tokens(self, text: str) -> int:
        """Approximate token count (simple word-based estimation)."""
        # Simple approximation: 1 token ≈ 4 characters or 0.75 words
        words = text.split()
        return int(len(words) * 0.75)

    def _split_into_sentences(self, text: str) -> List[str]:
        """Split text into sentences."""
        # Split on common sentence boundaries
        sentences = re.split(r'(?<=[.!?])\s+', text)
        return [s.strip() for s in sentences if s.strip()]

    def chunk_text(self, text: str, chunk_id_prefix: str = "chunk") -> List[Dict[str, str]]:
        """
        Split text into overlapping chunks.
        
        Returns list of dicts with keys: chunk_id, text
        """
        sentences = self._split_into_sentences(text)
        chunks = []
        current_chunk = []
        current_token_count = 0
        chunk_index = 0

        for sentence in sentences:
            sentence_tokens = self._count_tokens(sentence)
            
            # If adding this sentence exceeds chunk_size, save current chunk
            if current_token_count + sentence_tokens > self.chunk_size and current_chunk:
                chunk_text = " ".join(current_chunk)
                chunks.append({
                    "chunk_id": f"{chunk_id_prefix}#{chunk_index}",
                    "text": chunk_text
                })
                chunk_index += 1
                
                # Remove sentences from the beginning to create overlap
                overlap_tokens = 0
                while current_chunk and overlap_tokens < self.chunk_overlap:
                    removed = current_chunk.pop(0)
                    overlap_tokens += self._count_tokens(removed)
                
                current_token_count = overlap_tokens
            
            current_chunk.append(sentence)
            current_token_count += sentence_tokens

        # Add remaining chunk
        if current_chunk:
            chunk_text = " ".join(current_chunk)
            chunks.append({
                "chunk_id": f"{chunk_id_prefix}#{chunk_index}",
                "text": chunk_text
            })

        return chunks

    def chunk_documents(self, documents: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """
        Chunk multiple documents.
        
        Each document should have: chunk_id, source, text
        Returns list of chunks with: chunk_id, source, text
        """
        all_chunks = []
        
        for doc in documents:
            doc_chunks = self.chunk_text(doc["text"], doc["chunk_id"])
            for chunk in doc_chunks:
                all_chunks.append({
                    "chunk_id": chunk["chunk_id"],
                    "source": doc.get("source", "unknown"),
                    "text": chunk["text"]
                })
        
        return all_chunks
