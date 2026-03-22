# FlashCards — Plán 1: Infrastruktura

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Funkční Docker Compose stack — Nginx + PostgreSQL + FastAPI skeleton + Authelia proxy. Na konci tohoto plánu běží `docker compose up` a `GET /api/health` vrátí 200.

**Architecture:** Nginx jako reverse proxy předává `/api/*` na FastAPI backend a obsluhuje statické soubory frontendu. Authelia stojí před Nginx a předává ověřené requesty s `Remote-User` hlavičkou. PostgreSQL běží jako samostatná služba s pojmenovaným volume.

**Tech Stack:** Docker Compose, Nginx, FastAPI (Python 3.12), PostgreSQL 16, Authelia 4.x, python-dotenv, SQLAlchemy 2.x (async), Alembic

---

## Struktura souborů

```
flashcards/
├── docker-compose.yml
├── .env.example
├── .gitignore
├── nginx/
│   ├── nginx.conf
│   └── Dockerfile
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── alembic.ini
│   ├── alembic/
│   │   ├── env.py
│   │   └── versions/
│   │       └── 0001_initial.py
│   └── app/
│       ├── main.py              # FastAPI app, middleware, health endpoint
│       ├── config.py            # Nastavení z .env
│       ├── database.py          # SQLAlchemy async engine + session
│       ├── auth.py              # Extrakce Remote-User hlavičky, upsert User
│       └── models/
│           └── user.py          # SQLAlchemy model User
├── authelia/
│   ├── configuration.yml        # Authelia config (bypass mode pro vývoj)
│   └── users_database.yml       # Testovací uživatelé
└── media/                       # Placeholder pro Docker volume mount
    └── .gitkeep
```

---

## Task 1: Základní kostra repozitáře

**Files:**
- Create: `.gitignore`
- Create: `.env.example`
- Create: `media/.gitkeep`

- [ ] **Step 1: Vytvoř `.gitignore`**

```gitignore
.env
__pycache__/
*.pyc
.venv/
node_modules/
dist/
media/*
!media/.gitkeep
.superpowers/
```

- [ ] **Step 2: Vytvoř `.env.example`**

```env
POSTGRES_DB=flashcards
POSTGRES_USER=flashcards
POSTGRES_PASSWORD=changeme
POSTGRES_HOST=db
POSTGRES_PORT=5432
LIBRETRANSLATE_URL=http://libretranslate:5000
MEDIA_MAX_SIZE_MB=5
SM2_LEARNED_THRESHOLD_DAYS=21
```

- [ ] **Step 3: Vytvoř `.env` zkopírováním**

```bash
cp .env.example .env
```

- [ ] **Step 4: Vytvoř `media/.gitkeep`**

```bash
mkdir -p media && touch media/.gitkeep
```

- [ ] **Step 5: Commit**

```bash
git init
git add .gitignore .env.example media/.gitkeep
git commit -m "chore: initial repo structure"
```

---

## Task 2: FastAPI backend skeleton

**Files:**
- Create: `backend/requirements.txt`
- Create: `backend/app/config.py`
- Create: `backend/app/main.py`

- [ ] **Step 1: Vytvoř `backend/requirements.txt`**

```
fastapi==0.115.0
uvicorn[standard]==0.30.0
sqlalchemy[asyncio]==2.0.36
asyncpg==0.30.0
alembic==1.13.3
python-dotenv==1.0.1
python-multipart==0.0.12
httpx==0.27.2
pytest==8.3.3
pytest-asyncio==0.24.0
httpx==0.27.2
```

- [ ] **Step 2: Vytvoř `backend/app/config.py`**

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    postgres_db: str
    postgres_user: str
    postgres_password: str
    postgres_host: str = "db"
    postgres_port: int = 5432
    libretranslate_url: str = "http://libretranslate:5000"
    media_max_size_mb: int = 5
    sm2_learned_threshold_days: int = 21

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

    class Config:
        env_file = ".env"

settings = Settings()
```

Přidej `pydantic-settings==2.5.2` do `requirements.txt`.

- [ ] **Step 3: Vytvoř `backend/app/main.py`**

```python
from fastapi import FastAPI

app = FastAPI(title="FlashCards API")

@app.get("/api/health")
async def health():
    return {"status": "ok"}
```

- [ ] **Step 4: Otestuj lokálně (volitelné — bez Dockeru)**

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
# curl http://localhost:8000/api/health → {"status":"ok"}
```

- [ ] **Step 5: Commit**

