-- Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Create rag_chunks table
CREATE TABLE IF NOT EXISTS rag_chunks (
    id BIGSERIAL PRIMARY KEY,
    chunk_id TEXT UNIQUE NOT NULL,
    source TEXT NOT NULL,
    text TEXT NOT NULL,
    embedding VECTOR(3072),  -- Supports up to 3072 dimensions for text-embedding-3-large
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create index on chunk_id for fast lookups
CREATE INDEX IF NOT EXISTS idx_rag_chunks_chunk_id ON rag_chunks(chunk_id);

-- Create index on source for filtering
CREATE INDEX IF NOT EXISTS idx_rag_chunks_source ON rag_chunks(source);

-- Create HNSW index for vector similarity search (optimized for high-dimensional vectors)
CREATE INDEX IF NOT EXISTS idx_rag_chunks_embedding 
ON rag_chunks 
USING hnsw (embedding vector_cosine_ops)
WITH (m = 16, ef_construction = 64);

-- Create function for vector similarity search
CREATE OR REPLACE FUNCTION match_chunks(
    query_embedding VECTOR(3072),
    match_count INT DEFAULT 6
)
RETURNS TABLE(
    chunk_id TEXT,
    source TEXT,
    text TEXT,
    similarity FLOAT
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT
        rc.chunk_id,
        rc.source,
        rc.text,
        1 - (rc.embedding <=> query_embedding) AS similarity
    FROM rag_chunks rc
    ORDER BY rc.embedding <=> query_embedding
    LIMIT match_count;
END;
$$;

-- Create function for updating updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create trigger for auto-updating updated_at
CREATE TRIGGER update_rag_chunks_updated_at
    BEFORE UPDATE ON rag_chunks
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Row Level Security (RLS) policies for future auth integration
ALTER TABLE rag_chunks ENABLE ROW LEVEL SECURITY;

-- Allow public read access (can be restricted later with auth)
CREATE POLICY "Allow public read access" ON rag_chunks
    FOR SELECT
    USING (true);

-- Allow insert/update/delete with service role
CREATE POLICY "Allow service role full access" ON rag_chunks
    FOR ALL
    USING (true)
    WITH CHECK (true);

-- Grant necessary permissions
GRANT ALL ON rag_chunks TO authenticated;
GRANT ALL ON rag_chunks TO anon;
GRANT USAGE ON SCHEMA public TO authenticated;
GRANT USAGE ON SCHEMA public TO anon;
