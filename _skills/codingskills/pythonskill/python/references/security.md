# Python Security Reference

## The Golden Rules

1. Never trust user input — validate and sanitise everything
2. Never store secrets in code or VCS — use environment variables
3. Never store plain-text passwords — always hash with bcrypt or argon2
4. Never interpolate user input into SQL, shell commands, or eval
5. Fail securely — on error, deny access rather than allow it

---

## Password Hashing

```python
# bcrypt — industry standard, slow by design
import bcrypt

def hash_password(plain: str) -> bytes:
    return bcrypt.hashpw(plain.encode(), bcrypt.gensalt(rounds=12))

def verify_password(plain: str, hashed: bytes) -> bool:
    return bcrypt.checkpw(plain.encode(), hashed)

# Usage
stored_hash = hash_password("user_password")
is_valid = verify_password("user_password", stored_hash)  # True

# argon2 — newer, preferred for new projects
from argon2 import PasswordHasher
ph = PasswordHasher()

hashed = ph.hash("user_password")
try:
    ph.verify(hashed, "user_password")  # raises if wrong
except argon2.exceptions.VerifyMismatchError:
    raise AuthError("Invalid credentials")
```

**Never use**: `md5`, `sha1`, `sha256` alone for passwords — they're too fast.
**Never use**: `hashlib.md5(password)` — no salt, trivially brute-forced.

---

## Secrets and Tokens

```python
import secrets

# Cryptographically secure random — use this, not random
token = secrets.token_urlsafe(32)          # URL-safe base64, 32 bytes entropy
hex_token = secrets.token_hex(32)          # hex string
bytes_token = secrets.token_bytes(32)      # raw bytes

# Constant-time comparison (prevents timing attacks)
if secrets.compare_digest(user_token, stored_token):
    grant_access()

# WRONG — vulnerable to timing attacks
if user_token == stored_token:  # short-circuits!
    grant_access()
```

---

## Secrets Management

```python
# Load from environment — never hardcode
import os
from dotenv import load_dotenv

load_dotenv()  # reads .env for local dev only

DB_URL = os.environ["DATABASE_URL"]       # KeyError if missing — good!
SECRET_KEY = os.environ["SECRET_KEY"]
API_KEY = os.getenv("API_KEY", "")        # optional with default

# Use pydantic-settings for structured config
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str       # required — raises if absent
    secret_key: str         # required
    debug: bool = False

    class Config:
        env_file = ".env"

settings = Settings()
```

`.gitignore` must include `.env`. Commit only `.env.example` with placeholder values.

---

## SQL Injection Prevention

```python
# VULNERABLE — never do this
name = request.form["name"]
cursor.execute(f"SELECT * FROM users WHERE name = '{name}'")
# Attacker input: "'; DROP TABLE users; --"

# SAFE — parameterised queries always
cursor.execute("SELECT * FROM users WHERE name = %s", (name,))
cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))  # sqlite3

# SQLAlchemy ORM — safe by default
user = session.query(User).filter_by(name=name).first()

# SQLAlchemy core with text() — still parameterise
from sqlalchemy import text
result = conn.execute(
    text("SELECT * FROM users WHERE name = :name"),
    {"name": name}
)
```

---

## Command Injection Prevention

```python
import subprocess
from pathlib import Path

# VULNERABLE
user_dir = request.args["dir"]
os.system(f"ls {user_dir}")              # shell injection
subprocess.run(f"ls {user_dir}", shell=True)   # same problem

# SAFE — pass as list, never shell=True with user input
result = subprocess.run(
    ["ls", "-la", user_dir],
    capture_output=True,
    text=True,
    check=True,          # raises CalledProcessError on non-zero exit
    timeout=30,          # always set a timeout
)

# Validate paths before using them
def safe_path(base: Path, user_input: str) -> Path:
    """Resolve path and ensure it's within the base directory."""
    resolved = (base / user_input).resolve()
    if not str(resolved).startswith(str(base.resolve())):
        raise PermissionError(f"Path traversal attempt: {user_input!r}")
    return resolved
```

---

## Input Validation

```python
from pydantic import BaseModel, Field, field_validator
import re

class UserInput(BaseModel):
    username: str = Field(min_length=3, max_length=50, pattern=r"^[a-zA-Z0-9_]+$")
    email: str = Field(pattern=r"^[^@]+@[^@]+\.[^@]+$")
    age: int = Field(ge=0, le=150)
    score: float = Field(ge=0.0, le=100.0)

    @field_validator("username")
    @classmethod
    def no_reserved_words(cls, v: str) -> str:
        reserved = {"admin", "root", "system"}
        if v.lower() in reserved:
            raise ValueError(f"Username {v!r} is reserved")
        return v

# Use it
try:
    data = UserInput(**request_data)
except ValidationError as exc:
    return {"error": exc.errors()}, 422
```

