# Frontend

Browser UI for campus police pre-reception:

- Voice-to-text via Web Speech API (Chrome / Edge recommended)
- Text report submission to `POST /api/v1/reason`
- Leaflet map with nearby radius for extracted incident locations

The backend serves `frontend/public` at `http://127.0.0.1:8000/` when you run uvicorn from `backend/`.
