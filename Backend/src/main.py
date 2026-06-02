# main.py
from __future__ import annotations

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from src.configuration.config import config
from src.application.exception_handler import DomainError
from src.presentation.api.auth.router import router as auth_router
from src.presentation.api.roles.router import router as roles_router
from src.presentation.api.user.router import router as user_router


# ── lifespan ─────────────────────────────────────────────────────────────────

@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    from src.infrastructure.database.postgresql import engine
    from sqlalchemy import text
    async with engine.connect() as conn:
        await conn.execute(text("SELECT 1"))
    print(f"✓ DB connected — {config.APP_NAME} started")
    yield
    # shutdown
    await engine.dispose()
    print("✓ DB connections closed")


# ── app ───────────────────────────────────────────────────────────────────────

app = FastAPI(
    title=config.APP_NAME,
    version=config.APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# ── middleware ────────────────────────────────────────────────────────────────

app.add_middleware(
    CORSMiddleware,
    allow_origins=config.ALLOWED_HOSTS_LIST,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── exception handlers ────────────────────────────────────────────────────────

@app.exception_handler(DomainError)
async def domain_error_handler(request: Request, exc: DomainError):
    return JSONResponse(
        status_code=400,
        content={"detail": exc.message, "code": exc.code},
    )

##@app.exception_handler(Exception)
###async def global_error_handler(request: Request, exc: Exception):
    ##return JSONResponse(
       ## status_code=500,
       # content={
        #    "detail": str(exc) if config.DEBUG else "Internal server error",
         #   "code": "internal_error",
        #},
    #)
###
# ── routers ───────────────────────────────────────────────────────────────────

app.include_router(auth_router, prefix="/api/v1")
app.include_router(roles_router, prefix="/api/v1")
app.include_router(user_router, prefix="/api/v1")

# ── health ────────────────────────────────────────────────────────────────────

@app.get("/health", tags=["Health"])
async def health():
    return {
        "status": "ok",
        "app": config.APP_NAME,
        "env": config.APP_ENV,
    }

@app.get("/", tags=["Health"])
async def root():
    return {"message": f"Welcome to {config.APP_NAME}"}