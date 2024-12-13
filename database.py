from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from databases import Database
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative  import declarative_base

# MySQL database configuration
DB_URL = "mysql+pymysql://root:Sunetra@127.0.0.1:3306/fastapidemo"
engine = create_engine(DB_URL)
Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False,bind=engine)



