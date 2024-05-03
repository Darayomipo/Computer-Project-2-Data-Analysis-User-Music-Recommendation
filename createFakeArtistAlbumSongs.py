#This script was developed with the support of advanced AI tools alongside my contributions in detailing the specifications and requirements.
import sqlite3
from faker import Faker
import random
from datetime import datetime

# --- Setup ---

# Create a Faker instance
fake = Faker()

# Data generation parameters
num_artists = 500
num_songs = 1000

# List of possible music genres
genres = ["Jazz", "Pop", "Rock", "Hip Hop", "Afro Beats", "Techno",
          "Amapiano", "Classical", "Electronic", "Country", "RNB", "Blues"]

# --- Database Interaction ---

# Connect to the database (creates 'test.db' if it doesn't exist)
conn = sqlite3.connect('test.db')
cursor = conn.cursor()

# Create database tables if they don't already exist 
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Songs (
        SongID INTEGER PRIMARY KEY AUTOINCREMENT,
        Title TEXT NOT NULL,
        ArtistID INTEGER,
        AlbumID INTEGER,
        Genre TEXT,
        Duration INTEGER,  
        ReleaseDate DATE,
        FOREIGN KEY (ArtistID) REFERENCES Artists(ArtistID),
        FOREIGN KEY (AlbumID) REFERENCES Albums(AlbumID)
    );
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Artists (
        ArtistID INTEGER PRIMARY KEY AUTOINCREMENT,
        Name TEXT NOT NULL,
        Bio TEXT,
        Genre TEXT
    );
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Albums (
        AlbumID INTEGER PRIMARY KEY AUTOINCREMENT,
        Title TEXT NOT NULL,
        ArtistID INTEGER,
        ReleaseDate DATE,
        Genre TEXT,
        FOREIGN KEY (ArtistID) REFERENCES Artists(ArtistID)
    );
''')

# --- Data Insertion ---

# Insert Artists
for _ in range(num_artists):
    artist_name = fake.name()
    artist_bio = fake.text(max_nb_chars=200)
    artist_genre = random.choice(genres)
    cursor.execute("INSERT INTO Artists (Name, Bio, Genre) VALUES (?, ?, ?)",
                   (artist_name, artist_bio, artist_genre))

# Insert Albums 
album_counter = 0
for artist_id in range(1, num_artists + 1):
    cursor.execute("SELECT Genre FROM Artists WHERE ArtistID = ?", (artist_id,))
    artist_genre = cursor.fetchone()[0]

    num_albums_for_artist = random.randint(1, 3)  
    for _ in range(num_albums_for_artist):
        album_title = fake.sentence(nb_words=4)
        album_release_date = fake.date_between(start_date='-10y')
        cursor.execute("INSERT INTO Albums (Title, ArtistID, ReleaseDate, Genre) VALUES (?, ?, ?, ?)",
                       (album_title, artist_id, album_release_date, artist_genre))
        album_counter += 1

        # Insert at least 7 songs for the album
        for _ in range(7):
            song_title = fake.sentence(nb_words=4)
            song_duration = fake.random_int(min=120, max=360)
            cursor.execute("INSERT INTO Songs (Title, ArtistID, AlbumID, Genre, Duration, ReleaseDate) VALUES (?, ?, ?, ?, ?, ?)",
                           (song_title, artist_id, album_counter, artist_genre, song_duration, album_release_date))

            num_songs -= 1  # Decrement the remaining songs needed
            if num_songs == 0:
                break  # Exit the song loop if we've reached the target

# Insert remaining songs (if any)
while num_songs > 0: 
    song_title = fake.sentence(nb_words=4)
    song_duration = fake.random_int(min=120, max=360)

    if random.random() < 0.7: 
        album_id = random.randint(1, album_counter)
    else:
        album_id = None
        artist_id = random.randint(1, num_artists)
        cursor.execute("SELECT Genre FROM Artists WHERE ArtistID = ?", (artist_id,))
        song_genre = cursor.fetchone()[0]

    cursor.execute("INSERT INTO Songs (Title, ArtistID, AlbumID, Genre, Duration, ReleaseDate) VALUES (?, ?, ?, ?, ?, ?)",
                   (song_title, artist_id, album_id, song_genre, song_duration, fake.date_between(start_date='-10y')))
    num_songs -= 1 

# Save changes and close the connection
conn.commit()
conn.close()

print("Database 'test.db' populated with fake data.")