from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from api.main import api_router
from common.repository import repo
import os

app = FastAPI()
app.include_router(api_router)

@app.get("/api/v1/refresh")
async def refresh():
    repo.refresh()
    return {"status": "healthy"}

@app.get("/api/v1/health")
async def health_check():
    return {"status": "healthy"}

if os.environ.get("ENV") == "DEV":
    print("Local mode")
    origins = [
        "http://127.0.0.1:5173",
        "http://127.0.0.1:8000",
        "http://localhost:8000",
        "http://localhost:5173",
        "http://localhost:5175"
    ]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )
else:
    try:
        target_dir = "front-end/dist"
        app.mount("/", StaticFiles(directory=target_dir, html=True), name="site")
    except Exception as e:
        print(f'ERROR - static not found: {str(e)}')
