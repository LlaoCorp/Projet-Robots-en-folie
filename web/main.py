from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from api.router import router as robot_router
from fastapi.middleware.cors import CORSMiddleware
from database.init_db import init_db
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI()
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")


origins = [
    "http://127.0.0.1:8000",
    "http://localhost",
    "http://localhost:8000",
    "http://0.0.0.0:8000",
    "http://10.7.5.148",
    "http://10.7.5.131",
    "http://192.168.1.21",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(robot_router)

if __name__ == "__main__":
    init_db()
    import uvicorn
    uvicorn.run("main:app", reload=True, port=8000, host="0.0.0.0")