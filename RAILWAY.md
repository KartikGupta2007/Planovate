# Railway Deployment Environment Variables

## Required Environment Variables for Railway

Set these in your Railway project settings:

### Backend Configuration

```env
# LLM Provider (choose one)
LLM_PROVIDER=gemini

# Gemini API (Recommended - Free tier)
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-2.0-flash

# OR OpenAI API (Alternative)
# OPENAI_API_KEY=your_openai_key
# OPENAI_MODEL=gpt-4o-mini

# Server Config
DEBUG=false
PORT=$PORT  # Railway automatically provides this

# CORS Origins (Update with your frontend URL)
ALLOWED_ORIGINS=https://your-frontend-domain.vercel.app,http://localhost:5173

# File Upload Limits
MAX_IMAGE_SIZE_MB=10
```

## Railway Setup Steps:

1. **Create New Project** on Railway
2. **Connect GitHub Repository**: KartikGupta2007/Planovate
3. **Add Environment Variables** (Settings → Variables):
   - `GEMINI_API_KEY` = (your key from https://aistudio.google.com/app/apikey)
   - `LLM_PROVIDER` = `gemini`
   - `GEMINI_MODEL` = `gemini-2.0-flash`
   - `DEBUG` = `false`
   - `ALLOWED_ORIGINS` = (your frontend URL)

4. **Deploy** - Railway will automatically:
   - Install dependencies from `backend/requirements.txt`
   - Start server with Procfile command
   - Expose on generated Railway domain

5. **Verify Deployment**:
   - Visit: `https://your-project.up.railway.app/`
   - Check API docs: `https://your-project.up.railway.app/docs`
   - Health check: `https://your-project.up.railway.app/api/health`

## Troubleshooting:

- **Application failed to respond**: Check Gemini API key is set
- **Module not found**: Redeploy to reinstall dependencies
- **CORS errors**: Add frontend domain to ALLOWED_ORIGINS
- **500 errors**: Check logs in Railway dashboard

## Production Checklist:

✅ Set DEBUG=false  
✅ Add production frontend URL to ALLOWED_ORIGINS  
✅ Set valid GEMINI_API_KEY  
✅ Remove localhost origins from ALLOWED_ORIGINS  
✅ Monitor Railway logs for errors  
