# scripts/load_movies.py
import pandas as pd
from movies.models import Movie

def load_data(file_name):
    print('Uploading Data . . .')
    df = pd.read_csv(file_name, sep='\t', na_values='\\N')
    # Index(['tconst', 'titleType', 'primaryTitle', 'originalTitle', 'isAdult',
    #        'startYear', 'endYear', 'runtimeMinutes', 'genres'],
        #   dtype='object')


    df['titleType'] = df['titleType'].astype('string')
    df['primaryTitle'] = df['primaryTitle'].astype('string')
    df['originalTitle'] = df['originalTitle'].astype('string')
    # df['isAdult'] = df['originalTitle'].astype(bool)
    df= df[df['originalTitle'].notna()]

    moviesDf = df[df['titleType'] == 'movie']
    print("Data Loaded Succefuly!")
    return moviesDf
 
def saving_data(file_name):
    df = load_data(file_name)
    movies = []

    for _, row in df.iterrows():
        movie = Movie(
            imdb_id=row['tconst'],
            title=row['originalTitle'],
            titleType=row['titleType'] if row['titleType'] else pd.NaT,
            year=int(row['startYear']) if pd.notna(row['startYear']) else None,
            runtime_minutes=int(row['runtimeMinutes']) if pd.notna(row['runtimeMinutes']) else None,
            isAdult=bool(row['isAdult']) if pd.notna(row['isAdult']) else None,
            # average_rating=float(row['average_rating']) if pd.notna(row['average_rating']) else None,
            # num_votes=int(row['num_votes']) if pd.notna(row['num_votes']) else None,
        )
        movies.append(movie)

    Movie.objects.bulk_create(movies, batch_size=1000)
    print("Data Saved Succefuly!")

# Don't forget to call the function properly
saving_data('scripts/title.basics.tsv')




