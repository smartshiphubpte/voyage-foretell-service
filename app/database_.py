from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import asyncpg  # Ensure asyncpg is imported

# TODO: load from the dotenv

# DB_USER= "postgres"
# DB_PASSWORD= "postgres"
# DB_HOST= "localhost"
# DB_PORT= 5432
# DB_NAME= "postgres"
# DB_SCHEMA= "shipping_db"

DB_USER = "postgres"
DB_PASSWORD = "bzeUm@)=J=*5XRbI"
DB_HOST = "34.93.52.26"
DB_PORT = 5432
DB_NAME = "orion"
DB_SCHEMA = "shipping_db"

# Construct the DATABASE_URL using the variables
DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

print(f"DATABASE_URL {DATABASE_URL}")

# Previous SQLAlchemy engine setup is commented out to keep for reference
# engine = create_async_engine(DATABASE_URL, echo=True)

# Configure the Session class to be used for creating sessions
# AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

# New asyncpg connection pool setup
async def create_db_pool():
    return await asyncpg.create_pool(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

async def get_db():
    pool = await create_db_pool()
    async with pool.acquire() as connection:
        # Optionally, set the schema for the session
        # await connection.execute(f"SET search_path TO {DB_SCHEMA}")
        yield connection
        # The pool and connection are automatically released/closed when exiting the async context
