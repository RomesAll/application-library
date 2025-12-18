from sqlalchemy import text

from src.config.database import engine_sync

with engine_sync.connect() as conn:
    res = conn.execute(text("select version()"))
    print(res.all())