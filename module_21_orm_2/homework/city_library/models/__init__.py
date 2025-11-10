from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(url="postgresql+psycopg://postgres:postgres@localhost:5432/book_library", echo=True, pool_size=5, max_overflow=10,)

session_factory = sessionmaker(engine)