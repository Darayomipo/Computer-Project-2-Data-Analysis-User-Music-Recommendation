import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
# Replace 'your_models_module' with the actual name of your module
from models import UserListeningHistory, Song, Base

DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_listening_counts():
    with SessionLocal() as session:
        user_counts = session.query(
            UserListeningHistory.UserID, func.count(UserListeningHistory.HistoryID).label('listen_count')
        ).group_by(UserListeningHistory.UserID).all()
        return user_counts

def get_genre_distribution():
    with SessionLocal() as session:
        genre_counts = session.query(
            Song.Genre, func.count(UserListeningHistory.HistoryID).label('genre_count')
        ).join(Song, Song.SongID == UserListeningHistory.SongID)\
         .group_by(Song.Genre).all()
        return genre_counts

def visualize_data():
    # Fetch data
    user_listening_counts = get_listening_counts()
    genre_distribution = get_genre_distribution()

    # Convert to Pandas DataFrame
    df_user_counts = pd.DataFrame(user_listening_counts, columns=['UserID', 'ListenCount'])
    df_genre_distribution = pd.DataFrame(genre_distribution, columns=['Genre', 'Count'])

    # Visualization 1: Number of Listening Records per User
    plt.figure(figsize=(12, 8))
    sns.barplot(x='UserID', y='ListenCount', data=df_user_counts, palette='viridis')
    plt.title('Number of Listening Records per User')
    plt.xlabel('User ID')
    plt.ylabel('Number of Records')
    plt.xticks(rotation=45)
    plt.show()

    # Visualization 2: Distribution of Genres Across Listening Records
    plt.figure(figsize=(12, 8))
    sns.barplot(x='Genre', y='Count', data=df_genre_distribution, palette='coolwarm')
    plt.title('Distribution of Genres Across Listening Records')
    plt.xlabel('Genre')
    plt.ylabel('Count')
    plt.xticks(rotation=45)
    plt.show()

if __name__ == "__main__":
    visualize_data()
