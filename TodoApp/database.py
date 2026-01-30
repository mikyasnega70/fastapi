from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URL = 'postgresql://my_postgres_db_dz0p_user:TMJFqJ6xaOW5Dp2Pw1VGVN9vdm4SmRcK@dpg-d5ug2vogjchc73a0rmd0-a/my_postgres_db_dz0p'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

# SQLALCHEMY_DATABASE_URL = 'sqlite:///./todosapp.db'

# engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread':False})

session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

