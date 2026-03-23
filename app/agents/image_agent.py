"""
Image Agent — usa DALL-E 3 (OpenAI) para gerar a imagem do post.
"""

from openai import OpenAI

from app.core.config import settings


def generate_image(prompt: str) -> str:
    """
    Gera uma imagem com DALL-E 3 a partir do prompt.
    Retorna a URL da imagem gerada.
    """
    client = OpenAI(api_key=settings.OPENAI_API_KEY)

    # Adiciona estilo padrão Instagram ao prompt
    styled_prompt = (
        f"{prompt}. "
        "Style: vibrant Instagram-ready photo, high quality, eye-catching colors, "
        "modern aesthetic, no text overlays, cinematic composition."
    )

    response = client.images.generate(
        model="dall-e-3",
        prompt=styled_prompt,
        size="1024x1024",   # formato quadrado — ideal para Instagram
        quality="standard",
        n=1,
    )

    return response.data[0].url
