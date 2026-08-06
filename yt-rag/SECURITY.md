# Security Policy
## 🔐 Protecting Your API Keys

This project requires several API keys to function:
- **Supabase** (URL, Anon Key, Service Role Key)
- **OpenAI** (API Key)
- **Anthropic** (Optional, API Key)

### ⚠️ CRITICAL: Never Commit Real API Keys

**NEVER** commit real API keys, passwords, or secrets to version control. This repository uses the following security measures:

1. **`.env.example`**: Contains placeholder values only
2. **`.gitignore`**: Prevents `.env` files from being committed
3. **`.env`**: Your local file with real keys (never committed)

### ✅ Safe Workflow

```bash
# 1. Copy the example file
cp .env.example .env

# 2. Edit with YOUR real keys (this file is gitignored)
nano .env

# 3. Never commit .env - only .env.example is tracked
git add .env.example  # ✓ Safe
git add .env          # ✗ Blocked by .gitignore
```

### 🚨 If You Accidentally Committed a Key

1. **Immediately rotate/revoke** the compromised key in the provider's dashboard
2. Remove it from git history:
   ```bash
   # For recent commits
   git reset --soft HEAD~1
   # Edit the file to remove the key
   git commit --amend
   
   # For older commits, use BFG Repo-Cleaner or git filter-repo
   ```
3. Add the file pattern to `.gitignore`

### 🔒 Best Practices

- Use environment variables in production deployments
- Rotate keys regularly
- Use the principle of least privilege (use anon keys where possible)
- Monitor your API usage for unusual activity
- Never share your `.env` file

### 📚 Provider Security Documentation

- [OpenAI API Key Security](https://platform.openai.com/docs/api-reference/authentication)
- [Anthropic Security Best Practices](https://console.anthropic.com/docs)
- [Supabase Security Overview](https://supabase.com/docs/guides/auth)
