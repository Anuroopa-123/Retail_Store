# src/infrastructure/database/postgresql.py

from src.configuration.config import config
from sqlalchemy import URL
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

# Load database settings
db_settings = config.DB_KWARGS  # type: ignore

# ── Async URL (runtime) ───────────────────────────────────────────────────────
SQLALCHEMY_DATABASE_URL = URL.create(
    drivername="postgresql+asyncpg",
    username=db_settings["DB_USERNAME"],
    password=db_settings["DB_PASSWORD"],
    host=db_settings["DB_HOST"],
    database=db_settings["DB_NAME"],
    port=db_settings["DB_PORT"],
)

# ── Sync URL (alembic only) ───────────────────────────────────────────────────
SQLALCHEMY_SYNC_URL = URL.create(
    drivername="postgresql+psycopg2",
    username=db_settings["DB_USERNAME"],
    password=db_settings["DB_PASSWORD"],
    host=db_settings["DB_HOST"],
    database=db_settings["DB_NAME"],
    port=db_settings["DB_PORT"],
    query={"sslmode": "require", "channel_binding": "require"},
)

# ── Async engine ──────────────────────────────────────────────────────────────
engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_size=20,
    max_overflow=5,
    pool_pre_ping=True,        # handles Neon cold starts
    pool_recycle=300,          # recycle connections every 5 min
    echo=config.DEBUG,
    connect_args={
        "ssl": "require",      # Neon requires SSL
    },
)

# ── Session factory ───────────────────────────────────────────────────────────
SessionLocal = async_sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=True,
    expire_on_commit=False,
)


async def get_session():
    """Inject DB session into FastAPI routes via Depends(get_session)."""
    async with SessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()