```bash
git add backend/
git commit -m "feat: fastapi skeleton with health endpoint"
```

---

## Task 3: PostgreSQL + SQLAlchemy + Alembic

**Files:**
- Create: `backend/app/database.py`
- Create: `backend/app/models/user.py`
- Create: `backend/alembic.ini`
- Create: `backend/alembic/env.py`
- Create: `backend/alembic/versions/0001_initial.py`

- [ ] **Step 1: Vytvoř `backend/app/database.py`**

```python
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from app.config import settings

engine = create_async_engine(settings.database_url, echo=False)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)

class Base(DeclarativeBase):
    pass

async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session
```

- [ ] **Step 2: Vytvoř `backend/app/models/__init__.py`** (prázdný)

- [ ] **Step 3: Vytvoř `backend/app/models/user.py`**

```python
import uuid
from datetime import datetime
from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    username: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
```

- [ ] **Step 4: Inicializuj Alembic**

```bash
cd backend
alembic init alembic
```

- [ ] **Step 5: Uprav `backend/alembic/env.py`** — přidej import modelů a async podporu

```python
import asyncio
from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import async_engine_from_config
from alembic import context

# Importuj Base a všechny modely
from app.database import Base
from app.models import user  # noqa: F401
from app.config import settings

config = context.config
config.set_main_option("sqlalchemy.url", settings.database_url)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()

def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()

async def run_async_migrations() -> None:
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)
    await connectable.dispose()

def run_migrations_online() -> None:
    asyncio.run(run_async_migrations())

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
```

- [ ] **Step 6: Vytvoř první migraci**

```bash
cd backend
alembic revision --autogenerate -m "initial"
# Zkontroluj vygenerovaný soubor v alembic/versions/
```

- [ ] **Step 7: Commit**

```bash
git add backend/app/database.py backend/app/models/ backend/alembic/
git commit -m "feat: sqlalchemy models and alembic migration for User"
```

---

## Task 4: Authelia middleware + User upsert

**Files:**
- Create: `backend/app/auth.py`
- Modify: `backend/app/main.py`

- [ ] **Step 1: Napiš failing test**

Vytvoř `backend/tests/test_auth.py`:

```python
import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.mark.asyncio
async def test_health_no_auth_required():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        resp = await ac.get("/api/health")
    assert resp.status_code == 200

@pytest.mark.asyncio
async def test_protected_endpoint_without_header_returns_401():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        resp = await ac.get("/api/me")
    assert resp.status_code == 401

@pytest.mark.asyncio
async def test_protected_endpoint_with_header_returns_user():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        resp = await ac.get("/api/me", headers={"Remote-User": "testuser"})
    assert resp.status_code == 200
    assert resp.json()["username"] == "testuser"
```

- [ ] **Step 2: Spusť test — ověř že failuje**

```bash
cd backend
pytest tests/test_auth.py -v
# Expected: FAIL — /api/me neexistuje
```

- [ ] **Step 3: Vytvoř `backend/app/auth.py`**

```python
from fastapi import Header, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models.user import User

async def get_current_user(
    remote_user: str | None = Header(default=None, alias="Remote-User"),
    remote_email: str | None = Header(default=None, alias="Remote-Email"),
    db: AsyncSession = Depends(get_db),
) -> User:
    if not remote_user:
        raise HTTPException(status_code=401, detail="Unauthorized")

    result = await db.execute(select(User).where(User.username == remote_user))
    user = result.scalar_one_or_none()

    if user is None:
        user = User(username=remote_user, email=remote_email)
        db.add(user)
        await db.commit()
        await db.refresh(user)

    return user
```

- [ ] **Step 4: Přidej `/api/me` endpoint do `backend/app/main.py`**

```python
from fastapi import FastAPI, Depends
from app.auth import get_current_user
from app.models.user import User

app = FastAPI(title="FlashCards API")

@app.get("/api/health")
async def health():
    return {"status": "ok"}

@app.get("/api/me")
async def me(user: User = Depends(get_current_user)):
    return {"username": user.username, "email": user.email}
```

- [ ] **Step 5: Spusť testy — ověř že pasují**

```bash
pytest tests/test_auth.py -v
# Expected: PASS (3/3)
```

- [ ] **Step 6: Commit**

```bash
git add backend/app/auth.py backend/app/main.py backend/tests/
git commit -m "feat: authelia header auth and user upsert"
```

---

## Task 5: Docker Compose

