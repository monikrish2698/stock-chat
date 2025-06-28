"""Utility for executing Trino queries against an Iceberg catalog."""
from __future__ import annotations

import os
from typing import List, Dict, Any

from dotenv import load_dotenv
from trino.dbapi import connect

load_dotenv()

_HOST = os.getenv("TRINO_HOST", "localhost")
_PORT = int(os.getenv("TRINO_PORT", 8080))
_USER = os.getenv("TRINO_USER", "trino")
_CATALOG = os.getenv("TRINO_CATALOG", "iceberg")
_SCHEMA = os.getenv("TRINO_SCHEMA", "default")


class TrinoClient:
    def __init__(self) -> None:
        self._conn = connect(  # type: ignore
            host=_HOST,
            port=_PORT,
            user=_USER,
            catalog=_CATALOG,
            schema=_SCHEMA,
        )

    def fetch_all(self, query: str) -> List[Dict[str, Any]]:
        """Execute `query` and return results as list of dicts."""
        cur = self._conn.cursor()
        cur.execute(query)
        columns = [col[0] for col in cur.description]
        rows = cur.fetchall()
        return [dict(zip(columns, row)) for row in rows]
