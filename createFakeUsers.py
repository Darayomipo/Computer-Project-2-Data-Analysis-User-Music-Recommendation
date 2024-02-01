from faker import Faker
import random
import json
from datetime import datetime
import hashlib  # Import hashlib for SHA-256 hashing
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func

Base = declarative_base()

# User class definition
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    age = Column(Integer)
    country = Column(String)
    hashed_password = Column(String)
    music_genres = Column(Text)  # Stored as JSON string
    RegistrationDate = Column(DateTime, default=func.now())

# Setup SQLAlchemy connection to SQLite
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the tables in the database if they don't already exist
Base.metadata.create_all(bind=engine)

# Faker setup
fake = Faker()
Faker.seed(0)  # Optional: for reproducibility

# Function to generate fake music genres with 3 to 5 random selections
def generate_fake_music_genres():
    genres = ["Jazz", "Pop", "Rock", "Hip Hop", "Afro Beats", "Techno", "Amapiano", "Classical", "Electronic", "Country", "RNB", "Blues"]
    return random.sample(genres, random.randint(3, 5))

# Function to generate a registration date between January 1, 2024, and February 1, 2024
def generate_fake_registration_date():
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2024, 2, 1)
    return fake.date_time_between(start_date=start_date, end_date=end_date)

# Hash the password using SHA-256
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Function to add fake users to the database
def add_fake_users_to_database(num_users=10):
    # Create a new SQLAlchemy session
    db = SessionLocal()
    try:
        for _ in range(num_users):
            # Serialize the list of genres to a JSON string for storage
            music_genres_json = json.dumps(generate_fake_music_genres())

            # Create a fake user
            fake_user = User(
                username=fake.unique.user_name(),
                email=fake.unique.email(),
                age=random.randint(18, 50),
                country=fake.country(),
                hashed_password=hash_password("Test25"),
                music_genres=music_genres_json,
                RegistrationDate=generate_fake_registration_date()
            )
            db.add(fake_user)  # Add the fake user to the session
        db.commit()  # Commit the transaction for all users
        print(f"{num_users} fake users added to database.")
    except Exception as e:
        print(f"Error adding users to database: {e}")
        db.rollback()
    finally:
        db.close()  # Close the session

# Example usage: Create and add 10 users
add_fake_users_to_database(25)
