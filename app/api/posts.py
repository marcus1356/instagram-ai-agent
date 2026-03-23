from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.agents.content_agent import generate_post_content
from app.agents.image_agent import generate_image
from app.agents.trending_agent import get_trending_topics, pick_best_topic
from app.core.database import get_db
from app.models.post import Post, PostStatus
from app.schemas.post import GenerateRequest, PostResponse

router = APIRouter(prefix="/posts", tags=["posts"])


@router.get("/", response_model=list[PostResponse])
async def list_posts(db: AsyncSession = Depends(get_db)):
    """Lista todos os posts gerados, do mais recente ao mais antigo."""
    result = await db.execute(select(Post).order_by(Post.created_at.desc()))
    return result.scalars().all()


@router.get("/{post_id}", response_model=PostResponse)
async def get_post(post_id: int, db: AsyncSession = Depends(get_db)):
    """Retorna um post específico."""
    post = await db.get(Post, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post não encontrado")
    return post


@router.post("/generate", response_model=PostResponse, status_code=201)
async def generate_post(
    request: GenerateRequest = GenerateRequest(),
    db: AsyncSession = Depends(get_db),
):
    """
    Aciona o agente completo:
    1. Busca trending topic (ou usa o override)
    2. Gera legenda + hashtags com Claude
    3. Gera imagem com DALL-E 3
    4. Salva no banco
    """
    # 1. Trending topic
    if request.topic_override:
        topic = request.topic_override
    else:
        topics = get_trending_topics()
        topic = pick_best_topic(topics)

    # 2. Conteúdo com Claude
    content = generate_post_content(topic)

    # 3. Imagem com DALL-E
    image_url = generate_image(content["image_prompt"])

    # 4. Salva no banco
    post = Post(
        trending_topic=topic,
        caption=content["caption"],
        image_url=image_url,
        image_prompt=content["image_prompt"],
        hashtags=content["hashtags"],
        status=PostStatus.READY,
    )
    db.add(post)
    await db.commit()
    await db.refresh(post)

    return post


@router.delete("/{post_id}", status_code=204)
async def delete_post(post_id: int, db: AsyncSession = Depends(get_db)):
    """Remove um post do banco."""
    post = await db.get(Post, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post não encontrado")
    await db.delete(post)
    await db.commit()