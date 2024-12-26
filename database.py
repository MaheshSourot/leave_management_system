from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

SQL_ALCHEMY_URL="mysql+pymysql://root:Mahesh1234@localhost/leave_system"

engine=create_engine(SQL_ALCHEMY_URL,echo=True)

SessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base=declarative_base()

