#ChatGpt and Oluwadarasimi
from faker import Faker
import random
import json
from datetime import datetime
import hashlib
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    UserID = Column(Integer, primary_key=True, index=True)
    Username = Column(String, unique=True, index=True)
    Email = Column(String, unique=True, index=True)
    Age = Column(Integer)
    Country = Column(String)
    HashedPassword = Column(String)
    MusicGenres = Column(Text)  # Stored as JSON string
    RegistrationDate = Column(DateTime, default=func.now())

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

fake = Faker()
Faker.seed(0)

def generate_fake_music_genres():
    genres = ["Jazz", "Pop", "Rock", "Hip Hop", "Afro Beats", "Techno", "Amapiano", "Classical", "Electronic", "Country", "RNB", "Blues"]
    return random.sample(genres, random.randint(3, 5))

def generate_fake_registration_date():
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2024, 2, 1)
    return fake.date_time_between(start_date=start_date, end_date=end_date)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def add_fake_users_to_database(num_users=10000):
    db = SessionLocal()
    try:
        for _ in range(num_users):
            music_genres_json = json.dumps(generate_fake_music_genres())
            fake_user = User(
                Username=fake.unique.user_name(),
                Email=fake.unique.email(),
                Age=random.randint(18, 50),
                Country=fake.country(),
                HashedPassword=hash_password("Test1234"),  # Use a fake password and hash it
                MusicGenres=music_genres_json,
                RegistrationDate=generate_fake_registration_date()
            )
            db.add(fake_user)
        db.commit()
        print(f"{num_users} fake users added to database.")
    except Exception as e:
        print(f"Error adding users to database: {e}")
        db.rollback()
    finally:
        db.close()

add_fake_users_to_database()  # Example: Add 25 fake users to the database
