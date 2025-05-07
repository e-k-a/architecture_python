from fastapi import FastAPI
from routers import api_router
import uvicorn
from db import init_db

app = FastAPI()

@app.on_event("startup")
def startup_event():
    init_db()

app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="debug")