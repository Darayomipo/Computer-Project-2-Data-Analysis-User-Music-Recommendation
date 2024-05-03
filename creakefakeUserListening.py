#This script was developed with the support of advanced AI tools alongside my contributions in detailing the specifications and requirements.
from datetime import datetime, timedelta
import json
import random
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import UserListeningHistory, User, Song, Base

DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_preferred_genres(user_music_genres):
    try:
        return json.loads(user_music_genres)
    except json.JSONDecodeError:
        return []

def create_user_listening_histories(db_session):
    users = db_session.query(User).all()

    for index, user in enumerate(users):
        num_records = 10 if index < 100 else 2
        preferred_genres = get_preferred_genres(user.MusicGenres)

        if not preferred_genres:
            continue

        for _ in range(num_records):
            for genre in preferred_genres:
                preferred_songs = db_session.query(Song).filter(Song.Genre == genre).all()

                if preferred_songs:
                    song = random.choice(preferred_songs)
                    listen_date = datetime.now() - timedelta(days=random.randint(0, 365))
                    duration_listened = random.randint(30, song.Duration)

                    history = UserListeningHistory(
                        UserID=user.UserID,
                        SongID=song.SongID,
                        ListenDate=listen_date,
                        DurationListened=duration_listened,
                        Age=user.Age,
                        UserLocation=user.Country,  # Assuming User model has a Country attribute
                        SongGenre=song.Genre  # Directly using the genre of the chosen song
                    )

                    db_session.add(history)
                    break
        db_session.commit()

def main():
    db = next(get_db_session())
    create_user_listening_histories(db)

if __name__ == "__main__":
    main()
