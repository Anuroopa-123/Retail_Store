# main.py
from __future__ import annotations

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from slowapi.middleware import SlowAPIMiddleware
from src.infrastructure.security.rate_limit import limiter
from pathlib import Path
from starlette.middleware.trustedhost import TrustedHostMiddleware
from src.infrastructure.security.middleware import SecurityHeadersMiddleware

from src.configuration.config import config
from src.application.exception_handler import DomainError
from src.presentation.api.auth.router import router as auth_router
from src.presentation.api.roles.router import router as roles_router
from src.presentation.api.user.router import router as user_router
from fastapi.staticfiles import StaticFiles
from src.presentation.api.tenant.router import (
    router as tenant_router
)
from src.presentation.api.store.router import (
    router as store_router
)
from src.presentation.api.admin.router import (
    router as admin_router
)
from src.presentation.api.employee.router import (
    router as employee_router
)
from src.presentation.api.department.router import (
    router as department_router
)
from src.presentation.api.admin.profile_router import (
    router as admin_profile_router
)

from src.presentation.api.product_category.router import (
    router as product_category_router
)
BASE_DIR = Path(__file__).resolve().parent.parent

UPLOAD_DIR = BASE_DIR / "uploads"

print("UPLOAD_DIR =", UPLOAD_DIR)
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

app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)

# ── security middleware ───────────────────────────────────────────────────────


# app.add_middleware(
#     TrustedHostMiddleware,
#     allowed_hosts=[
#         "localhost",
#         "127.0.0.1",
#     ]
# )

app.add_middleware(SecurityHeadersMiddleware)

# ── middleware ────────────────────────────────────────────────────────────────

app.add_middleware(
    CORSMiddleware,
    allow_origins=config.CORS_ORIGINS_LIST,
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
app.include_router(
    tenant_router,
    prefix="/api/v1"
)
app.include_router(
    store_router,
    prefix="/api/v1"
)
app.include_router(
    admin_router,
    prefix="/api/v1"
)

app.include_router(
    employee_router,
    prefix="/api/v1"
)
app.include_router(
    department_router,
    prefix="/api/v1"
)
app.include_router(

    admin_profile_router,

    prefix="/api/v1"

)
app.include_router(
    product_category_router,
    prefix="/api/v1"
)
app.mount(
    "/uploads",
    StaticFiles(directory=str(UPLOAD_DIR)),
    name="uploads"
)
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