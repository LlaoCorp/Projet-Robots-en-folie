from fastapi import FastAPI
from api.router import router as robot_router
from database.init_db import init_db

app = FastAPI()
app.include_router(robot_router)

if __name__ == "__main__":
    init_db()
    import uvicorn
    uvicorn.run("main:app", reload=True, port=8000)