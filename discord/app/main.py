import logging
# Import asynccontextmanager for managing the lifespan of the FastAPI application
from contextlib import asynccontextmanager

from app.chat.routes import chat_router
from app.utils.logging import setup_logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

print(f"4. working in file /discord/app/main.py)")

# Set up logging configuration, set to INFO level (INFO, DEBUG, WARNING, ERROR, CRITICAL)
setup_logging()

# A decorator that allows you to define an asynchronous context manager.
@asynccontextmanager
async def lifespan(app: FastAPI):
    # code for anything before starting server
    yield
    # code for clean up
    pass


# Middleware to log exceptions


app = FastAPI(
    lifespan=lifespan,
    version="1.0.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or specify domains e.g., ["https://example.com"]
    allow_credentials=True,
    allow_methods=["*"],  # Or specify specific methods e.g., ["GET", "POST"]
    allow_headers=["*"],  # Or specify headers e.g., ["Authorization", "Content-Type"]
)


@app.get("/ready")
def ready():
    return JSONResponse(content={"success": True, "status": "ready"})


# Include API router
app.include_router(chat_router, prefix="/api")
