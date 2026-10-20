from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.database import engine, Base
from app.routers import auth, sedes, consumo, solar

# Crear las tablas automáticamente si no existen en Neon
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="API REST de AnalíticaEnergética Solar para IPS (Proyecto HeliosIPS)"
)

# Configuración de CORS habilitada para permitir peticiones desde Java
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registro de Routers con el prefijo /api/v1
app.include_router(auth.router, prefix=settings.API_V1_STR)
app.include_router(sedes.router, prefix=settings.API_V1_STR)
app.include_router(consumo.router, prefix=settings.API_V1_STR)
app.include_router(solar.router, prefix=settings.API_V1_STR)

@app.get("/")
def root():
    return {
        "sistema": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "estado": "Servidor Activo",
        "base_datos": "Neon PostgreSQL (Cloud)",
        "documentacion_swagger": "/docs"
    }