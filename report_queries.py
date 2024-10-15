import os
import psycopg2
import pandas as pd

def connect_db():
    user = os.getenv('POSTGRES_USER')
    password = os.getenv('POSTGRES_PASSWORD')
    db = os.getenv('POSTGRES_DB')
    host = os.getenv('POSTGRES_HOST')

    conn = psycopg2.connect(
        dbname=db,
        user=user,
        password=password,
        host=host
    )
    return conn

def query_to_dataframe(query, conn):
    return pd.read_sql_query(query, conn)

def main():
    conn = connect_db()

    queries = {
        "Películas mejor calificadas de la última década": """
            SELECT tb.primarytitle, tr.averagerating, tb.startyear
            FROM title_ratings tr
            JOIN title_basics tb ON tr.tconst = tb.tconst
            WHERE tb.startyear >= extract(year from now()) - 10
            ORDER BY tr.averagerating DESC
            LIMIT 10;
        """,
        "Géneros más populares a lo largo de los años": """
            SELECT UNNEST(genres) as genre, COUNT(*) as count
            FROM title_basics
            GROUP BY genre
            ORDER BY count DESC;
        """,
        "Directores más prolíficos y exitosos": """
            SELECT nb.primaryname, COUNT(*) as movie_count, AVG(tr.averagerating) as avg_rating
            FROM title_principals tp
            JOIN name_basics nb ON tp.nconst = nb.nconst
            JOIN title_ratings tr ON tp.tconst = tr.tconst
            WHERE tp.category = 'director'
            GROUP BY nb.primaryname
            ORDER BY movie_count DESC, avg_rating DESC
            LIMIT 10;
        """,
        "Relación entre calificaciones y duración de las películas": """
            SELECT tb.runtimeminutes, AVG(tr.averagerating) as avg_rating
            FROM title_basics tb
            JOIN title_ratings tr ON tb.tconst = tr.tconst
            WHERE tb.runtimeminutes IS NOT NULL
            GROUP BY tb.runtimeminutes
            ORDER BY tb.runtimeminutes;
        """
    }

    for description, query in queries.items():
        df = query_to_dataframe(query, conn)
        print(f"--- {description} ---")
        print(df)
        print("\n")

    conn.close()

if __name__ == "__main__":
    main()
