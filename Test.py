import sqlite3
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MultiLabelBinarizer

# Connect to SQLite database
conn = sqlite3.connect('test.db')

# Fetch data
query = "SELECT Age, Country, MusicGenres FROM users"
df = pd.read_sql_query(query, conn)
conn.close()

# Processing the MusicGenres data
# Assume MusicGenres are stored as comma-separated values
df['MusicGenres'] = df['MusicGenres'].apply(lambda x: x.split(','))

# MultiLabelBinarizer to transform the MusicGenres column
mlb = MultiLabelBinarizer()
genres = mlb.fit_transform(df['MusicGenres'])
genres_df = pd.DataFrame(genres, columns=mlb.classes_)

# Concatenate age and country data with genre data
# Optional: Further encode 'Country' with pd.get_dummies() if needed
final_df = pd.concat([df[['Age']], genres_df], axis=1)

# Calculate similarity matrix
similarity_matrix = cosine_similarity(final_df)

# Function to get recommendations
def get_recommendations(user_index, top_n=3):
    similar_scores = list(enumerate(similarity_matrix[user_index]))
    similar_scores = sorted(similar_scores, key=lambda x: x[1], reverse=True)
    similar_scores = similar_scores[1:top_n+1]  # Skip the user itself
    user_indices = [i[0] for i in similar_scores]
    return df['MusicGenres'].iloc[user_indices]

# Example: Get recommendations for the first user
recommendations = get_recommendations(0)
print("Recommended Music Genres for User 0:")
for genres in recommendations:
    print(genres)
