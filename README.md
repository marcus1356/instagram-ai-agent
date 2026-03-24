# Instagram AI Agent

<p align="center">
  <strong>Agente de IA que gera e publica conteúdo de cultura pop para o Instagram usando Claude e DALL-E.</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/python-3.11+-blue?logo=python&logoColor=white" alt="Python 3.11+">
  <img src="https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi&logoColor=white" alt="FastAPI">
  <img src="https://img.shields.io/badge/Claude_API-Anthropic-6B4FBB?logo=anthropic&logoColor=white" alt="Claude">
  <img src="https://img.shields.io/badge/OpenAI-DALL--E-412991?logo=openai&logoColor=white" alt="OpenAI">
  <img src="https://img.shields.io/badge/license-MIT-green" alt="MIT">
</p>

---

## Visão Geral

Agente autônomo de marketing para Instagram. Monitora tendências do Google Trends, gera legendas envolventes com Claude, cria imagens com DALL-E e posta automaticamente em horário configurável.

### Principais Funcionalidades

- **Geração de conteúdo com IA** — Legendas criativas via Claude (Anthropic)
- **Imagens geradas por IA** — Criação visual automática com DALL-E (OpenAI)
- **Tendências em tempo real** — Monitora Google Trends BR via `pytrends`
- **Agendamento automático** — Posts diários em horário configurável
- **Dashboard web** — Interface para monitorar posts e histórico
- **Armazenamento local** — SQLite para histórico completo de publicações

---

## Stack

| Camada | Tecnologia |
|--------|-----------|
| Backend | FastAPI + Uvicorn |
| IA (texto) | Claude API (Anthropic) |
| IA (imagem) | DALL-E (OpenAI) |
| Tendências | pytrends (Google Trends) |
| Banco de dados | SQLite + aiosqlite (async) |
| Agendamento | APScheduler |
| Frontend | Jinja2 Templates |

---

## Início Rápido

### 1. Clonar e instalar

```bash
git clone https://github.com/marcus1356/instagram-ai-agent.git
cd instagram-ai-agent

python -m venv .venv
source .venv/bin/activate    # Linux/Mac
# .venv\Scripts\activate     # Windows

pip install -r requirements.txt
```

### 2. Configurar variáveis de ambiente

```bash
cp .env.example .env
```

Edite `.env`:

```env
ANTHROPIC_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-...

POST_HOUR=9
POST_MINUTE=0
```

### 3. Executar

```bash
python -m app.main
```

Acesse o dashboard em **http://localhost:8000**

---

## Arquitetura

```
instagram-ai-agent/
├── app/
│   ├── main.py            # App FastAPI e lifecycle
│   ├── agents/
│   │   ├── content_agent.py   # Geração de legenda com Claude
│   │   ├── image_agent.py     # Geração de imagem com DALL-E
│   │   └── trending_agent.py  # Coleta tendências Google Trends BR
│   ├── api/
│   │   └── posts.py           # Endpoints REST
│   ├── core/
│   │   ├── config.py          # Configurações via .env
│   │   └── database.py        # Conexão SQLite async
│   ├── models/
│   │   └── post.py            # Modelo de dados Post
│   └── schemas/               # Schemas Pydantic
├── templates/                 # Templates HTML do dashboard
├── requirements.txt
└── .env.example
```

### Fluxo

```
Scheduler (diário)
    ↓
trending_agent  →  Tendências Google Trends BR
    ↓
content_agent   →  Legenda gerada com Claude
    ↓
image_agent     →  Imagem gerada com DALL-E
    ↓
Database        →  Salva post no SQLite
    ↓
Instagram API   →  Publica o post
```

---

## API Endpoints

| Método | Rota | Descrição |
|:------:|------|-----------|
| `GET` | `/` | Dashboard web |
| `GET` | `/api/posts` | Lista posts com filtros |
| `POST` | `/api/posts/generate` | Gera novo post |

---

## Licença

MIT — use livremente para fins pessoais e comerciais.
