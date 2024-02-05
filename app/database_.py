from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database configuration from environment variables
DATABASE_URL = f"postgresql+asyncpg://{os.getenv('DB_USER')}:" \
               f"{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:" \
               f"{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"

engine = create_async_engine(DATABASE_URL, echo=True)

# Configure the Session class to be used for creating sessions
AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

async def get_db():
    async with AsyncSessionLocal() as session:
        await session.execute(f"SET search_path TO {os.getenv('DB_SCHEMA')}")
        await session.commit()
        yield session