**Files:**
- Create: `docker-compose.yml`
- Create: `backend/Dockerfile`
- Create: `nginx/Dockerfile`
- Create: `nginx/nginx.conf`

- [ ] **Step 1: Vytvoř `backend/Dockerfile`**

```dockerfile
FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

- [ ] **Step 2: Vytvoř `nginx/nginx.conf`**

```nginx
server {
    listen 80;

    location /api/ {
        proxy_pass http://backend:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header Remote-User $http_remote_user;
        proxy_set_header Remote-Email $http_remote_email;
    }

    location /media/ {
        alias /media/;
    }

    location / {
        root /usr/share/nginx/html;
        try_files $uri $uri/ /index.html;
    }
}
```

- [ ] **Step 3: Vytvoř `nginx/Dockerfile`**

```dockerfile
FROM nginx:alpine
COPY nginx.conf /etc/nginx/conf.d/default.conf
```

- [ ] **Step 4: Vytvoř `docker-compose.yml`**

```yaml
services:
  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: ${POSTGRES_DB}
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER}"]
      interval: 5s
      retries: 5

  backend:
    build: ./backend
    env_file: .env
    depends_on:
      db:
        condition: service_healthy
    volumes:
      - media_data:/media

  nginx:
    build: ./nginx
    ports:
      - "80:80"
    depends_on:
      - backend
    volumes:
      - media_data:/media

volumes:
  postgres_data:
  media_data:
```

*Poznámka: Authelia se přidá jako samostatný krok po ověření základního stacku. Pro lokální vývoj postačí přímý přístup přes Nginx s manuálním přidáváním `Remote-User` hlavičky.*

- [ ] **Step 5: Spusť stack**

```bash
docker compose up --build
```

- [ ] **Step 6: Spusť migrace**

```bash
docker compose exec backend alembic upgrade head
```

- [ ] **Step 7: Ověř health endpoint**

```bash
curl http://localhost/api/health
# Expected: {"status":"ok"}

curl http://localhost/api/me -H "Remote-User: testuser"
# Expected: {"username":"testuser","email":null}
```

- [ ] **Step 8: Commit**

```bash
git add docker-compose.yml backend/Dockerfile nginx/
git commit -m "feat: docker compose stack with nginx, backend, postgres"
```

---

## Task 6: Authelia integrace (volitelné pro produkci)

**Files:**
- Create: `authelia/configuration.yml`
- Create: `authelia/users_database.yml`
- Modify: `docker-compose.yml`

- [ ] **Step 1: Vytvoř `authelia/users_database.yml`** s testovacím uživatelem

```yaml
users:
  testuser:
    displayname: "Test User"
    password: "$argon2id$v=19$m=65536,t=3,p=4$..." # vygeneruj: authelia hash-password
    email: test@example.com
    groups: []
```

- [ ] **Step 2: Vytvoř `authelia/configuration.yml`** — minimální konfigurace pro vývoj

```yaml
theme: dark
jwt_secret: a_very_secret_jwt_key_change_in_prod
default_redirection_url: http://localhost/

server:
  host: 0.0.0.0
  port: 9091

log:
  level: debug

authentication_backend:
  file:
    path: /config/users_database.yml

access_control:
  default_policy: one_factor

session:
  secret: a_very_secret_session_key

storage:
  local:
    path: /config/db.sqlite3

notifier:
  filesystem:
    filename: /config/notification.txt
```

- [ ] **Step 3: Přidej Authelia do `docker-compose.yml`**

```yaml
  authelia:
    image: authelia/authelia:latest
    volumes:
      - ./authelia:/config
    ports:
      - "9091:9091"
    depends_on:
      - nginx
```

- [ ] **Step 4: Ověř přihlášení přes Authelia**

```bash
docker compose up --build
# Otevři http://localhost:9091 — přihlas se jako testuser
# Authelia přesměruje na http://localhost/ s Remote-User hlavičkou
```

- [ ] **Step 5: Commit**

```bash
git add authelia/ docker-compose.yml
git commit -m "feat: authelia sso proxy for local dev"
```

---

## Hotovo

Na konci tohoto plánu:
- ✅ `docker compose up` spustí celý stack
- ✅ `GET /api/health` → 200
- ✅ `GET /api/me` s `Remote-User` hlavičkou → vrátí uživatele (upsert)
- ✅ Alembic migrace fungují
- ✅ PostgreSQL data persistují přes restarty
- ✅ Media volume připraven

**Pokračuj plánem 2: Backend core** (`2026-03-22-02-backend-core.md`)
