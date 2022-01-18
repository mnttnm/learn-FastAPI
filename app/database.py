from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# defining the base class for the models that we are going to define for our tables
Base = declarative_base()


# for every API request a session is established with dbms and then
# once the request is done, the session is terminated
# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# not getting used, as we are using sqlalchemy to connect to db
# while True:
#     try:
#         # cursor_factory is needed to get column name for the table
#         conn = psycopg2.connect(
#             host='localhost', database='fastapi', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()  # to be used to execute sql statement
#         print('Database connection was successful')
#         break
#     except Exception as error:
#         print('db connection failed, error: ', error)
#         time.sleep(2)
