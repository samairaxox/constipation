# Hackathon Project Template

This is a full-stack starter template for the hackathon.

## 📂 Project Structure

- **frontend/**: React (Vite) application with Tailwind CSS, Recharts, and a Dashboard layout.
- **backend/**: FastAPI (Python) server with basic health check endpoints.
- **agents/**: Placeholder Python modules for Generative AI agents (Marketing, Finance, Orchestrator).

## 🚀 Getting Started

Follow these steps to get the project running.

### 1️⃣ Frontend Setup (React)

Open a terminal and run:

```bash
cd frontend
npm install
npm run dev
```

The app will be available at `http://localhost:5173`.

### 2️⃣ Backend Setup (FastAPI)

Open a **new** terminal and run:

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.
Docs available at `http://127.0.0.1:8000/docs`.

### 3️⃣ AI Agents

The `agents/` folder contains boilerplate code. You can run the orchestrator manually to test:

```bash
python agents/orchestrator.py
```

## 🛠 Tech Stack

- **Frontend**: React, Vite, Tailwind CSS, Recharts, Axios
- **Backend**: FastAPI, Uvicorn
- **AI**: Python (Multi-agent structure)

Happy Hacking! 🚀
