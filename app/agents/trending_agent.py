"""
Trending Agent — busca os tópicos em alta globalmente usando pytrends.
Filtra por cultura pop: entretenimento, celebridades, filmes, música, séries.
"""

import random

from pytrends.request import TrendReq


POP_CULTURE_CATEGORIES = [
    "entertainment",
    "celebrities",
    "movies",
    "music",
    "tv shows",
    "gaming",
    "viral",
]


def get_trending_topics(geo: str = "", count: int = 10) -> list[str]:
    """
    Retorna os trending topics globais do Google Trends.
    geo="" = mundial | geo="BR" = Brasil
    """
    try:
        pytrends = TrendReq(hl="en-US", tz=360)
        trending_df = pytrends.trending_searches(pn="united_states")
        topics = trending_df[0].tolist()
        return topics[:count]
    except Exception as e:
        print(f"[TrendingAgent] Erro ao buscar trends: {e}")
        return _fallback_topics()


def pick_best_topic(topics: list[str]) -> str:
    """
    Escolhe o tópico mais relevante para cultura pop.
    Por enquanto escolhe aleatoriamente — pode evoluir para scoring com Claude.
    """
    if not topics:
        return random.choice(_fallback_topics())
    return topics[0]


def _fallback_topics() -> list[str]:
    """Tópicos de fallback caso a API falhe."""
    return [
        "Taylor Swift new album",
        "Oscar 2025 nominees",
        "Marvel new movie",
        "Netflix trending series",
        "viral music video",
    ]