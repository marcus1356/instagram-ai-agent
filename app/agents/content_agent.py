"""
Content Agent — usa Claude para gerar a legenda ideal e os hashtags
para um post de cultura pop no Instagram.
"""

import anthropic

from app.core.config import settings


SYSTEM_PROMPT = """Você é um especialista em marketing digital e cultura pop.
Sua função é criar conteúdo viral para o Instagram focado em trending topics globais.

Regras:
- Escreva sempre em português brasileiro
- Tom: jovem, energético, atual e engajante
- A legenda deve ter entre 150-250 caracteres (sem contar hashtags)
- Use emojis estrategicamente (3-5 por legenda)
- Gere exatamente 15 hashtags relevantes (mix de populares e de nicho)
- Hashtags devem estar no final, separadas por espaço

Formato de resposta (JSON):
{
  "caption": "legenda aqui com emojis",
  "hashtags": "#hashtag1 #hashtag2 ... #hashtag15",
  "image_prompt": "prompt detalhado em inglês para gerar imagem com DALL-E"
}

O image_prompt deve ser:
- Em inglês
- Estilo vibrante, colorido e chamativo para Instagram
- Sem rosto de pessoas reais (evitar problemas de direitos)
- Relacionado ao tópico de forma criativa e visual"""


def generate_post_content(topic: str) -> dict:
    """
    Gera legenda, hashtags e prompt de imagem para um tópico.
    Retorna dict com: caption, hashtags, image_prompt
    """
    client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)

    user_message = f"""Crie um post viral para o Instagram sobre este trending topic de cultura pop:

Tópico: {topic}

Lembre-se: retorne APENAS o JSON, sem markdown, sem explicações."""

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_message}],
    )

    raw = message.content[0].text.strip()

    import json
    return json.loads(raw)
