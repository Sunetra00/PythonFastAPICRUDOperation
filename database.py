from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from databases import Database
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative  import declarative_base

# MySQL database configuration
DB_URL = "mysql+pymysql://root:Sunetra@127.0.0.1:3306/fastapidemo"
engine = create_engine(
	DB_URL,
	pool_size=10,          # Number of connections to keep in the pool
    max_overflow=5,        # Extra connections allowed beyond pool_size
    pool_timeout=30,       # Wait time (in seconds) for a connection
    pool_recycle=1800,     # Recycle connections after 30 minutes to avoid stale connections
)
# Base class for models
Base = declarative_base()
# Session Factory for the database
SessionLocal = sessionmaker(autocommit=False,bind=engine)

# Dependency for database session
def get_db():
    db = SessionLocal()
    try:
        yield db # Provide a database session
    finally:
        db.close()  # Add parentheses here # Ensure the session is closed after use