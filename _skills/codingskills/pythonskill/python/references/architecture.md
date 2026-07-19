# Python Architecture Patterns Reference

## Project Layout

### Standard Python Package (src layout — recommended)

```
myproject/
├── src/
│   └── myproject/
│       ├── __init__.py
│       ├── py.typed              # PEP 561 — marks package as typed
│       ├── config.py             # Settings class (pydantic-settings)
│       ├── exceptions.py         # Custom exception hierarchy
│       ├── models/               # Data models, ORM entities
│       │   └── __init__.py
│       ├── schemas/              # Request/response validation (Pydantic)
│       ├── services/             # Business logic — NO framework deps here
│       ├── repositories/         # Data access layer
│       ├── api/                  # HTTP layer (Flask/FastAPI)
│       │   ├── __init__.py
│       │   └── routes.py
│       └── utils/                # Pure helpers
├── tests/
│   ├── conftest.py
│   ├── unit/
│   └── integration/
├── pyproject.toml
├── .env.example
└── Dockerfile
```

The `src/` layout prevents accidental imports of the local package instead of the installed one.

---

## Configuration (12-Factor)

Store config in environment variables. Never hardcode. Use pydantic-settings:

```python
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    # Required — will raise ValidationError if missing
    database_url: str
    secret_key: str

    # Optional with defaults
    debug: bool = False
    port: int = Field(default=8000, ge=1, le=65535)
    log_level: str = "INFO"
    allowed_hosts: list[str] = ["localhost"]

# Singleton — import this everywhere
settings = Settings()
```

`.env.example` (committed to VCS — shows required keys, no actual values):
```
DATABASE_URL=postgresql://user:pass@localhost/mydb
SECRET_KEY=your-secret-here
DEBUG=false
PORT=8000
```

---

## Application Factory Pattern (Flask)

```python
# src/myproject/app.py
from flask import Flask
from .api.routes import api_bp
from .config import settings

def create_app() -> Flask:
    """Factory function — enables multiple instances for testing."""
    app = Flask(__name__)
    app.config["SECRET_KEY"] = settings.secret_key
    app.config["DEBUG"] = settings.debug

    # Register blueprints
    app.register_blueprint(api_bp, url_prefix="/api/v1")

    # Register error handlers
    register_error_handlers(app)

    return app

def register_error_handlers(app: Flask) -> None:
    @app.errorhandler(404)
    def not_found(e):
        return {"error": "Not found"}, 404

    @app.errorhandler(422)
    def validation_error(e):
        return {"error": str(e)}, 422
```

---

## Service Layer (Business Logic)

Keep business logic in `services/` — no HTTP imports, no ORM imports ideally.
This makes it easily testable and framework-independent.

```python
# src/myproject/services/analysis.py
from __future__ import annotations
from dataclasses import dataclass
from ..models import Record
from ..repositories import RecordRepository

@dataclass
class AnalysisResult:
    record_id: int
    score: float
    flags: list[str]
    passed: bool

class AnalysisService:
    def __init__(self, repository: RecordRepository) -> None:
        self._repo = repository  # injected dependency

    def analyse(self, record_id: int) -> AnalysisResult:
        record = self._repo.get_by_id(record_id)
        if record is None:
            raise ValueError(f"Record {record_id} not found")

        score = self._compute_score(record)
        flags = self._detect_flags(record)

        return AnalysisResult(
            record_id=record_id,
            score=score,
            flags=flags,
            passed=score >= 0.8 and not flags,
        )

    def _compute_score(self, record: Record) -> float:
        # Pure computation — easy to test
        ...
```

---

## Repository Pattern (Data Access)

Abstract the database behind a simple interface. Makes testing trivial.

```python
# src/myproject/repositories/base.py
from typing import Protocol, TypeVar
from ..models import Record

T = TypeVar("T")

class RecordRepository(Protocol):
    def get_by_id(self, id: int) -> Record | None: ...
    def list_all(self, limit: int = 100) -> list[Record]: ...
    def save(self, record: Record) -> Record: ...
    def delete(self, id: int) -> bool: ...

# src/myproject/repositories/sql.py — real impl
class SQLRecordRepository:
    def __init__(self, db_session) -> None:
        self._session = db_session

    def get_by_id(self, id: int) -> Record | None:
        return self._session.get(Record, id)

# tests/conftest.py — test impl (no DB needed)
class InMemoryRecordRepository:
    def __init__(self) -> None:
        self._store: dict[int, Record] = {}

    def get_by_id(self, id: int) -> Record | None:
        return self._store.get(id)

    def save(self, record: Record) -> Record:
        self._store[record.id] = record
        return record
```

---

## API Design (REST)

