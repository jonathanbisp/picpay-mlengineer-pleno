import sqlite3
from fastapi import FastAPI
from loguru import logger

from core.app import AppSettings


async def connect_to_db(app: FastAPI, settings: AppSettings) -> None:
    logger.info("Connecting to SQLite database")
    app.state.db = sqlite3.connect(
        "./storage/db.db",
        check_same_thread=False,
        autocommit=True
    )
    app.state.db.execute(
        """CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY, 
            dep_time INTEGER NOT NULL,
            arr_time INTEGER NOT NULL,
            prediction Decimal(14, 28),
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )"""
    )
    app.state.db.commit()
    logger.info("Connection established")


async def close_db_connection(app: FastAPI) -> None:
    logger.info("Closing connection to database")
    app.state.db.close()
    logger.info("Connection closed")
