import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx
from wordcloud import WordCloud

# Database connection
db_path = 'test.db'
conn = sqlite3.connect(db_path)

# Fetch data from Songs table
songs_query = "SELECT * FROM Songs"
songs_data = pd.read_sql_query(songs_query, conn)

# Fetch data from UserListeningHistory table
listening_history_query = "SELECT * FROM UserListeningHistory"
user_listening_history = pd.read_sql_query(listening_history_query, conn)

# Close the database connection
conn.close()

# Merging UserListeningHistory with Songs to get Genre and ReleaseDate
listening_history_merged = user_listening_history.merge(songs_data[['SongID', 'Genre', 'ReleaseDate']], on='SongID')

# Visualization and Analysis

# 1. Histogram of song durations
plt.figure(figsize=(10, 6))
sns.histplot(songs_data['Duration'], bins=30, kde=True)
plt.title('Distribution of Song Durations')
plt.xlabel('Duration (seconds)')
plt.ylabel('Frequency')
plt.show()

# 2. Box plot for song duration across genres
plt.figure(figsize=(12, 8))
sns.boxplot(data=songs_data, x='Genre', y='Duration')
plt.title('Song Duration Distribution by Genre')
plt.xlabel('Genre')
plt.ylabel('Duration (seconds)')
plt.show()

# 3. Average duration over time (by month)
songs_data['ReleaseDate'] = pd.to_datetime(songs_data['ReleaseDate'])
songs_data['YearMonth'] = songs_data['ReleaseDate'].dt.to_period('M')
average_duration_over_time = songs_data.groupby('YearMonth')['Duration'].mean().reset_index()
average_duration_over_time['YearMonth'] = average_duration_over_time['YearMonth'].astype(str)

plt.figure(figsize=(14, 6))
sns.lineplot(data=average_duration_over_time, x='YearMonth', y='Duration')
plt.title('Average Song Duration Over Time')
plt.xlabel('Year-Month')
plt.ylabel('Average Duration (seconds)')
plt.xticks(rotation=45)
plt.show()

# 4. Distribution of how long users listen to songs
plt.figure(figsize=(10, 6))
sns.histplot(listening_history_merged['DurationListened'], bins=30, kde=True)
plt.title('Distribution of Duration Listened by Users')
plt.xlabel('Duration Listened (seconds)')
plt.ylabel('Frequency')
plt.show()

# 5. Average Duration Listened by Genre
avg_duration_listened_by_genre = listening_history_merged.groupby('Genre')['DurationListened'].mean().reset_index()

plt.figure(figsize=(12, 8))
sns.barplot(data=avg_duration_listened_by_genre, x='Genre', y='DurationListened')
plt.title('Average Duration Listened by Genre')
plt.xlabel('Genre')
plt.ylabel('Average Duration Listened (seconds)')
plt.show()
#Assuming 'listening_history_merged' includes a 'Count' column for aggregating listen counts by Genre


#6 Pie Charts for Proportion of Songs in Each Genre
genre_proportions = songs_data['Genre'].value_counts()

plt.figure(figsize=(10, 8))
plt.pie(genre_proportions, labels=genre_proportions.index, autopct='%1.1f%%', startangle=140)
plt.title('Proportion of Songs by Genre')
plt.show()

#7  Genre Popularity Bar Chart (based on listen counts)
genre_popularity = listening_history_merged.groupby('Genre')['UserID'].count().reset_index(name='ListenCount').sort_values(by='ListenCount', ascending=False)
plt.figure(figsize=(12, 8))
sns.barplot(data=genre_popularity, x='Genre', y='ListenCount')
plt.title('Genre Popularity Based on Listen Counts')
plt.xlabel('Genre')
plt.ylabel('Listen Count')
plt.xticks(rotation=45)
plt.show()





