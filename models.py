# Disclaimer
# This project was developed with assistance from various external resources to ensure accuracy and 
# comprehensiveness. Notably, I utilized guidance and support from OpenAI's ChatGPT for advanced coding techniques and theoretical
# insights. Additionally, educational resources such as GeeksforGeeks.org were consulted for specific programming challenges and 
# best practices. The integration of these resources was crucial in enhancing the quality and reliability of the work presented.

import json
from sqlalchemy import DateTime
from datetime import datetime
from sqlalchemy import create_engine, ForeignKey, Date, REAL, CheckConstraint, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker,relationship

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    UserID = Column(Integer, primary_key=True, index=True)
    Username = Column(String, unique=True, index=True)
    Email = Column(String, unique=True, index=True)
    
    Age = Column(Integer)
    Country = Column(String) 
    HashedPassword = Column(String)
    MusicGenres = Column(Text)  
    RegistrationDate = Column(DateTime)



    def set_genres(self, genres_list):
        self.MusicGenres = json.dumps(genres_list)

    def get_genres(self):
        return json.loads(self.MusicGenres)
    


        
    
class Song(Base):
    __tablename__ = 'songs'
    SongID = Column(Integer, primary_key=True, autoincrement=True)
    Title = Column(String, nullable=False)
    ArtistID = Column(Integer, ForeignKey('artists.ArtistID'))
    AlbumID = Column(Integer, ForeignKey('albums.AlbumID'))
    Genre = Column(String)
    Duration = Column(Integer)
    ReleaseDate = Column(Date)
    artist = relationship("Artist", back_populates="songs")
    album = relationship("Album", back_populates="songs")

class Artist(Base):
    __tablename__ = 'artists'
    ArtistID = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(String, nullable=False)
    Bio = Column(Text)
    Genre = Column(String)
    songs = relationship("Song", back_populates="artist")
    albums = relationship("Album", back_populates="artist")

class Album(Base):
    __tablename__ = 'albums'
    AlbumID = Column(Integer, primary_key=True, autoincrement=True)
    Title = Column(String, nullable=False)
    ArtistID = Column(Integer, ForeignKey('artists.ArtistID'))
    ReleaseDate = Column(Date)
    Genre = Column(String)
    artist = relationship("Artist", back_populates="albums")
    songs = relationship("Song", back_populates="album")

class UserListeningHistory(Base):
    __tablename__ = 'userlisteninghistory'
    HistoryID = Column(Integer, primary_key=True, autoincrement=True)
    UserID = Column(Integer, ForeignKey('users.UserID'))
    SongID = Column(Integer, ForeignKey('songs.SongID'))
    ListenDate = Column(DateTime, default=datetime.now)
    DurationListened = Column(Integer)
    Age = Column(Integer)
    UserLocation = Column(String)  # New field for storing user location
    SongGenre = Column(String)  # New field for storing song genre
    user = relationship("User")
    song = relationship("Song")

class UserRatings(Base):
    __tablename__ = 'userratings'
    RatingID = Column(Integer, primary_key=True, autoincrement=True)
    UserID = Column(Integer, ForeignKey('users.UserID'))
    SongID = Column(Integer, ForeignKey('songs.SongID'))
    Rating = Column(Integer, CheckConstraint('Rating >= 1 AND Rating <= 5'))
    user = relationship("User")
    song = relationship("Song")

class UserPreferences(Base):
    __tablename__ = 'userpreferences'
    PreferenceID = Column(Integer, primary_key=True, autoincrement=True)
    UserID = Column(Integer, ForeignKey('users.UserID'))
    Genre = Column(String)
    ArtistID = Column(Integer, ForeignKey('artists.ArtistID'))
    user = relationship("User")
    artist = relationship("Artist")
    
    def set_preference(self, user_id, genre, artist_id):
        self.UserID = user_id
        self.Genre = genre
        self.ArtistID = artist_id
   

class AudioFeatures(Base):
    __tablename__ = 'audiofeatures'
    FeatureID = Column(Integer, primary_key=True, autoincrement=True)
    SongID = Column(Integer, ForeignKey('songs.SongID'))
    Tempo = Column(REAL)
    Key = Column(Integer)
    Energy = Column(REAL)
    Danceability = Column(REAL)
    Valence = Column(REAL)
    song = relationship("Song")

Base.metadata.create_all(bind=engine)
