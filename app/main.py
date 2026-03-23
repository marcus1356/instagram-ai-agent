from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from sqlalchemy import func, select

from app.api.posts import router as posts_router
from app.core.config import settings
from app.core.database import AsyncSessionLocal, create_tables
from app.models.post import Post, PostStatus

TEMPLATES_DIR = Path(__file__).parent.parent / "templates"
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    yield


app = FastAPI(
    title=settings.APP_NAME,
    description="Agente de IA que gera e monitora posts de cultura pop para o Instagram.",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(posts_router)


@app.get("/")
async def dashboard(request: Request):
    """Dashboard visual — lista todos os posts gerados."""
    async with AsyncSessionLocal() as db:
        result = await db.execute(select(Post).order_by(Post.created_at.desc()))
        posts = result.scalars().all()

        total = len(posts)
        ready = sum(1 for p in posts if p.status == PostStatus.READY)
        posted = sum(1 for p in posts if p.status == PostStatus.POSTED)

    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "posts": posts,
            "total": total,
            "ready": ready,
            "posted": posted,
        },
    )


@app.get("/health")
async def health():
    return {"status": "ok"}
