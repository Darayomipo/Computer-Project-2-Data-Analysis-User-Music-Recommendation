import json
from sqlalchemy import DateTime
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    
    age = Column(Integer)
    country = Column(String) 
    hashed_password = Column(String)
    music_genres = Column(Text)  
    RegistrationDate = Column(DateTime)


    def set_genres(self, genres_list):
        self.music_genres = json.dumps(genres_list)

    def get_genres(self):
        return json.loads(self.music_genres)

Base.metadata.create_all(bind=engine)
