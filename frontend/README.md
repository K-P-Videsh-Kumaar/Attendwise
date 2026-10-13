# AttendWise frontend

The frontend is a responsive React + Vite single-page application. It uses Framer Motion for interface transitions and calls the AttendWise FastAPI API.

## Run locally

Start the backend first:

```bash
cd ../backend
source .venv/bin/activate
uvicorn app.main:app --reload
```

Then serve this directory on port 5173 (the backend's default allowed frontend origin):

```bash
cd ../frontend
npm install
npm run dev
```

Open `http://localhost:5173`. Create an account and add a subject to get started.

Run `npm run build` to create a production build in `dist/`.
