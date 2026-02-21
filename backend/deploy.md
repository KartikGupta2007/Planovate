# RenovAI Backend Deployment

## Render
1. Create a new Web Service and connect the GitHub repo.
2. Set the root directory to `backend`.
3. Build command:
   - `pip install -r requirements.txt`
4. Start command:
   - `uvicorn main:app --host 0.0.0.0 --port 8000`
5. Add environment variables from `backend/.env.example`.
6. Deploy.

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
