# 🏠 Planovate – Smart Room Renovation Planner

[![FastAPI](https://img.shields.io/badge/FastAPI-0.115.0-009688?logo=fastapi)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-19.2.0-61DAFB?logo=react)](https://react.dev/)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python)](https://www.python.org/)
[![Appwrite](https://img.shields.io/badge/Appwrite-Cloud-F02E65?logo=appwrite)](https://appwrite.io/)

**AI-powered web application that analyzes your current room photos and generates optimized renovation plans with accurate cost estimations in Indian Rupees (₹).**

Upload before and after room images, set your budget, and get instant AI-powered renovation recommendations with priority-based task breakdowns, location-based pricing, and budget optimization.

---

## 📋 Table of Contents

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Architecture](#-project-architecture)
- [Installation](#-installation--setup)
- [Usage](#-usage)
- [API Documentation](#-api-documentation)
- [Project Structure](#-project-structure)
- [Configuration](#-configuration)
- [Team & Ownership](#-team--ownership)

---

## ✨ Features

### Core Capabilities

🎨 **Smart Image Analysis**
- Upload current room and ideal room photos
- AI-powered computer vision analyzes differences
- Detects issues: cracks, paint condition, lighting, flooring, ceiling damage

🤖 **AI-Powered Recommendations**
- Generates comprehensive renovation plans
- LLM integration for natural language explanations (Gemini/OpenAI/Ollama)
- Priority-based task ranking (High/Medium/Low)

💰 **Intelligent Cost Estimation**
- Location-based pricing (city/region multipliers)
- Real Indian market rates (INR)
- Budget optimization algorithm
- Detailed cost breakdown per task

📊 **User Dashboard**
- View all renovation projects
- Track budget vs estimated costs
- Project history with before/after comparisons
- Beautiful Parapixel design system

🔐 **Authentication & Storage**
- Secure user authentication (Appwrite)
- Cloud image storage
- Project data persistence
- Multi-user support

### Advanced Features

✅ Auto-budget calculation (uses AI estimate if user doesn't provide budget)  
✅ Room coverage detection and area estimation  
✅ Responsive design (mobile, tablet, desktop)  
✅ Editable project descriptions  
✅ Real-time cost summaries  
✅ Before/After showcase gallery  

---

## 🛠️ Tech Stack

### Frontend
- **Framework:** React 19.2.0 with Vite
- **Styling:** Tailwind CSS 4.2.0, Custom Parapixel Design System
- **Routing:** React Router DOM 7.13.0
- **Forms:** React Hook Form 7.71.2
- **Auth/Storage:** Appwrite SDK 22.4.0
- **State Management:** React Context API

### Backend
- **Framework:** FastAPI 0.115.0
- **Server:** Uvicorn 0.30.0 (ASGI)
- **Computer Vision:** OpenCV 4.10.0, NumPy 1.26.4
- **LLM Integration:** Gemini AI (configurable: OpenAI, Ollama)
- **Validation:** Pydantic 2.8.0
- **Environment:** Python-dotenv 1.0.1

### Infrastructure
- **Frontend Hosting:** Vite Dev Server (Production: Vercel/Netlify)
- **Backend Hosting:** Uvicorn (Production: Docker/Railway/Render)
- **Database:** Appwrite Cloud
- **File Storage:** Appwrite Storage
- **CORS:** Configured for localhost + production origins

---

## 🏗️ Project Architecture

```
┌─────────────────┐         ┌──────────────────┐         ┌─────────────────┐
│   React UI      │────────▶│   FastAPI        │────────▶│   Appwrite      │
│  (Frontend)     │  HTTP   │   (Backend)      │  SDK    │  (Cloud DB)     │
│                 │◀────────│                  │◀────────│                 │
│  - Auth Pages   │  JSON   │  - API Routes    │         │  - Auth         │
│  - Dashboard    │         │  - AI Pipeline   │         │  - Storage      │
│  - Upload Form  │         │  - LLM Service   │         │  - Database     │
└─────────────────┘         └──────────────────┘         └─────────────────┘
                                     │
                            ┌────────┴────────┐
                            ▼                 ▼
                    ┌──────────────┐  ┌──────────────┐
                    │  OpenCV      │  │  Gemini AI   │
                    │  Vision      │  │  LLM API     │
                    │  Analysis    │  │  Service     │
                    └──────────────┘  └──────────────┘
```

### Data Flow

1. **User uploads images** → Frontend sends to `/api/analyze`
2. **Backend receives request** → Validates images, extracts metadata
3. **AI Vision Module** → Analyzes images, generates feature vectors
4. **Pricing Engine** → Calculates costs with location multipliers
5. **Optimizer** → Fits plan within budget (if provided)
6. **LLM Service** → Generates human-readable explanations
7. **Backend responds** → Returns plan with costs and descriptions
8. **Frontend displays** → Auto-fills comprehensive project description
9. **User saves project** → Stores in Appwrite with images

---

## 🚀 Installation & Setup

### Prerequisites

- **Node.js** 18+ ([Download](https://nodejs.org/))
- **Python** 3.10+ ([Download](https://www.python.org/downloads/))
- **Git** ([Download](https://git-scm.com/downloads))
- **Appwrite Account** ([Sign up](https://cloud.appwrite.io/))

### Step 1: Clone Repository

```bash
git clone https://github.com/yourusername/planovate.git
cd planovate
```

### Step 2: Backend Setup

#### 2.1 Create Python Virtual Environment

```bash
cd backend
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

#### 2.2 Install Dependencies

```bash
pip install -r requirements.txt
```

#### 2.3 Configure Environment Variables

```bash
cp .env.example .env
```

Edit `.env` file with your configuration:

```env
# Server Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=true

# CORS Origins (comma-separated)
ALLOWED_ORIGINS=http://localhost:5173,http://localhost:5174,http://localhost:3000

# File Upload Limits
MAX_IMAGE_SIZE_MB=10

# LLM Provider (choose: gemini, openai, ollama)
LLM_PROVIDER=gemini
LLM_TIMEOUT=12

# Gemini API (Recommended - Free tier available)
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-2.0-flash

# OpenAI API (Alternative)
OPENAI_API_KEY=your_openai_key
OPENAI_MODEL=gpt-4o-mini

# Ollama (Local LLM - Alternative)
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.1
```

**Get Gemini API Key:** https://aistudio.google.com/app/apikey

#### 2.4 Start Backend Server

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Backend will run at: **http://localhost:8000**  
API Docs: **http://localhost:8000/docs** (Swagger UI)

---

### Step 3: Frontend Setup

#### 3.1 Install Dependencies

```bash
cd ../frontend
npm install
```

#### 3.2 Configure Environment Variables

```bash
cp .env.example .env
```

Edit `.env` file with your Appwrite credentials:

```env
# Appwrite Configuration
VITE_APPWRITE_URL=https://cloud.appwrite.io/v1
VITE_APPWRITE_PROJECT_ID=your_project_id
VITE_APPWRITE_DATABASE_ID=your_database_id
VITE_APPWRITE_TABLE_ID=your_table_id
VITE_APPWRITE_BUCKET_ID=your_bucket_id

# Backend API
VITE_BACKEND_API_URL=http://localhost:8000

# Optional
VITE_TINYMCE_EDITOR_ID=your_tinymce_id
```

#### 3.3 Setup Appwrite Project

1. **Create Appwrite Project** at https://cloud.appwrite.io/
2. **Create Database** → Copy Database ID
3. **Create Collection (Table)** with these attributes:
   - `Title` (String, required)
   - `City` (String, required)
   - `CurrentPhoto` (String, required) - stores file ID
   - `Idealphoto` (String, required) - stores file ID  ⚠️ lowercase 'p'
   - `Budget` (Integer, optional, min: 15000)
   - `Description` (String, required, size: 10000)
4. **Create Storage Bucket** → Copy Bucket ID
5. **Enable Auth** → Email/Password provider

#### 3.4 Start Frontend Server

```bash
npm run dev
```

Frontend will run at: **http://localhost:5173** (or 5174)

---

## 📖 Usage

### 1. Register & Login

- Open http://localhost:5173
- Click "Sign Up" → Create account
- Login with credentials

### 2. Create New Project

- Click **"+ NEW RENOVATION"** on dashboard
- Fill in project details:
  - **Project Title** (e.g., "Living Room Renovation")
  - **City** (e.g., "Mumbai")
  - **Upload Current Photo** (your room's current state)
  - **Upload Ideal Photo** (your room's desired state)
  - **Budget (Optional)** (e.g., ₹100,000)

### 3. Generate AI Analysis

- Click **"Analyze & Generate Description"**
- Wait 5-10 seconds for AI processing
- Review generated plan with:
  - Overall condition assessment
  - Priority-based task list with costs
  - Individual task descriptions
  - Total cost estimation
  - Budget optimization status

### 4. Save & View Project

- Click **"Create Project"**
- View on dashboard with before/after images
- Check detailed breakdown anytime

---

## 🔌 API Documentation

### Base URL
```
http://localhost:8000
```

### Endpoints

#### 1. Analyze Renovation
```http
POST /api/analyze
Content-Type: multipart/form-data
```

**Request Body:**
```
old_image: File (JPEG/PNG/WebP, required)
new_image: File (JPEG/PNG/WebP, required)
budget: Float (INR, optional)
location: String (city name, optional)
room_area: Float (sqft, optional)
llm_provider: String (gemini/openai/ollama, optional)
llm_api_key: String (your API key, optional)
llm_model: String (model name, optional)
```

**Response:**
```json
{
  "score": 0.65,
  "estimated_cost": 72000.0,
  "optimized": true,
  "currency": "INR",
  "plan": [
    {
      "task": "Crack repair",
      "priority": "high",
      "cost": 15000.0,
      "description": "Fix wall cracks with cement putty and primer"
    }
  ],
  "explanation": "Based on our analysis, moderate renovation is needed..."
}
```

#### 2. Health Check
```http
GET /api/health
```

**Response:**
```json
{
  "status": "ok"
}
```

#### 3. User History
```http
GET /api/history/{user_id}
```

**Response:**
```json
[
  {
    "project_id": "uuid",
    "created_at": "2026-02-22T10:30:00",
    "score": 0.65,
    "estimated_cost": 72000.0,
    "optimized": true
  }
]
```

### Interactive API Docs

Visit **http://localhost:8000/docs** for Swagger UI with live testing.

---

## 📁 Project Structure

```
Planovate/
├── frontend/                          # React Frontend Application
│   ├── src/
│   │   ├── components/
│   │   │   ├── Navbar.jsx            # Navigation with logo/auth
│   │   │   ├── BeforeAfterShowcase.jsx  # Gallery component
│   │   │   └── pages/
│   │   │       ├── Dashboard.jsx     # Main dashboard (logged in/out)
│   │   │       ├── Upload.jsx        # Project creation form
│   │   │       ├── Login.jsx         # Authentication
│   │   │       ├── Register.jsx      # User registration
│   │   │       ├── History.jsx       # Project history
│   │   │       └── eachOldProject.jsx  # Project detail view
│   │   ├── appwrite/
│   │   │   ├── auth.js               # Auth service
│   │   │   └── service.js            # Database & storage service
│   │   ├── api/
│   │   │   └── renovation.js         # Backend API client
│   │   ├── context/
│   │   │   └── AuthContext.jsx       # Global auth state
│   │   ├── Conf/
│   │   │   └── conf.js               # Environment config
│   │   ├── assets/                   # Images, icons
│   │   ├── App.jsx                   # Root component
│   │   └── main.jsx                  # Entry point
│   ├── public/                       # Static files
│   ├── package.json                  # Dependencies
│   ├── vite.config.js                # Vite configuration
│   ├── tailwind.config.js            # Tailwind CSS config
│   └── .env.example                  # Environment template
│
├── backend/                          # Python FastAPI Backend
│   ├── main.py                       # FastAPI application entry
│   ├── config.py                     # Settings & environment
│   ├── api/                          # API Layer (Member 2)
│   │   ├── routes.py                 # HTTP endpoints
│   │   ├── schemas.py                # Pydantic models
│   │   └── dependencies.py           # Dependency injection
│   ├── ai/                           # Computer Vision (Member 3)
│   │   ├── vision.py                 # OpenCV image analysis
│   │   ├── feature_vector.py         # Feature extraction
│   │   ├── scoring.py                # Damage scoring
│   │   └── preprocessing.py          # Image preprocessing
│   ├── services/                     # Business Logic (Member 4)
│   │   ├── pipeline.py               # Main orchestrator
│   │   ├── llm_service.py            # LLM integration (Gemini/OpenAI)
│   │   ├── pricing_engine.py         # Cost calculation with multipliers
│   │   ├── optimizer.py              # Budget optimization algorithm
│   │   ├── constants.py              # Configuration constants
│   │   └── cache.py                  # LLM response caching
│   ├── storage/                      # User uploaded files (gitignored)
│   ├── data/                         # Cached data (gitignored)
│   ├── requirements.txt              # Python dependencies
│   └── .env.example                  # Environment template
│
├── shared/                           # Shared Contracts
│   └── contracts.json                # Frozen API schemas
│
├── docs/                             # Documentation
│   └── SETUP.md                      # Original setup guide
│
├── README.md                         # This file
└── .gitignore                        # Git ignore rules
```

---

## ⚙️ Configuration

### Backend Configuration (`backend/.env`)

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `HOST` | Server host | `0.0.0.0` | No |
| `PORT` | Server port | `8000` | No |
| `DEBUG` | Debug mode | `true` | No |
| `ALLOWED_ORIGINS` | CORS origins (comma-separated) | `localhost:5173,5174,3000` | Yes |
| `MAX_IMAGE_SIZE_MB` | Max upload size | `10` | No |
| `LLM_PROVIDER` | LLM service (`gemini`/`openai`/`ollama`) | `gemini` | Yes |
| `GEMINI_API_KEY` | Google Gemini API key | - | If using Gemini |
| `GEMINI_MODEL` | Gemini model name | `gemini-2.0-flash` | No |
| `OPENAI_API_KEY` | OpenAI API key | - | If using OpenAI |
| `OPENAI_MODEL` | OpenAI model | `gpt-4o-mini` | No |

### Frontend Configuration (`frontend/.env`)

| Variable | Description | Required |
|----------|-------------|----------|
| `VITE_APPWRITE_URL` | Appwrite endpoint | Yes |
| `VITE_APPWRITE_PROJECT_ID` | Appwrite project ID | Yes |
| `VITE_APPWRITE_DATABASE_ID` | Database ID | Yes |
| `VITE_APPWRITE_TABLE_ID` | Collection ID | Yes |
| `VITE_APPWRITE_BUCKET_ID` | Storage bucket ID | Yes |
| `VITE_BACKEND_API_URL` | Backend URL | Yes (default: `http://localhost:8000`) |

### Pricing Configuration

Located in `backend/services/constants.py`:

```python
# Base rates (INR) - Indian market rates 2024-25
CRACK_REPAIR_PER_SQFT = 200        # Cement putty + primer
PAINT_MATTE_PER_SQFT = 45          # Primer + 2 coats
PAINT_WATERPROOF_PER_SQFT = 70     # Waterproof coating
LIGHTING_BASIC_PER_UNIT = 2500     # LED panel with wiring
FLOORING_TILE_PER_SQFT = 250       # Vitrified tiles + laying
CEILING_BASIC_PER_SQFT = 110       # Gypsum board + finish

LABOR_FACTOR = 0.35                # 35% labor surcharge
BUFFER_FACTOR = 0.1                # 10% contingency
MIN_BUDGET = 15000                 # Minimum project budget
```

---

## 👥 Team & Ownership

This project follows a modular team structure with clear ownership:

| Member | Responsibility | Tech Stack | Files |
|--------|----------------|------------|-------|
| **Member 1** | Frontend UI & Appwrite Integration | React, Tailwind CSS, Appwrite SDK | `frontend/src/` |
| **Member 2** | Backend API & Routing | FastAPI, Pydantic | `backend/api/`, `main.py`, `config.py` |
| **Member 3** | Computer Vision & AI Analysis | OpenCV, NumPy | `backend/ai/` |
| **Member 4** | LLM Integration, Optimization & Deployment | Gemini/OpenAI, Algorithm Design | `backend/services/`, `requirements.txt` |

### Git Workflow

1. **Branch Naming:** `feature/m{number}-{description}`
   - Member 1: `feature/m1-dashboard`
   - Member 2: `feature/m2-api-routes`
   - Member 3: `feature/m3-vision-model`
   - Member 4: `feature/m4-llm-service`

2. **Workflow:**
   ```bash
   git checkout -b feature/m1-new-feature
   # Make changes
   git add .
   git commit -m "Add feature description"
   git pull origin main  # Before pushing
   git push origin feature/m1-new-feature
   # Create Pull Request
   ```

3. **Rules:**
   - Work only in your assigned folder
   - Pull before push to avoid conflicts
   - Test locally before merging
   - Keep `shared/contracts.json` frozen (team agreement required for changes)

---

## 🎨 Design System

**Parapixel Theme** - Bold, modern, and playful

### Colors
- **Background:** `#F4EFE4` (Cream)
- **Text:** `#111` (Black)
- **Primary CTA:** `#ADFF2F` (Lime Green)
- **Accent:** `#FF1F5A` (Pink)
- **Border:** `#111` (Black, 2px solid)

### Typography
- **Display:** Lilita One (Headers, Hero Text)
- **UI:** Boogaloo (Buttons, Labels)
- **Body:** System fonts

### Components
- Hard shadows: `4px 4px 0px #111`
- Border radius: `8px` to `999px` (pills)
- Hover effects: Scale, translate, color shifts
- Animated blobs with 3D rotation keyframes

---

## 🐛 Troubleshooting

### Backend Issues

**Port 8000 already in use:**
```bash
# Kill existing process
lsof -ti:8000 | xargs kill -9

# Or use different port
uvicorn main:app --reload --port 8001
```

**ModuleNotFoundError:**
```bash
# Ensure venv is activated
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

**CORS Errors:**
- Add frontend port to `ALLOWED_ORIGINS` in `backend/.env`
- Restart backend server after changes

### Frontend Issues

**Appwrite Connection Failed:**
- Verify credentials in `frontend/.env`
- Check Appwrite console permissions
- Ensure database and bucket exist

**Images Not Displaying:**
- Check attribute names: `CurrentPhoto`, `Idealphoto` (exact casing)
- Verify file IDs are saved correctly
- Test with `getFileView()` method

**Build Errors:**
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

---

## 📄 License

MIT License - See LICENSE file for details

---

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

---

## 📞 Support

For issues and questions:
- **GitHub Issues:** [Create an issue](https://github.com/yourusername/planovate/issues)
- **Documentation:** Check this README and `docs/SETUP.md`
- **API Docs:** http://localhost:8000/docs (when running)

---

**Made with ❤️ by Team Planovate**
