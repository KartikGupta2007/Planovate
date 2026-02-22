# Production Deployment Checklist

## Pre-Deployment Checklist

### Backend Configuration
- [ ] Set `ENVIRONMENT=production` in Railway/Render
- [ ] Set `DEBUG=false` in production environment
- [ ] Configure valid `GEMINI_API_KEY` (or OpenAI)
- [ ] Set production frontend URL in `ALLOWED_ORIGINS`
- [ ] Set `ALLOWED_HOSTS` to your Railway domain
- [ ] Verify all dependencies in `requirements.txt` are installed
- [ ] Test `/api/health` endpoint returns healthy status

### Frontend Configuration
- [ ] Update `VITE_BACKEND_API_URL` to production Railway URL
- [ ] Verify Appwrite production credentials
- [ ] Set production CORS in Railway to match Vercel URL
- [ ] Test image uploads work with production backend
- [ ] Ensure UserId column exists in Appwrite database

### Security Checks
- [ ] API docs disabled in production (`DEBUG=false`)
- [ ] Security headers enabled (X-Content-Type-Options, X-Frame-Options)
- [ ] HTTPS enabled (Railway provides this automatically)
- [ ] Sensitive data not logged in production mode
- [ ] File upload size limits enforced (10MB default)

### Testing
- [ ] Test health check: `curl https://your-app.up.railway.app/`
- [ ] Test API health: `curl https://your-app.up.railway.app/api/health`
- [ ] Test image analysis endpoint with sample images
- [ ] Verify CORS headers from production frontend
- [ ] Test error handling returns proper JSON responses

### Monitoring
- [ ] Check Railway logs for startup messages
- [ ] Monitor request response times (X-Process-Time header)
- [ ] Track request IDs for debugging (X-Request-ID header)
- [ ] Set up error alerting if needed

## Railway Environment Variables

Set these in Railway Settings → Variables:

```env
ENVIRONMENT=production
DEBUG=false
GEMINI_API_KEY=your_api_key_here
LLM_PROVIDER=gemini
GEMINI_MODEL=gemini-2.0-flash
ALLOWED_ORIGINS=https://your-frontend.vercel.app
ALLOWED_HOSTS=your-app.up.railway.app
LOG_LEVEL=INFO
MAX_IMAGE_SIZE_MB=10
```

## Quick Deploy Commands

### Railway (Already configured)
```bash
git push origin main  # Railway auto-deploys
```

### Manual Railway Deploy
```bash
railway up
```

### Check Railway Logs
```bash
railway logs
```

## Production URLs

- **Backend API:** https://planovate-production.up.railway.app
- **API Docs:** Disabled in production (enable with DEBUG=true if needed)
- **Health Check:** https://planovate-production.up.railway.app/api/health
- **Frontend:** https://planovate.vercel.app

## Rollback Plan

If deployment fails:
1. Check Railway logs for errors
2. Verify environment variables are set correctly
3. Test backend locally with production settings
4. Redeploy previous working commit:
   ```bash
   git revert HEAD
   git push origin main
   ```

## Performance Tips

- Railway provides automatic scaling
- OpenCV runs in headless mode (optimized for servers)
- Request timeouts set to 30s (configurable)
- CORS preflight requests cached for 1 hour
- Images limited to 10MB to prevent memory issues

## Support

If issues occur:
- Check Railway logs: Settings → Deployments → View Logs
- Verify environment variables: Settings → Variables
- Test endpoints with curl or Postman
- Check CORS configuration matches frontend URL
