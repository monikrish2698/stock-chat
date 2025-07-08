from dotenv import load_dotenv
import trino
from contextlib import contextmanager
from typing import Iterator
import os

load_dotenv()

class TrinoConnection:
    def __init__(self, 
                 host: str,
                 port: int,
                 user: str,
                 catalog: str, auth) -> None:
        self._connection_params = {
            "host": host,
            "port": port,
            "user": user,
            "http_scheme" : "https",
            "catalog": catalog,
            "auth": auth
        }

        self.__conn = None

    def connect(self) -> None:
        params = self._connection_params.copy()
        self.__conn = trino.dbapi.connect(**params)
    
    def close(self) -> None:
        if self.__conn is not None:
            self.__conn.close()
            self.__conn = None
    
    @contextmanager
    def connection(self):
        try:
            self.connect()
            yield self.__conn
        finally:
            self.close()

db_params = {
    "host": os.getenv("TRINO_HOST", "localhost"),
    "port": int(os.getenv("TRINO_PORT", 8080)),
    "user": os.getenv("TRINO_USER", "trino"),
    "catalog": os.getenv("TRINO_CATALOG", "iceberg"),
    "auth" : trino.auth.BasicAuthentication(os.getenv("TRINO_USER"), os.getenv("TRINO_PWD"))
}

trino_connection = TrinoConnection(**db_params)

