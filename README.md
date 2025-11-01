Kitchen Cashbook
A minimal web app to capture income and expenses for a cloud kitchen.
Built with FastAPI (Python backend), SQLite, and a mobile-friendly PWA frontend.

Features
Add, view, and manage income and expense entries
Mobile-responsive UI (will work on mobile web browser - preferably chrome)
PWA: Installable on Android/iOS home screen
Data stored in SQLite (backend) or browser local storage (frontend-only mode)
API endpoints for integration and automation
Quick Start
1. Clone the repository
2. Create and activate a virtual environment (Windows PowerShell)
3. Install dependencies
4. Run the server
5. Open the app

On your computer: http://localhost:8000/

On your phone (same Wi-Fi): http://<your-ip>:8000/

**Project Structure**

API Endpoints

POST /api/entries — Create a new entry

GET /api/entries — List entries

GET /api/summary?month=YYYY-MM — Get monthly summary

Deployment

Do not commit .venv or any virtual environment folders.

Add .venv and venv/ to your .gitignore.

You can deploy to Render, Railway, Fly.io, or any cloud that supports FastAPI.



Built by **Anand Velchuri**

Tech Stack used to build this app:

**Backend**

   Python 3
   - FastAPI (web framework)
   - Uvicorn (ASGI server)
   - SQLite (database)
   - Pydantic (data validation)
   - pytest (testing)

**Frontend**

   - HTML5
   - CSS3 (with responsive/mobile-first design)
   - JavaScript (ES6)
   - Progressive Web App (PWA) features
   - manifest.json
   - Service Worker

**DevOps / Tooling**

   - Git (version control)
   - pip (Python package manager)
   - venv (Python virtual environments)
   - .gitignore (to exclude venv and other files)