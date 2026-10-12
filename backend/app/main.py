from fastapi import FastAPI

app = FastAPI(
    title="RepoLens",
    description="A Hybrid RAG-powered Codebase Intelligence Engine",
    version="0.1.0"
)

@app.get("/")
def home():
    return {
        "message": "Welcome to RepoLens!",
        "status": "running"
    }

