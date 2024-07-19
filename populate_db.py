import os
import time
import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
from uuid import UUID

# Esperar hasta que la base de datos esté lista
time.sleep(10)


# Conexión a la base de datos PostgreSQL
conn = psycopg2.connect(
    dbname='soccer-movies',
    user='user',
    password='password',
    host='db',
    port='5432'
)
cursor = conn.cursor()
csv_path = '/files'

# Función para reemplazar NaN en columnas booleanas
def replace_nan_with_boolean(df, boolean_columns):
    for col in boolean_columns:
        if col in df.columns:
            df[col] = df[col].fillna(False).astype(bool)

# Función para convertir columnas a string (para UUIDs)
def convert_to_string(df, uuid_columns):
    for col in uuid_columns:
        if col in df.columns:
            df[col] = df[col].apply(lambda x: str(x) if pd.notna(x) else None)

# Cargar CSVs en DataFrames
critic_reviews = pd.read_csv(os.path.join(csv_path, 'critic_reviews.csv'))
movies = pd.read_csv(os.path.join(csv_path, 'movies.csv'))
user_reviews = pd.read_csv(os.path.join(csv_path, 'user_reviews.csv'))

# Reemplazar NaN con booleanos en columnas booleanas
replace_nan_with_boolean(critic_reviews, [
    'isFresh', 'isRotten', 'isRtUrl', 'isTopCritic'
])
replace_nan_with_boolean(user_reviews, [
    'isVerified', 'isSuperReviewer', 'hasSpoilers', 'hasProfanity'
])

# Convertir columnas UUID a string
convert_to_string(critic_reviews, ['movieId'])
convert_to_string(movies, ['movieId'])
convert_to_string(user_reviews, ['movieId'])

# Reemplazar NaN con booleanos
replace_nan_with_boolean(critic_reviews, ['boolean_col1', 'boolean_col2'])  # Reemplaza con nombres de columnas booleanas reales
replace_nan_with_boolean(movies, ['boolean_col1', 'boolean_col2'])
replace_nan_with_boolean(user_reviews, ['boolean_col1', 'boolean_col2'])

# Insertar datos en la tabla critic_reviews
critic_reviews_tuples = [tuple(x) for x in critic_reviews.to_numpy()]
critic_reviews_cols = ','.join(list(critic_reviews.columns))
insert_query = f"INSERT INTO critic_reviews ({critic_reviews_cols}) VALUES %s"
execute_values(cursor, insert_query, critic_reviews_tuples)

# Insertar datos en la tabla movies
movies_tuples = [tuple(x) for x in movies.to_numpy()]
movies_cols = ','.join(list(movies.columns))
insert_query = f"INSERT INTO movies ({movies_cols}) VALUES %s"
execute_values(cursor, insert_query, movies_tuples)

# Insertar datos en la tabla user_reviews
user_reviews_tuples = [tuple(x) for x in user_reviews.to_numpy()]
user_reviews_cols = ','.join(list(user_reviews.columns))
insert_query = f"INSERT INTO user_reviews ({user_reviews_cols}) VALUES %s"
execute_values(cursor, insert_query, user_reviews_tuples)

# Confirmar cambios y cerrar conexión
conn.commit()
cursor.close()
conn.close()
