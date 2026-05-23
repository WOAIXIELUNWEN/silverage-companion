from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.api.chat import router as chat_router
from app.api.health import router as health_router
from app.models.database import init_db

app = FastAPI(
    title="SilverAge Companion API",
    description="AI-powered elderly care companion platform",
    version="1.0.0",
)

# Init database on startup
@app.on_event("startup")
def on_startup():
    init_db()


# API routes
app.include_router(chat_router)
app.include_router(health_router)

# Static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.get("/")
def index():
    return FileResponse("app/static/index.html")


@app.get("/api/health")
def health_check():
    return {"status": "ok", "service": "SilverAge Companion"}
