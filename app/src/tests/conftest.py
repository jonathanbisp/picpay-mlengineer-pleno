import pytest
from fastapi import FastAPI
from asgi_lifespan import LifespanManager
import sqlite3
from httpx import AsyncClient
from dependencies.sqlite import get_db
import pytest_asyncio


@pytest.fixture
def app() -> FastAPI:
    from main import get_application  # local import for testing purpose

    return get_application()


@pytest_asyncio.fixture
async def initialized_app(app: FastAPI) -> FastAPI:
    def get_db_mock(): 
        db = sqlite3.connect(
            "file::memory:",
            check_same_thread=False,
            autocommit=True
        )
        db.execute(
            """CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY, 
                dep_time INTEGER NOT NULL,
                arr_time INTEGER NOT NULL,
                prediction Decimal(14, 28),
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )"""
        )
        db.commit()
        return db
    
    app.dependency_overrides[get_db] = get_db_mock
        
        

@pytest.fixture
def db(initialized_app: FastAPI) -> sqlite3.Connection:
    return initialized_app.state.db


@pytest_asyncio.fixture
async def client(initialized_app: FastAPI) -> AsyncClient:
    async with AsyncClient(
        app=initialized_app,
        base_url="http://testserver",
        headers={"Content-Type": "application/json"},
    ) as client:
        yield client
        
        