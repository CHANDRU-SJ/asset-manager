from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.routes import assets

from app.database import engine, Base

app = FastAPI(title="Asset Manager API")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Shutdown: close connections
    await engine.dispose()

app = FastAPI(title="Asset Manager API", lifespan=lifespan)

# Include routes
app.include_router(assets.router)