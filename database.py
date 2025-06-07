from sqlalchemy import  create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# create a url to specify the location of db in TodoApp
SQLALCHEMY_DATABASE_URL = 'sqlite:///./todos.db'

# create engine
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={
    'check_same_thread': False
})

SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)

Base = declarative_base()