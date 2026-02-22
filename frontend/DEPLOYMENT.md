# Frontend Production Deployment Guide

## Production Checklist

### Before Deploying to Vercel/Netlify

1. **Environment Variables**
   - [ ] Copy `.env.production.example` to `.env.production`
   - [ ] Set `VITE_BACKEND_API_URL` to Railway production URL
   - [ ] Set all Appwrite production credentials
   - [ ] Verify all required env vars are set

2. **Code Quality**
   - [ ] Remove all `console.log` statements (now using conditional logger)
   - [ ] Test all features work with production backend
   - [ ] Verify image uploads work
   - [ ] Test user authentication flow
   - [ ] Confirm dashboard shows only user's projects

3. **Build & Test**
   ```bash
   npm run build
   npm run preview  # Test production build locally
   ```

4. **Deployment Settings**
   - **Build Command:** `npm run build`
   - **Output Directory:** `dist`
   - **Node Version:** 18+

## Vercel Deployment

### Quick Deploy

1. **Connect GitHub Repository**
   ```bash
   # Vercel will auto-detect Vite configuration
   ```

2. **Set Environment Variables** in Vercel Dashboard:
   ```env
   VITE_BACKEND_API_URL=https://planovate-production.up.railway.app
   VITE_APPWRITE_URL=https://cloud.appwrite.io/v1
   VITE_APPWRITE_PROJECT_ID=your_project_id
   VITE_APPWRITE_DATABASE_ID=your_database_id
   VITE_APPWRITE_TABLE_ID=your_table_id
   VITE_APPWRITE_BUCKET_ID=your_bucket_id
   ```

3. **Deploy**
   - Vercel auto-deploys on git push to main
   - Manual deploy: `vercel --prod`

### Custom Domain (Optional)

1. Go to Vercel Dashboard → Settings → Domains
2. Add your custom domain
3. Update DNS records as instructed
4. Update `ALLOWED_ORIGINS` in Railway backend

## Netlify Deployment

### Quick Deploy

1. **Connect GitHub Repository**

2. **Build Settings**
   - Build command: `npm run build`
   - Publish directory: `dist`

3. **Environment Variables** (same as Vercel above)

4. **Deploy**
   - Auto-deploys on git push to main
   - Manual deploy: `netlify deploy --prod`

## Post-Deployment

### Update Backend CORS

In Railway, update environment variables:
```env
ALLOWED_ORIGINS=https://your-app.vercel.app,https://www.your-app.vercel.app
```

### Test Production

- [ ] Visit production URL
- [ ] Register new user
- [ ] Login works
- [ ] Upload renovation project with images
- [ ] Click "Analyze & Generate Description"
- [ ] Verify AI analysis returns results
- [ ] Save project
- [ ] Check dashboard shows project
- [ ] Logout and login - verify project still there
- [ ] Create second project - verify both show up
- [ ] Login as different user - verify isolation (only own projects visible)

### Monitor

- Check Vercel/Netlify Analytics
- Monitor Railway backend logs
- Test CORS from production frontend
- Verify all API calls successful

## Troubleshooting

### CORS Errors
- Verify backend `ALLOWED_ORIGINS` includes frontend URL (with https://)
- Check Railway logs for CORS-related errors
- Ensure no trailing slashes in URLs

### API Calls Failing
- Check `VITE_BACKEND_API_URL` is set correctly
- Verify Railway backend is running
- Test backend health: `curl https://your-backend.up.railway.app/api/health`
- Check browser Network tab for failed requests

### Images Not Loading
- Verify Appwrite bucket permissions (public read access)
- Check Appwrite storage quota
- Confirm file IDs are being saved correctly

### Build Failures
- Run `npm run build` locally first
- Check for TypeScript/ESLint errors
- Verify all dependencies installed
- Check Node version (18+)

## Rollback

If production has issues:
```bash
# Revert to previous deploy
git revert HEAD
git push origin main
```

Or use Vercel/Netlify dashboard to rollback to previous deployment.

## Environment Comparison

| Feature | Development | Production |
|---------|-------------|------------|
| Backend URL | localhost:8000 | Railway URL |
| API Docs | Enabled | Disabled |
| Logging | Enabled | Disabled |
| HTTPS | No | Yes |
| CORS | Localhost | Production domains |
| Appwrite | Dev project | Prod project |

## Performance Optimization

Already implemented:
- ✅ Vite build optimization
- ✅ Code splitting
- ✅ Tree shaking
- ✅ Conditional logging
- ✅ Production mode builds
- ✅ Asset optimization

## Support

- **Vercel Docs:** https://vercel.com/docs
- **Netlify Docs:** https://docs.netlify.com
- **Railway Docs:** https://docs.railway.app
- **Vite Docs:** https://vitejs.dev/guide/
