import os
import time  
import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
import csv
# from psycopg2 import sql

# Conectar a la base de datos
def connect_db():
    while True:
        try:
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
            print("Conectado a Base de Datos")
            return conn
        except psycopg2.OperationalError:
            print("Esperando que la base de datos este lista...")
            time.sleep(5)

def set_constraints(conn, enable=True):
    cur = conn.cursor()
    action = 'ENABLE' if enable else 'DISABLE'
    queries = [
        f"ALTER TABLE title_basics {action} TRIGGER ALL;",
        f"ALTER TABLE name_basics {action} TRIGGER ALL;",
        f"ALTER TABLE title_akas {action} TRIGGER ALL;",
        f"ALTER TABLE title_principals {action} TRIGGER ALL;",
        f"ALTER TABLE title_ratings {action} TRIGGER ALL;"
    ]
    
    for query in queries:
        cur.execute(query)
    
    conn.commit()
    cur.close()

def transform_array_column(df, column_name):
    df[column_name] = df[column_name].apply(
        lambda x: "{" + ",".join(x.split(',')) + "}" if pd.notna(x) else None
    )


# Leer y cargar datos desde TSV a PostgreSQL
def load_tsv_to_db(file_path, table_name, columns, conn, array_columns=None):
    print(f"Inicia carga de datos del archivo: {file_path}, tabla: {table_name}")
    cur = conn.cursor()

    df = pd.read_csv(file_path, sep='\t', quotechar='"', quoting=3, dtype=str)
    df = df.replace({'\\N': None})  # Reemplazar '\N' con None
    df.columns = [col.lower() for col in df.columns]  # Convertir a minúsculas para que coincidan con los nombres en PostgreSQL

    if array_columns:
        for col in array_columns:
            transform_array_column(df, col)
   
    # Formatear los valores para la inserción masiva
    values = [tuple(x) for x in df.to_numpy()]

    # Generar la consulta de inserción masiva
    insert_query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES %s ON CONFLICT DO NOTHING"

    # Ejecutar la inserción masiva
    execute_values(cur, insert_query, values)

    # Confirmar la transacción
    conn.commit()

# Leer y cargar datos desde TSV a PostgreSQL
def load_tsv_to_db_in_chunks(file_path, table_name, columns, conn, array_columns=None, chunksize=10000):
    print(f"Inicia carga de datos del archivo: {file_path}, tabla: {table_name}")
    cur = conn.cursor()

    for chunk in pd.read_csv(file_path, sep='\t', quotechar='"', quoting=3, dtype=str, chunksize=chunksize):
        chunk = chunk.replace({'\\N': None})  # Reemplazar '\N' con None
        chunk.columns = [col.lower() for col in chunk.columns]  # Convertir a minúsculas para que coincidan con los nombres en PostgreSQL

        if array_columns:
            for col in array_columns:
                transform_array_column(chunk, col)

        # Formatear los valores para la inserción masiva
        values = [tuple(x) for x in chunk.to_numpy()]

        # Generar la consulta de inserción masiva
        insert_query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES %s ON CONFLICT DO NOTHING"

        # Ejecutar la inserción masiva
        execute_values(cur, insert_query, values)
        
        # Confirmar la transacción
        conn.commit()

    cur.close()



def wait_for_files(file_paths, timeout=60):
    print("Esperar hasta que los archivos estén disponibles.")
    start_time = time.time()
    while time.time() - start_time < timeout:
        all_files_exist = all(os.path.exists(file_path) for file_path in file_paths)
        if all_files_exist:
            return True
        time.sleep(5)  # Espera 5 segundos antes de volver a comprobar
    raise FileNotFoundError("No se encontraron todos los archivos dentro del tiempo de espera.")

def main():
    print("Se inicia carga de información.")
    
    # Rutas de archivos TSV
    file_paths = [
        '/files/title.basics.tsv',
        '/files/name.basics.tsv',
        '/files/title.akas.tsv',
        '/files/title.principals.tsv',
        '/files/title.ratings.tsv'
    ]

    # Esperar a que los archivos estén disponibles
    wait_for_files(file_paths)
    print("Todos los archivos disponibles.")
   
    # Conectar a la base de datos
    conn = connect_db()
    
    print("Desactivar restricciones de claves.")
    set_constraints(conn, enable=False)

    # Cargar datos en cada tabla
    # load_data_to_db('title_basics', '/files/title.basics.tsv', conn)
    # load_data_to_db('name_basics', '/files/name.basics.tsv', conn)
    # load_data_to_db('title_akas', '/files/title.akas.tsv', conn)
    # load_data_to_db('title_principals', '/files/title.principals.tsv', conn)
    # load_data_to_db('title_ratings', '/files/title.ratings.tsv', conn)
    
    
    try:
        # Cargar datos en cada tabla
        #load_tsv_to_db('/files/title.basics.tsv', 'title_basics', [
        load_tsv_to_db_in_chunks('/files/title.basics.tsv', 'title_basics', [
            'tconst', 'titletype', 'primarytitle', 'originaltitle', 'isadult',
            'startyear', 'endyear', 'runtimeminutes', 'genres'], conn, array_columns=['genres'])

        #load_tsv_to_db('/files/name.basics.tsv', 'name_basics', [
        load_tsv_to_db_in_chunks('/files/name.basics.tsv', 'name_basics', [
            'nconst', 'primaryname', 'birthyear', 'deathyear', 'primaryprofession',
            'knownfortitles'], conn, array_columns=['primaryprofession', 'knownfortitles'])

        #load_tsv_to_db('/files/title.akas.tsv', 'title_akas', [
        load_tsv_to_db_in_chunks('/files/title.akas.tsv', 'title_akas', [
            'titleid', 'ordering', 'title', 'region', 'language', 'types', 'attributes',
            'isoriginaltitle'], conn, array_columns=['types', 'attributes'])

        #load_tsv_to_db('/files/title.principals.tsv', 'title_principals', [
        load_tsv_to_db_in_chunks('/files/title.principals.tsv', 'title_principals', [
            'tconst', 'ordering', 'nconst', 'category', 'job', 'characters'], conn)

        #load_tsv_to_db('/files/title.ratings.tsv', 'title_ratings', [
        load_tsv_to_db_in_chunks('/files/title.ratings.tsv', 'title_ratings', [
            'tconst', 'averagerating', 'numvotes'], conn)
        
    except Exception as e:
        print(f"Error durante la carga de datos: {e}")
    
    finally:
        # Reactivar restricciones
        print("Reactivar restricciones de claves.")
        set_constraints(conn, enable=True)
        conn.close()
    

    # Cerrar la conexión
    conn.close()
    print("Proceso de carga de información completa.")

if __name__ == "__main__":
    main()