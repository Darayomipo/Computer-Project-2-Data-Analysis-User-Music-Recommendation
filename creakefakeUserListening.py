import json
from datetime import datetime, timedelta
import random
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, or_
from models import UserListeningHistory, User, Song, Base

# Assuming you have already set up your database URL
DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Helper function to get user's preferred genres
def get_preferred_genres(user_music_genres):
    try:
        # Assuming MusicGenres is stored as a JSON string
        return json.loads(user_music_genres)
    except json.JSONDecodeError:
        # Fallback in case of parsing error, considering it as an empty list
        return []

# Function to create user listening histories with genre diversity
def create_user_listening_histories(db_session):
    # Process all users
    users = db_session.query(User).all()

    for index, user in enumerate(users):
        num_records = 100 if index < 1000 else 5  # First 1000 users get 100 histories, the rest get 5
        preferred_genres = get_preferred_genres(user.MusicGenres)

        if not preferred_genres:
            continue  # Skip users with no preferred genres

        for _ in range(num_records):
            for genre in preferred_genres:
                preferred_songs = db_session.query(Song).filter(Song.Genre == genre).all()

                if preferred_songs:
                    song = random.choice(preferred_songs)  # Randomly select a song from the preferred genre
                    listen_date = datetime.now() - timedelta(days=random.randint(0, 365))  # Random listen date within the last year
                    duration_listened = random.randint(30, song.Duration)  # Random duration from 30 seconds to the full song length

                    history = UserListeningHistory(
                        UserID=user.UserID,
                        SongID=song.SongID,
                        ListenDate=listen_date,
                        DurationListened=duration_listened,
                    )

                    db_session.add(history)
                    break  # Break after adding a song to avoid adding multiple songs from the same genre per iteration
        db_session.commit()

# Main function to run the script
def main():
    db = next(get_db_session())  # Get database session
    create_user_listening_histories(db)

if __name__ == "__main__":
    main()