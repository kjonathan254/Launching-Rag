# YT-RAG: RAG API with Supabase and Multi-AI Support

FastAPI backend with automatic API documentation, Supabase integration with pgvector for vector similarity search, multi-AI provider support (OpenAI & Anthropic), and Docker containerization.

## 🎯 Features

- **FastAPI backend** with automatic API documentation
- **Supabase integration** with pgvector for vector similarity search
- **Multi-AI Provider support** (OpenAI & Anthropic)
- **Vector embeddings** with semantic search
- **Citation-based answers** with source tracking
- **Frontend-ready architecture** for NextJS integration
- **Docker containerization** for easy deployment

## 🏗️ Architecture

```
yt-rag/
├── app/
│   ├── core/           # Infrastructure (config, database)
│   ├── models/         # Pydantic data models
│   ├── services/       # Business logic (RAG, embeddings)
│   └── main.py         # FastAPI application
├── sql/
│   └── init_supabase.sql  # Database initialization script
├── .env.example
├── requirements.txt
├── Dockerfile
└── README.md
```

## 🚀 Quick Start Guide

### Prerequisites
- Python 3.11+
- Supabase account
- OpenAI API key
- Anthropic API key (optional, for Claude)

### Step 1: Clone and Install Dependencies

```bash
cd yt-rag

# Create virtual environment
python3.11 -m venv venv_yt_rag
source venv_yt_rag/bin/activate  # On Windows: venv_yt_rag\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Get API Keys

#### Supabase Setup:
1. Go to supabase.com and create a new project
2. Wait for project to be ready (~2 minutes)
3. Go to Settings → API and copy:
   - Project URL
   - Anon public key
   - Service role secret key

#### OpenAI Setup:
1. Go to platform.openai.com
2. Create account/sign in → API Keys → Create new key
3. Copy the key

### Step 3: Configure Environment

```bash
cp .env.example .env
nano .env  # Edit with your real API keys
```

Update `.env`:
```env
SUPABASE_URL=https://your-project-ref.supabase.co
SUPABASE_ANON_KEY=your_anon_key_here
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key_here
OPENAI_API_KEY=sk-your_openai_key_here
OPENAI_EMBED_MODEL=text-embedding-3-small  # 1536 dimensions
OPENAI_CHAT_MODEL=gpt-4o
AI_PROVIDER=openai
```

### Step 4: Initialize Database

1. Open Supabase Dashboard → SQL Editor
2. Click "New query"
3. Copy entire contents of `sql/init_supabase.sql`
4. Paste and click "Run"

### Step 5: Start the Server

```bash
uvicorn app.main:app --reload --port 8000
```

The API will be available at:
- API: http://localhost:8000
- Interactive Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 📚 API Usage

### Health Check
```bash
curl http://localhost:8000/healthz
```

### Seed Knowledge Base
```bash
curl -X POST http://localhost:8000/seed
```

### Ask Questions (RAG)
```bash
curl -X POST http://localhost:8000/answer \
  -H "Content-Type: application/json" \
  -d '{"query": "Can I return shoes after 30 days?", "top_k": 6}'
```

Example Response:
```json
{
  "text": "Based on our return policy, you can return unworn shoes within 30 days...",
  "citations": ["policy_returns_v1#0"],
  "debug": {
    "top_doc_ids": ["policy_returns_v1#0"],
    "latency_ms": 1250
  }
}
```

## 🔧 Configuration Options

### AI Providers

**OpenAI (Recommended):**
```env
AI_PROVIDER=openai
OPENAI_API_KEY=your_key
OPENAI_EMBED_MODEL=text-embedding-3-small  # 1536 dimensions
OPENAI_CHAT_MODEL=gpt-4o-mini
```

**Anthropic Claude:**
```env
AI_PROVIDER=anthropic
ANTHROPIC_API_KEY=your_key
ANTHROPIC_CHAT_MODEL=claude-3-5-sonnet-20241022
OPENAI_API_KEY=your_openai_key  # Still needed for embeddings
```

### RAG Parameters
Adjust in `app/core/config.py`:
- `chunk_size`: Token limit per chunk (default: 400)
- `chunk_overlap`: Overlap between chunks (default: 60 tokens)
- `default_top_k`: Number of chunks to retrieve (default: 6)
- `temperature`: LLM creativity (default: 0.1)

## 🐳 Docker Deployment

```bash
# Build image
docker build -t yt-rag .

# Run container
docker run -p 8080:8080 --env-file .env yt-rag
```

## 🔮 NextJS Frontend Integration

```javascript
// lib/supabase.js
import { createClient } from '@supabase/supabase-js'

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY
)

// API calls to your backend
const response = await fetch('http://localhost:8000/answer', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ query: 'user question' })
})
```

## 🛠️ Development

### Code Quality
```bash
# Format code
black app/
isort app/

# Lint code
flake8 app/
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request
