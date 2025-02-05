from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# React 정적 파일을 FastAPI에 포함
app.mount("/static", StaticFiles(directory="frontend_build"), name="static")

@app.get("/")
def read_root():
    return {"message": "FastAPI + React EXE is running!"}
