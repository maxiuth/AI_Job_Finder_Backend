# JobFit — AI-Powered Job Finder and Matching Platform

JobFit helps job seekers find relevant openings and understand exactly how well they match each role. It pulls live job listings from an external API, compares them against the user's resume using Google Gemini, and returns a fit score along with actionable feedback and a personalized improvement plan (e.g., certifications, courses, skill gaps to close).

## Features

- **User Authentication** — Secure login/registration with JWT or Firebase OAuth
- **Job Search** — Search by job title and location, powered by the OpenWebNinja Jobs API
- **AI Resume Matching** — Each job listing is evaluated against the user's resume using Google Gemini
- **Detailed Feedback** — For every job, users receive:
  - A fit/match score
  - Strengths and gaps relative to the role
  - A personalized improvement plan (courses, certifications, skills to develop)
- **Activity Tracking** — Stores jobs viewed and jobs applied to, tied to the user's account
- **Resume Pre-processing** — Resume is parsed and structured once, then reused for fast comparisons

## Tech Stack

**Frontend**

- React

**Backend**

- Python (Flask / FastAPI — specify which)

**Database**

- Stores: user name, email, password (hashed), jobs viewed, jobs applied

**External Services**

- [OpenWebNinja](https://www.openwebninja.com/) — Job listings API
- Google Gemini — Resume-to-job fit analysis and feedback generation
- Firebase OAuth or JWT — Authentication

## Architecture Overview

```
┌─────────────┐      ┌──────────────┐      ┌────────────────────┐
│   React     │ ───► │  Python API  │ ───► │  OpenWebNinja API   │
│  (Frontend) │      │  (Backend)   │      │  (Job Listings)     │
└─────────────┘      └──────┬───────┘      └────────────────────┘
                             │
                             ├──► Google Gemini (Resume ↔ Job Fit Analysis)
                             │
                             └──► Database (Users, Viewed/Applied Jobs)
```

**Flow:**

1. User registers/logs in (JWT or Firebase OAuth)
2. User enters desired job title + location
3. Backend queries OpenWebNinja API for matching listings
4. Each listing + the user's pre-processed resume is sent to Gemini for evaluation
5. Backend returns jobs enriched with fit scores, feedback, and improvement plans
6. User actions (viewed/applied) are logged to the database

## Getting Started

### Prerequisites

- Node.js (for the React frontend)
- Python 3.x (for the backend)
- API keys for:
  - OpenWebNinja
  - Google Gemini
  - Firebase (if using Firebase OAuth)

### Installation

1. Clone the repository

   ```bash
   git clone https://github.com/your-username/jobfit.git
   cd jobfit
   ```

2. **Backend setup**

   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate   # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Frontend setup**

   ```bash
   cd frontend
   npm install
   ```

4. **Environment variables**

   Create a `.env` file in the backend directory:

   ```
   OPENWEBNINJA_API_KEY=your_key_here
   GEMINI_API_KEY=your_key_here
   JWT_SECRET=your_secret_here
   FIREBASE_CONFIG=your_config_here
   DATABASE_URL=your_database_url_here
   ```

5. **Run the app**

   ```bash
   # Backend
   cd backend
   python app.py

   # Frontend (in a separate terminal)
   cd frontend
   npm start
   ```

## Database Schema (Draft)

| Table          | Fields                                              |
| -------------- | --------------------------------------------------- |
| `users`        | id, name, email, password_hash, created_at          |
| `jobs_viewed`  | id, user_id, job_id, job_title, company, viewed_at  |
| `jobs_applied` | id, user_id, job_id, job_title, company, applied_at |

## Security

- Passwords are hashed before storage (never stored in plain text)
- Authentication via JWT or Firebase OAuth
- API keys and secrets stored in environment variables, never committed to source control
- HTTPS enforced in production

## Roadmap

- [ ] User authentication (JWT / Firebase OAuth)
- [ ] Resume upload and pre-processing pipeline
- [ ] OpenWebNinja API integration
- [ ] Gemini-based fit scoring and feedback generation
- [ ] Jobs viewed/applied tracking
- [ ] Frontend UI for search, results, and feedback display
- [ ] Deployment
