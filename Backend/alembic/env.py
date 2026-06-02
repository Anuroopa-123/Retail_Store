# alembic/env.py

import sys
import os
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

# ── tell Python where src/ is ─────────────────────────────────────────────────
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# ── load config ───────────────────────────────────────────────────────────────
from src.configuration.config import config as app_config

# ── import all models ─────────────────────────────────────────────────────────
import src.domain.entities  # noqa: F401

# ── get Base ──────────────────────────────────────────────────────────────────
from src.domain.entities.base import BaseModel

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# ── build sync URL ────────────────────────────────────────────────────────────
db = app_config.DB_KWARGS
SYNC_URL = (
    f"postgresql+psycopg2://{db['DB_USERNAME']}:{db['DB_PASSWORD']}"
    f"@{db['DB_HOST']}:{db['DB_PORT']}/{db['DB_NAME']}"
    f"?sslmode=require&channel_binding=require"
)
config.set_main_option("sqlalchemy.url", SYNC_URL)

target_metadata = BaseModel.metadata


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()