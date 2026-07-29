import os
from sqlmodel import SQLModel, create_engine, Session

DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL:
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

    # Supabase requires SSL. Serverless (Vercel) functions are short-lived,
    # so keep pooling minimal and recycle connections quickly to avoid
    # "too many connections" errors against Supabase's pooler.
    connect_args = {"sslmode": "require"} if "sslmode" not in DATABASE_URL else {}
    engine = create_engine(
        DATABASE_URL,
        echo=False,
        pool_pre_ping=True,
        pool_size=1,
        max_overflow=2,
        pool_recycle=300,
        connect_args=connect_args,
    )
else:
    # NOTE: On Vercel this branch will crash on any write, since the
    # serverless filesystem is read-only outside /tmp. If you see this
    # branch being hit in production logs, DATABASE_URL isn't reaching
    # the deployed function — check the Vercel env var scope (Production
    # vs Preview vs Development) and redeploy after setting it.
    sqlite_file_name = "/tmp/vault.db"
    sqlite_url = f"sqlite:///{sqlite_file_name}"
    connect_args = {"check_same_thread": False}
    engine = create_engine(sqlite_url, connect_args=connect_args)
    print("[WARNING] DATABASE_URL not set — falling back to ephemeral SQLite in /tmp.")


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