---

## HTTP Security Headers (Flask example)

```python
from flask import Flask

app = Flask(__name__)

@app.after_request
def add_security_headers(response):
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    response.headers["Referrer-Policy"] = "no-referrer"
    return response
```

---

## JWT Handling

```python
import jwt
from datetime import datetime, timezone, timedelta

SECRET = os.environ["JWT_SECRET"]
ALGORITHM = "HS256"

def create_token(user_id: int, expires_in: int = 3600) -> str:
    payload = {
        "sub": str(user_id),
        "iat": datetime.now(timezone.utc),
        "exp": datetime.now(timezone.utc) + timedelta(seconds=expires_in),
    }
    return jwt.encode(payload, SECRET, algorithm=ALGORITHM)

def verify_token(token: str) -> dict:
    try:
        return jwt.decode(token, SECRET, algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise AuthError("Token has expired")
    except jwt.InvalidTokenError as exc:
        raise AuthError(f"Invalid token: {exc}")
```

**Never**: store sensitive data in the JWT payload — it's base64-encoded, not encrypted.
**Always**: verify the `exp` claim (PyJWT does this automatically).
**Always**: use a strong secret (≥ 256 bits).

---

## File Upload Security

```python
import magic  # python-magic: validates actual file type, not just extension
from pathlib import Path
import hashlib

ALLOWED_TYPES = {"image/jpeg", "image/png", "image/gif", "application/pdf"}
MAX_SIZE = 10 * 1024 * 1024  # 10 MB

def validate_upload(file_bytes: bytes, filename: str) -> Path:
    # 1. Size check
    if len(file_bytes) > MAX_SIZE:
        raise ValueError(f"File too large: {len(file_bytes)} bytes")

    # 2. MIME type check (from actual content, not extension)
    mime = magic.from_buffer(file_bytes, mime=True)
    if mime not in ALLOWED_TYPES:
        raise ValueError(f"File type not allowed: {mime}")

    # 3. Generate safe filename (never trust the original)
    content_hash = hashlib.sha256(file_bytes).hexdigest()[:16]
    ext = {"image/jpeg": ".jpg", "image/png": ".png",
           "image/gif": ".gif", "application/pdf": ".pdf"}[mime]
    safe_name = f"{content_hash}{ext}"

    # 4. Store outside web root
    upload_path = Path("/var/uploads") / safe_name
    upload_path.write_bytes(file_bytes)
    return upload_path
```

---

## Rate Limiting

```python
# Flask-Limiter
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@app.route("/api/login", methods=["POST"])
@limiter.limit("5 per minute")  # strict on auth endpoints
def login():
    ...
```

---

## Secure Random vs Random

```python
# For security-sensitive purposes ONLY use:
import secrets
token = secrets.token_urlsafe(32)
otp = secrets.randbelow(1_000_000)  # 6-digit OTP

# random module is fine for non-security use:
import random
sample = random.sample(population, k=10)  # OK — not security-sensitive
```

---

## Logging Safely

```python
# NEVER log sensitive data
logger.info("User logged in: username=%s password=%s", username, password)  # WRONG
logger.info("Login attempt: token=%s", auth_token)  # WRONG

# Log identifiers only, not values
logger.info("User login: user_id=%s", user_id)  # OK
logger.info("Auth token used: token_prefix=%s", token[:8] + "...")  # OK (prefix only)

# Mask in Pydantic models
from pydantic import SecretStr

class Config(BaseModel):
    api_key: SecretStr  # .get_secret_value() to access; repr shows "**"
```

---

## Security Checklist Before Release

- [ ] No hardcoded secrets anywhere in the codebase (`git grep -i "password\|secret\|api_key"`)
- [ ] `.env` is in `.gitignore`
- [ ] All user input validated before use
- [ ] No `eval()`, `exec()`, or `pickle.loads()` on untrusted data
- [ ] No `shell=True` with user-controlled input
- [ ] Parameterised queries everywhere (no f-string SQL)
- [ ] Passwords hashed with bcrypt/argon2 (not md5/sha1)
- [ ] JWT tokens verified (signature + expiry)
- [ ] Dependencies up to date (`pip audit` / `safety check`)
- [ ] HTTP security headers set
- [ ] Rate limiting on auth and write endpoints
- [ ] File uploads validated for type and size
