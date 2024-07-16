import pandas as pd
import psycopg2
from psycopg2.extras import execute_values

# Conexión a la base de datos PostgreSQL
conn = psycopg2.connect(
    dbname='soccer-movies',
    user='user',
    password='password',
    host='localhost',
    port='5432'
)
cursor = conn.cursor()

# Cargar CSVs en DataFrames
critic_reviews = pd.read_csv('critic_reviews.csv')
movies = pd.read_csv('movies.csv')
user_reviews = pd.read_csv('user_reviews.csv')

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
