from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from app.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="API REST pour la gestion des dépenses personnelles",
    debug=False,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def normalize_error(code: str, message: str, details=None):
    return {"error": {"code": code, "message": message, "details": details}}


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(status_code=exc.status_code, content=normalize_error("HTTP_ERROR", str(exc.detail)))


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(status_code=422, content=normalize_error("VALIDATION_ERROR", "Paramètres invalides", exc.errors()))


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    return JSONResponse(status_code=500, content=normalize_error("INTERNAL_ERROR", "Erreur interne du serveur"))


@app.get("/", tags=["Root"])
def read_root():
    return {
        "message": "Bienvenue sur l'API LedgerOne",
        "version": settings.VERSION,
        "documentation": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "healthy"}


from app.api.routes import categories, transactions
from app.api.routes import settings as settings_router
from app.api.routes import insights
from app.api.routes import alerts
from app.api.routes import import_csv
app.include_router(categories.router, prefix=settings.API_PREFIX)
app.include_router(transactions.router, prefix=settings.API_PREFIX)
app.include_router(settings_router.router, prefix=settings.API_PREFIX)
app.include_router(insights.router, prefix=settings.API_PREFIX)
app.include_router(alerts.router, prefix=settings.API_PREFIX)
app.include_router(import_csv.router, prefix=settings.API_PREFIX)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=False)
