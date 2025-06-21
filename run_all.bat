@echo off

echo Запуск FastAPI...
start cmd /k "cd backend && ..\.venv\Scripts\uvicorn.exe app.main:app --reload"

echo Запуск Vue фронтенда...
start cmd /k "cd frontend && npm run dev"
