from __future__ import annotations
from typing import Any
import pymssql
from airflow.providers.common.sql.hooks.sql import DbApiHook
import pyodbc


class MsSqlHook(DbApiHook):
    conn_name_attr = "mssql_conn_id"
    default_conn_name = "mssql_default"
    conn_type = "mssql"
    hook_name = "Microsoft SQL Server"
    supports_autocommit = True
    DEFAULT_SQLALCHEMY_SCHEME = "mssql+pymssql"

    def __init__(self,*args,sqlalchemy_scheme: str | None = None, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.schema = kwargs.pop("schema", None)
        self._sqlalchemy_scheme = sqlalchemy_scheme

    @property
    def connection_extra_lower(self) -> dict:
        conn = self.get_connection(self.mssql_conn_id) 
        return {k.lower(): v for k, v in conn.extra_dejson.items()}
        
    @property
    def sqlalchemy_scheme(self) -> str:
        return (
            self._sqlalchemy_scheme
            or self.connection_extra_lower.get("sqlalchemy_scheme")
            or self.DEFAULT_SQLALCHEMY_SCHEME
        )

    def get_uri(self) -> str:
        from urllib.parse import parse_qs, urlencode, urlsplit, urlunsplit

        r = list(urlsplit(super().get_uri()))
      
        r[0] = self.sqlalchemy_scheme
      
        qs = parse_qs(r[3], keep_blank_values=True)
        for k in list(qs.keys()):
            if k.lower() == "sqlalchemy_scheme":
                qs.pop(k, None)
        r[3] = urlencode(qs, doseq=True)
        return urlunsplit(r)

    def get_sqlalchemy_connection(
        self, connect_kwargs: dict | None = None, engine_kwargs: dict | None = None
    ) -> Any:
       
        engine = self.get_sqlalchemy_engine(engine_kwargs=engine_kwargs)
        return engine.connect(**(connect_kwargs or {}))

    def get_conn(
        self,
    ) -> pymssql.connect:
      
        conn = self.get_connection(self.mssql_conn_id)

        conn = pymssql.connect(
            server=conn.host,
            user=conn.login,
            password=conn.password,
            database=self.schema or conn.schema,
            port=conn.port,
        )
        return conn

    def set_autocommit(
        self,
        conn: pymssql.connect,
        autocommit: bool,
    ) -> None:
        conn.autocommit(autocommit)

    def get_autocommit(self, conn: pymssql.connect):
        return conn.autocommit_state