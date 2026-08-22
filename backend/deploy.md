# RenovAI Backend Deployment

## Render
1. Create a new Web Service and connect the GitHub repo.
2. Set the root directory to `backend`.
3. Set Python version to `3.11.11`.
4. Build command:
   - `pip install --no-cache-dir -r requirements.txt`
5. Start command:
   - `uvicorn main:app --host 0.0.0.0 --port $PORT`
6. Add environment variables from `backend/.env.example`.
7. Set production values:
   - `DEBUG=false`
   - `ENVIRONMENT=production`
   - `ALLOWED_ORIGINS=https://your-frontend-domain`
8. Deploy.

### Render Blueprint (Recommended)
- The repo includes `render.yaml` at root for one-click backend setup.

## Railway
1. Create a new project and link the GitHub repo.
2. Set the root directory to `backend`.
3. Add a Start command:
   - `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. Add environment variables from `backend/.env.example`.
5. Deploy.

## Notes
- Make sure `python-multipart` is installed for file uploads.
- LLM is optional. If not configured, the pipeline runs in deterministic mode.
- If Render defaults to Python 3.14+, `pydantic-core` may try a source build and fail.
  Pinning to Python 3.11 avoids this.
