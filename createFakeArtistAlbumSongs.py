import sqlite3
from faker import Faker
import random
from datetime import datetime

# Create a Faker instance
fake = Faker()

# Define data generation parameters
num_artists = 2000
num_songs = 10000

# Define the list of genres
genres = ["Jazz", "Pop", "Rock", "Hip Hop", "Afro Beats", "Techno",
          "Amapiano", "Classical", "Electronic", "Country", "R&B", "Blues"]

# Establish a connection to the database ('test.db')
conn = sqlite3.connect('test.db')
cursor = conn.cursor()

# Table Creation (add any error handling you deem necessary)
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

    num_albums_for_artist = random.randint(0, 3)  
    for _ in range(num_albums_for_artist):
        album_title = fake.sentence(nb_words=4)
        album_release_date = fake.date_between(start_date='-10y')
        cursor.execute("INSERT INTO Albums (Title, ArtistID, ReleaseDate, Genre) VALUES (?, ?, ?, ?)",
                       (album_title, artist_id, album_release_date, artist_genre))
        album_counter += 1

# Insert Songs
for song_id in range(1, num_songs + 1):
    song_title = fake.sentence(nb_words=4)
    song_duration = fake.random_int(min=120, max=360)

    if random.random() < 0.7: 
        album_id = random.randint(1, album_counter)
        cursor.execute("SELECT Genre, ReleaseDate FROM Albums WHERE AlbumID = ?", (album_id,))
        song_genre, album_release_str = cursor.fetchone() 
        album_release_date = datetime.strptime(album_release_str, '%Y-%m-%d').date() 
        song_release_date = album_release_date  
    else:
        album_id = None
        artist_id = random.randint(1, num_artists)
        cursor.execute("SELECT Genre FROM Artists WHERE ArtistID = ?", (artist_id,))
        song_genre = cursor.fetchone()[0]
        song_release_date = fake.date_between(start_date='-10y')

    cursor.execute("INSERT INTO Songs (Title, ArtistID, AlbumID, Genre, Duration, ReleaseDate) VALUES (?, ?, ?, ?, ?, ?)",
                   (song_title, artist_id, album_id, song_genre, song_duration, song_release_date))

# Commit changes and close 
conn.commit()
conn.close()

print("Database 'test.db' populated with fake data.")
