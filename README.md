# WRC486 Pass Management System

This project is a pass management system for an enterprise, built with Django (backend), React (frontend), PostgreSQL (database), and fully containerized with Docker.

## Features
- User authentication (JWT)
- Pass creation, editing, printing, and emailing
- Uses data from a PostgreSQL database (names, departments, etc.)
- Passes are saved to an archive database
- Template editor for pass forms (DOCX)
- Admin panel for user and template management

## Project Structure
- `backend/` — Django REST API
- `frontend/` — React SPA
- `templates/` — Pass templates (DOCX)
- `docs/` — Documentation (explanatory note, presentation, etc.)

## Quick Start
1. Install Docker and Docker Compose
2. Run: `docker-compose up --build`
3. Access the frontend at `http://localhost:3000` and the backend at `http://localhost:8010`

## Documentation
- See `templates/Blank_razovogo_propuska.docx` for the pass template

---
For detailed setup and development instructions, see the full documentation in the `docs/` folder. 