```python
# Consistent response shape
def success_response(data, status: int = 200):
    return {"data": data, "error": None}, status

def error_response(message: str, status: int = 400):
    return {"data": None, "error": message}, status

# URI conventions
GET    /api/v1/records          # list
POST   /api/v1/records          # create
GET    /api/v1/records/{id}     # retrieve
PUT    /api/v1/records/{id}     # full replace
PATCH  /api/v1/records/{id}     # partial update
DELETE /api/v1/records/{id}     # delete

# Always version your API: /api/v1/
# Use plural nouns for collections
# Return full representation after create/update
# Include pagination: {"data": [...], "page": 1, "total": 500, "next": "/api/v1/records?page=2"}
```

---

## Validation with Pydantic

```python
from pydantic import BaseModel, Field, field_validator, model_validator
from typing import Annotated

PositiveFloat = Annotated[float, Field(gt=0)]

class CreateRecordRequest(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    value: PositiveFloat
    category: str
    tags: list[str] = []

    @field_validator("category")
    @classmethod
    def validate_category(cls, v: str) -> str:
        allowed = {"A", "B", "C"}
        if v not in allowed:
            raise ValueError(f"category must be one of {allowed}")
        return v

    @model_validator(mode="after")
    def check_consistency(self) -> "CreateRecordRequest":
        if self.category == "A" and self.value > 100:
            raise ValueError("Category A cannot have value > 100")
        return self
```

---

## Dependency Injection

Avoid global state. Pass dependencies explicitly.

```python
# Bad — hidden global dependency
def analyse(record_id: int) -> dict:
    db = get_db()  # hidden
    ...

# Good — explicit injection
def analyse(record_id: int, *, service: AnalysisService) -> dict:
    ...

# Or use a container (for larger apps)
from typing import Annotated
from fastapi import Depends

def get_analysis_service(db=Depends(get_db)) -> AnalysisService:
    return AnalysisService(SQLRecordRepository(db))

@router.get("/records/{id}/analyse")
def analyse_record(id: int, service: Annotated[AnalysisService, Depends(get_analysis_service)]):
    return service.analyse(id)
```

---

## Async Python

Use `asyncio` when your bottleneck is I/O (network, file, database). Not for CPU-bound work.

```python
import asyncio
import httpx

async def fetch_all(urls: list[str]) -> list[dict]:
    async with httpx.AsyncClient() as client:
        tasks = [client.get(url) for url in urls]
        responses = await asyncio.gather(*tasks, return_exceptions=True)

    results = []
    for url, resp in zip(urls, responses):
        if isinstance(resp, Exception):
            logger.error("Failed to fetch %s: %s", url, resp)
        else:
            results.append(resp.json())
    return results

# Run from sync context
data = asyncio.run(fetch_all(urls))
```

CPU-bound parallelism → `multiprocessing` or `concurrent.futures.ProcessPoolExecutor`.

---

## Twelve-Factor Checklist

Apply these principles to any app that will be deployed:

1. **One codebase** in VCS — multiple environments, same code
2. **Explicit dependencies** — `pyproject.toml` / `requirements.txt`; no `--user` installs
3. **Config in environment** — never hardcode host/port/creds
4. **Backing services** — database, cache, queue: connect via URL from env
5. **Build/release/run separated** — Docker build → tag/push → container run
6. **Stateless processes** — no local file storage, no session in memory
7. **Port binding** — expose via `PORT` env var; don't hardcode
8. **Concurrency via processes** — scale by adding workers, not threads
9. **Disposability** — fast start (`< 5s`), graceful shutdown on SIGTERM
10. **Dev/prod parity** — same OS, same services in dev and prod (Docker helps)
11. **Logs as streams** — write to stdout; let the platform collect them
12. **Admin tasks** — run as one-off processes in the same environment

---

## Database Migrations (Alembic)

```bash
# Setup
alembic init alembic
# Edit alembic.ini: sqlalchemy.url = %(DATABASE_URL)s

# Create migration
alembic revision --autogenerate -m "add users table"
# Review generated file — always check autogenerate output!

# Apply
alembic upgrade head

# Rollback
alembic downgrade -1
```

Zero-downtime migration pattern:
1. Add column as nullable (deploy)
2. Backfill existing rows (run migration)
3. Make column not-null with default (deploy)
4. Never drop columns immediately — mark deprecated, wait one release

---

## Monolith vs Microservices

Start with a monolith. Extract services only when you have:
- Clear domain boundaries (verified by data)
- Different scaling requirements between components
- Multiple teams who need to deploy independently

Strangler Fig Pattern for extraction:
1. Add facade (API gateway or proxy) in front of monolith
2. Implement new service for one bounded context
3. Route traffic to new service; fall back to monolith on errors
4. Once stable, remove monolith path
5. Repeat for next bounded context
