# Python Architecture Knowledge Base

*Source: "Python Architecture Patterns" by Jaime Buelta (Packt, 2022)*
*Extracted and curated for OpenClaw projects - 2026-03-07*

---

## Table of Contents

1. [Introduction to Software Architecture](#introduction)
2. [API Design](#api-design)
3. [Data Modeling](#data-modeling)
4. [The Data Layer](#data-layer)
5. [Twelve-Factor App Methodology](#twelve-factor)
6. [Web Server Structures](#web-server)
7. [Event-Driven Structures](#event-driven)
8. [Microservices vs Monolith](#microservices)
9. [Testing and TDD](#testing)
10. [Package Management](#packaging)
11. [Logging](#logging)
12. [Metrics](#metrics)
13. [Profiling](#profiling)
14. [Debugging](#debugging)
15. [Ongoing Architecture](#ongoing)
16. [Applied to 5-Gas Analyzer](#applied-5gas)

---

## Introduction <a name="introduction"></a>

### Core Principles

**Software Architecture** defines the structure of a software system. It focuses on **long-term implications** rather than short-term wins.

**Key Considerations:**
- Business vision & stakeholder requirements
- Technical requirements (scalability, performance)
- Security and reliability concerns
- Division of tasks for team coordination
- Technology stack constraints

**Conway's Law**: The structure of the software mirrors the communication structure of the organization. Team boundaries define system boundaries.

**Single-Responsibility Principle**: Each element should have a clear function and interface.

### Example Architecture: LAMP Stack

**LAMP** = Linux + Apache + MySQL + PHP

Components:
- **Database**: Reliable, stores all data, backup/recovery critical
- **Web Worker**: Scalable, stateless, updated frequently
- **Web Server**: Handles HTTP, static files, load balancing

**Communication**: Each component uses different protocols (SQL, FastCGI, HTTP)

### Security by Design

**Password Storage Best Practice:**
- Never store plain text passwords
- Store **cryptographic hash** + **salt**
- Use algorithms like bcrypt with multiple rounds
- Only compare hash during login; actual password is unknown to system

---

## API Design <a name="api-design"></a>

### Abstractions

An API presents **simplified actions** without exposing implementation complexity.

**Good API Design:**
- Clear menu of actions
- Deterministic (same input → same output for functional APIs)
- Stateful vs stateless operations clearly defined
- Opaque implementation details

**Leaky Abstractions**: All non-trivial abstractions leak some details. Design for:
- Clear external error messages
- Graceful degradation
- Proper error handling for dependent service failures

### RESTful Interfaces

**REST Constraints** (Fielding):
1. Client-server architecture
2. Stateless requests
3. Cacheable responses
4. Layered system
5. Uniform interface:
   - Resource identification
   - Resource manipulation via representations
   - Self-descriptive messages
   - HATEOAS (Hypermedia as Engine of Application State)

**Practical RESTful (JSON over HTTP):**

**Resources** (passive) vs **Actions** (operations on resources)

**CRUD Operations:**

| Resource Type | GET | POST | PUT | PATCH | DELETE |
|---------------|-----|------|-----|-------|--------|
| Collection | List all | Create | N/A | N/A | N/A |
| Single item | Retrieve | N/A | Replace fully | Partial update | Delete |

**URI Design:**
```
/books                    # Collection
/books/1                  # Single resource
/books/1/cover            # Sub-resource
/books/search?q=python   # Search with query params
```

**Best Practices:**
- Use **plural nouns** for collections
- Use **UUIDs** or natural keys (not sequential integers) for IDs
- Return **full URIs** in responses (Location header, embedded links)
- 404 for missing resources, 405 for wrong method
- Pagination: `?page=1&size=10` with `next`/`previous` links

### Authentication

**HTML Interfaces:** Cookie-based session with:
- `Secure` (HTTPS only)
- `HttpOnly` (not accessible by JavaScript)
- `SameSite` (CSRF protection)

**RESTful APIs:** OAuth 2.0
- **Authorization Code Grant**: User-facing apps (3-legged)
- **Client Credentials Grant**: Server-to-server (2-legged)
- Use **JWT tokens** for self-contained signed tokens
- Bearer token: `Authorization: Bearer <token>`

### Versioning

**Semantic Versioning (X.Y.Z):**
- Major (X): backward-incompatible changes
- Minor (Y): new features, backward-compatible
- Patch (Z): bug fixes, no interface change

**Simplified Versioning** (for cloud services):
- Constantly increasing counter
- `v1.2.37` → next is `v1.2.38`
- Increase minor when patch reaches threshold (e.g., 100)

**When to use which?**
- Semantic: Stable APIs, libraries supporting multiple versions
- Simple: Single deployed version, internal usage reference only

### Frontend vs Backend

| Aspect | Frontend | Backend |
|--------|----------|---------|
| Focus | User experience, responsiveness | Stability, reliability |
| Execution | User's device | Controlled servers |
| Load | Distributed | Centralized |
| Changes | Frequent, visible | Less frequent, roll out globally |
| Tech | HTML/CSS/JS, React, design | Python/Java/C#, SQL/NoSQL, Nginx, Docker |

**Full Stack**: Requires different mindsets; most engineers lean one direction.

### OpenAPI (Swagger)

Define APIs in YAML/JSON → Auto-generate documentation & client/server stubs.

**Benefits:**
- Single source of truth
- Interactive docs (try it out)
- Code generation for multiple languages
- Refinement through design-first approach

---

## Data Modeling <a name="data-modeling"></a>

### Database Types

**1. Relational (SQL)**
- MySQL, PostgreSQL, Oracle, SQL Server
- Fixed schema, tables with rows/columns
- Primary key (unique identifier) + Foreign keys (relationships)
- ACID transactions
- **Best for**: Structured data, complex queries, strong consistency

**2. Non-Relational (NoSQL)**

| Type | Examples | Structure | Query |
|------|----------|-----------|-------|
| Key-Value | Redis, Riak | `<key, opaque-value>` | Get/Put by key only |
| Document | MongoDB, Elasticsearch | JSON-like documents in collections | Rich field queries |
| Wide-Column | Cassandra, Bigtable | Sparse rows, column families | Query by row key + prefix |
| Graph | Neo4j, ArangoDB | Nodes & edges with properties | Traversal queries |

**3. Small/Embedded**
- **SQLite**: Full SQL, single file, zero-config
- Use for: Single-process apps, local storage, prototyping

### ACID Transactions

- **Atomicity**: All-or-nothing; rolls back on error
- **Consistency**: All constraints respected (foreign keys, triggers)
- **Isolation**: Parallel transactions appear sequential
- **Durability**: Committed data survives crashes

**Cost**: Performance + scalability trade-off. Distributed ACID is extremely difficult.

### Distributed Relational Databases

#### Primary/Replica (Read Scaling)

**Pattern**: 1 primary (writes) + N replicas (reads)

```
Writes → Primary → Replicas (async)
Reads  → Any replica (or primary)
```

**Replication Lag**: Time delay between primary write and replica update.
- Typically < 1 second
- Avoid write-then-read immediately on replica; use primary or cache
- Promotion on primary failure (HA)

**Tools**: Pgpool (PostgreSQL), ProxySQL (MySQL) for transparent routing.

**Don't skip backups** even with replicas!

#### Sharding (Write Scaling)

**Horizontal partitioning** across multiple servers using **shard key**.

**Pure Sharding (hash-based):**
```python
shard_id = hash(shard_key) % num_shards
```
- All queries must include shard key
- Data evenly distributed
- Cross-shard queries impossible (or very expensive)

**Mixed Sharding:**
- Use translation table: `<input> → shard_key`
- More flexible, but translation lookup adds overhead
- Can rebalance shards dynamically by updating mapping

**Table Sharding** (for specific large tables):
- Entire tables on different servers
- No joins across shards
- Only for small clusters with unrelated large tables

**When to Shard?**
- Write throughput exceeds single server
- Data size exceeds single server capacity
- Shard key naturally partitions workload

**Challenges:**
- No cross-shard transactions (eventual consistency)
- Joins impossible across shards
- Application logic must handle routing
- Rebalancing is complex and slow

### Schema Design

**Steps:**
1. Draw tables, fields, relationships (ER diagram)
2. Define primary keys (natural vs surrogate)
3. Add foreign keys for relationships
4. Choose data types appropriately

**Relationship Types:**

| Type | Example | Implementation |
|------|---------|----------------|
| One-to-Many | Author → Books | FK in "many" side |
| One-to-One | Book ↔ ISBN | Unique FK either way |
| Many-to-Many | Books ↔ Genres | Junction table with FKs |

**Field Design Tips:**
- Strings: account for future growth, be generous with VARCHAR length
- Numbers: use `INTEGER` (no need for `SMALLINT`/`TINYINT`; space savings negligible)
- booleans: use BOOLEAN or TINYINT(1)
- **UTC for all timestamps**; convert to user timezone on display
- **Store prices as integers** (cents) to avoid float errors
- **Use readable strings** instead of enums (e.g., "RED" vs 1)
- Avoid over-optimization; prioritize understandability

**Normalization (reduce redundancy):**

**1NF (First Normal Form):** Atomic values, no repeating groups

**2NF:** No partial dependencies (every non-key field fully depends on full PK)

**3NF:** No transitive dependencies (non-key → non-key)

**Denormalization:**
- Intentional redundancy for performance
- Trade storage/consistency for speed
- Common in document stores (embedding)
- Use when queries would require multiple joins

**Schema Changes:**
- Always plan migrations; never direct edit in production
- Backward compatibility: add columns nullable, don't drop old ones immediately
- Zero-downtime migrations:
  1. Add new column/table
  2. Backfill data
  3. Switch code over (gradual or feature flag)
  4. Remove old column after full migration

---

## The Data Layer <a name="data-layer"></a>

### Domain-Driven Design (DDD)

Separate **domain logic** from implementation details. Core entities represent business concepts, not database tables.

### ORM (Object-Relational Mapping)

**Benefits:**
- Database independence (swap MySQL → PostgreSQL)
- Automatic SQL generation
- Change tracking
- Relationship management
- Validation

**Choosing an ORM:**
- **SQLAlchemy** (Python): Most flexible, explicit, unit-of-work pattern
- Django ORM: Integrated, simpler, but less flexible
- Avoid writing raw SQL unless necessary

**Repository Pattern:**
- Isolate data access behind interfaces
- Makes testing easier (mock repository)
- Decouples domain from database specifics

**Unit of Work Pattern:**
- Track changes to objects
- Commit all changes as single transaction
- SQLAlchemy session = Unit of Work

### CQRS (Command Query Responsibility Segregation)

**Separate models for reads and writes:**
- Write side: transactional, normalized
- Read side: denormalized, optimized for queries

**Benefits:**
- Read side can be scaled independently
- Different storage engines possible (SQL for writes, Elasticsearch for reads)
- No lock contention

**Complexity cost**: Dual models to maintain, eventual consistency between them.

### Database Migrations

**Goal:** Version-controlled, repeatable, backward-compatible schema changes.

**SQLAlchemy + Alembic** (Python):
- autogenerate diffs from model changes
- manual refinement for complex changes
- `alembic revision --autogenerate` → edit → `alembic upgrade head`

**Always:**
- Test migrations on staging copy
- Have rollback plan
- Keep migrations reversible (or provide manual rollback steps)
- Run during maintenance window for critical changes

**Zero-Downtime Strategies:**
- Add new column (nullable) → deploy → backfill → make required
- Add new table → deploy → switch reads → migrate data → switch writes
- Never drop columns immediately; mark deprecated first

---

## Twelve-Factor App Methodology <a name="twelve-factor"></a>

**Best practices for modern web apps:**

1. **Codebase**: One repo, tracked in VCS, many deployments
2. **Dependencies**: Explicit, no system-wide deps; use `requirements.txt` / `package.json`
3. **Config**: Store in environment variables; config files committed
4. **Backing services**: Treat DB, cache, queue as attached resources (connect via URL)
5. **Build, release, run**: Strict separation; each release is immutable
6. **Processes**: Stateless; store data in backing services
7. **Port binding**: Export HTTP via port binding (not port number hardcoded)
8. **Concurrency**: Scale via process model (worker count), not threads
9. **Disposability**: Fast startup/shutdown; handle SIGTERM gracefully
10. **Dev-prod parity**: Keep environments similar (same tools, languages)
11. **Logs**: Treat as event streams; don't manage log files
12. **Admin processes**: Run one-off tasks in same environment as app

**Container-Friendly**: These factors map naturally to Docker/Kubernetes.

---

## Web Server Structures <a name="web-server"></a>

### WSGI (Web Server Gateway Interface)

Python standard for web apps:
- `application(environ, start_response) → iterable`
- Synchronous, request-response

**Deployment Options:**
- **uWSGI**: Full-featured, supports multiple protocols
- **Gunicorn**: Simple, pre-fork worker model
- **mod_wsgi**: Apache module

**Process Models:**
- **Pre-fork**: Master spawns workers upfront; accept connections distributes
- **Threaded**: Each worker handles multiple concurrent requests via threads
- **Async**: Single process, many concurrent (asyncio, gevent)

**Configuration:**
```
workers = 2-4 * CPU cores
timeout = 30-60s
max_requests = to recycle workers after N requests (memory leaks)
```

### Django MVT (Model View Template)

**Request flow:**
1. URL routing (`urls.py`) → View
2. View handles business logic, queries Model
3. Model → Database (via ORM)
4. View renders Template → HttpResponse

**Middleware**: Plugins that process request/response globally. Use for:
- Authentication
- Security headers
- Logging
- Session handling

**Django REST Framework (DRF)** for APIs:
- Serializers: Convert model ↔ JSON
- ViewSets: CRUD operations with minimal code
- Routers: Auto-generate URLs for viewsets
- Permissions: Authentication/authorization

---

## Event-Driven Structures <a name="event-driven"></a>

### Asynchronous Tasks

Offload long-running/background work from request/response cycle.

**Use Cases:**
- Email sending
- Image/video processing
- Webhooks
- Scheduled reports
- Data synchronization

**Pattern:**
```
HTTP Request → Queue (Redis/RabbitMQ) → Worker → Process
```

**Benefits:**
- Fast response (just enqueue)
- Retry logic
- Parallel processing
- Decoupling

**Celery** (Python standard):
- `@celery.task` decorated functions
- Brokers: Redis, RabbitMQ
- Workers: `celery -A proj worker --loglevel=info`
- Beat: Scheduler for periodic tasks
- Flower: Web monitoring UI

**Task Design:**
- **Idempotent**: Running twice same as once (safe for retries)
- **Small scope**: Single responsibility per task
- **All data in args**: No global state; pass everything explicitly

**Error Handling:**
- Retry with exponential backoff (`autoretry_for`, `countdown`)
- Dead letter queue for failed tasks
- Alerting on failure rate

---

## Microservices vs Monolith <a name="microservices"></a>

### Monolithic Architecture

**Definition:** Single codebase, single deployment unit, shared database.

**Pros:**
- Simple to develop, test, deploy
- ACID transactions easy
- Single tech stack
- Low operational overhead

**Cons:**
- Tight coupling
- Single point of failure
- Hard to scale specific components
- Tech lock-in

**When to use:** Small team (<10 dev), early-stage, simple domain.

### Microservices Architecture

**Definition:** Multiple independent services, each with own database, deployed separately.

**Pros:**
- Independent scaling
- Team autonomy (Conway's Law)
- Tech diversity (polyglot)
- Fault isolation

**Cons:**
- Network latency
- Distributed transactions (2PC, sagas)
- Complexity (deployment, monitoring, tracing)
- Data consistency challenges

**Migration from Monolith (4 Acts):**

1. **Analyze**: Identify bounded contexts (Domain-Driven Design)
2. **Design**: Plan service boundaries, APIs
3. **Plan**: Migration strategy (strangler fig, database split)
4. **Execute**: Incremental extraction (facade → proxy → new service)

**Strangler Fig Pattern:**
- Wrap monolith with API gateway
- Gradually extract services
- Route traffic to new service, fall back to monolith
- Eventually decommission monolith pieces

**Database per Service:**
- Each service owns its data
- No direct cross-service DB access
- Communicate via APIs or events
- Use CDC (Change Data Capture) or shared DB for legacy integration

---

## Logging <a name="logging"></a>

### Log Levels

- `CRITICAL` / `FATAL` / `ERROR`: Failures requiring immediate attention
- `WARNING`: Unexpected but recoverable
- `INFO`: Key operational events (startup, shutdown, major milestones)
- `DEBUG`: Detailed diagnostic info (disable in production)

**Python:**
```python
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info("User %s logged in", user_id)
logger.error("DB connection failed", exc_info=True)  # include traceback
```

### Best Practices

1. **Structured logging** (JSON):
```json
{"timestamp":"...","level":"INFO","message":"...","user_id":123,"trace_id":"abc"}
```
- Machine-parseable
- Centralized log aggregators (ELK, Splunk) parse easily

2. **Correlation IDs**:
- Generate unique `trace_id` at request entry
- Pass through all services (HTTP header, queue metadata)
- Enables distributed tracing

3. **Sensitive data**: Never log passwords, tokens, PII

4. **Log destinations**:
- Local files (rotate with logrotate) - for debugging
- Stdout (Docker/K8s) - collect by sidecar
- Central service (Sentry, Datadog, CloudWatch)

5. **Log rotation**: Size- or time-based rotation; keep N days

---

## Metrics <a name="metrics"></a>

### Metrics vs Logs

| Metrics | Logs |
|---------|------|
| Numeric values (counters, gauges, histograms) | Text events |
| Aggregated over time | Individual occurrences |
| Alerting, dashboards | Debugging, investigation |
| Low cardinality | High cardinality OK |

### Prometheus (Industry Standard)

**Exporter pattern**: `/metrics` endpoint returning text exposition format:
```
# HELP http_requests_total Total HTTP requests
# TYPE http_requests_total counter
http_requests_total{method="GET",endpoint="/api/users"} 1234
```

**Python**: `prometheus-client` library
```python
from prometheus_client import Counter, generate_latest
REQUESTS = Counter('http_requests_total', 'Total requests')
@app.route('/metrics')
def metrics():
    return generate_latest()
```

**Querying:**
```
rate(http_requests_total[5m])  # per-second rate over last 5m
histogram_quantile(0.95, http_request_duration_seconds_bucket)
```

**Alerting**: Use Alertmanager for threshold alerts → PagerDuty/Slack.

---

## Profiling <a name="profiling"></a>

### Types

- **CPU profiling**: Where time is spent
- **Memory profiling**: Allocation, leaks
- **I/O profiling**: Blocking calls, network waits

### Tools (Python)

**cProfile** (built-in): Statistical profiling
```bash
python -m cProfile -o profile.pstats myscript.py
python -c "import pstats; p = pstats.Stats('profile.pstats'); p.sort_stats('cumulative').print_stats(20)"
```

**line_profiler**: Line-by-line timing (decorator `@profile`)
```bash
kernprof -l -v myscript.py
```

**memory_profiler**: Line-by-line memory usage
```bash
pip install memory_profiler
python -m memory_profiler myscript.py
```

**Py-Spy**: Sampling profiler, low overhead, attach to running process
```bash
py-spy top --pid <pid>
py-spy record -o profile.svg --pid <pid>
```

**Production profiling:**
- Generate火焰图 (flame graph) for quick visual热点
- Profile only for limited time (circuit breaker)
- ConsiderMTrace (asyncio-specific)

**Optimization workflow:**
1. Profile → identify hot spots
2. Optimize (algorithm, data structure, caching)
3. Re-profile to verify improvement
4. Repeat

---

## Debugging <a name="debugging"></a>

### Production Debugging

**Canary releases**: Gradual rollout, monitor errors before full push

**Feature flags**: Toggle features without deploy
```python
if settings.FEATURE_NEW_UI:
    render_new()
else:
    render_old()
```

**Request IDs**:
```python
import uuid
request_id = uuid.uuid4()
# Add to log context, DB queries, external calls
```

**Log levels**: Temporarily increase logging level for affected component

**Postmortem Analysis**:
- What happened?
- Why did it happen? (root cause)
- How to prevent recurrence?
- Timeline reconstruction (logs, metrics)

**Premortem**: Before release, "What could go wrong?" - proactive risk assessment

**Load testing**:
- Simulate production traffic patterns
- Identify bottlenecks before they hit production
- Tools: Locust, k6, JMeter

**Versioning:**
- Semantic versioning for APIs
- Backward compatibility: never break clients silently
- Incremental changes: deprecate before removal
- Deploy with rollback plan

**Debugpy** (VS Code debugger): Attach to remote Python process:
```python
import debugpy
debugpy.listen(("0.0.0.0", 5678))
debugpy.wait_for_client()  # pause until debugger attaches
```

---

## Applied to 5-Gas Analyzer <a name="applied-5gas"></a>

### Current Architecture (Web App)

**Stack**: Flask + SQLite? (from exhaust-analyzer)
- Single monolith (good for MVP)
- Templates/static served directly by Flask
- Knowledge base in `knowledge/knowledge_base.py`
- Exhaust fault patterns in `engine/assessor.py`

### Proposed: Desktop (Tauri + PyInstaller Sidecar)

**Architecture:**
```
Tauri UI (Rust) → Flask API (port 5678) ←─ PyInstaller onefile (backend.exe)
```

**Data Flow:**
1. User enters gas readings in UI
2. Tauri calls `py_api` (Rust sidecar) → POST `/api/analyze`
3. Flask processes via `engine.assessor.match_patterns()`
4. Returns diagnosis to UI

**Key Considerations:**

1. **Resource Path Resolution** (PyInstaller):
```python
def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

app = Flask(__name__, 
           template_folder=resource_path('templates'),
           static_folder=resource_path('static'))
```

2. **Stateless API**: All state in request; no server-side session

3. **Single Responsibility**:
   - Tauri: UI, native integration, updater
   - Flask: API, engine, business logic
   - `engine/`: Pure Python, testable independently

4. **Configuration**: Use environment variables or config file (not hardcoded)
   - `PORT=5678`
   - `DEBUG=false`
   - `ADSENSE_ID=...`

5. **Logging**: Structured JSON logs to stdout; Tauri captures and displays
   - `{"level":"INFO","message":"Analysis complete","fault_code":"P0420"}`

6. **Metrics**: Internal endpoint `/metrics` for health/diagnostics
   - `analyses_total`, `analysis_duration_seconds`, `fault_detected_total`

7. **Error Handling**:
   - 400 for invalid input (missing fields, out-of-range vals)
   - 500 for internal errors (with request_id for tracing)
   - Log full traceback, return user-friendly message

8. **Versioning**: UA sends `X-App-Version`; server logs for compatibility tracking

9. **Packaging**:
   - Backend: `pyinstaller --onefile --add-data "templates;templates" ...`
   - Frontend: Tauri bundles backend as external binary
   - Both built in CI for Win/Linux/macOS

10. **Updates**: Tauri auto-updater (tauri-updater) downloads new backend+frontend

### Refactoring Opportunities (if needed)

- **Extract engine** as separate Python package (`5gas-engine`) for reuse (web + desktop)
- **Configuration management**: pydantic settings class
- **API versioning**: `/api/v1/analyze` if breaking changes expected
- **OpenAPI spec**: Document API; generate docs; auto-test with schemathesis

---

## Quick Reference

### Project Structure (Flask)
```
myapp/
├── app.py              # Flask app factory
├── requirements.txt
├── config.py           # Config classes
├── blueprints/         # Modular routes
│   └── api.py
├── models/             # SQLAlchemy models
├── schemas/            # Marshmallow/DRF serializers
├── services/           # Business logic
├── utils/              # Helpers
├── static/
├── templates/
└── tests/
```

### Dockerfile (12-Factor)
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV PORT=8000
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:$PORT"]
```

### Systemd Service
```ini
[Unit]
Description=My Flask App
After=network.target

[Service]
User=appuser
WorkingDirectory=/opt/myapp
Environment="PORT=8000"
ExecStart=/opt/myapp/venv/bin/gunicorn app:app --bind 0.0.0.0:$PORT
Restart=always

[Install]
WantedBy=multi-user.target
```

### Celery Beat Schedule
```python
app.conf.beat_schedule = {
    'daily-report': {
        'task': 'tasks.generate_daily_report',
        'schedule': crontab(hour=2, minute=0),  # 2 AM daily
    },
}
```

---

*End of Knowledge Base*
