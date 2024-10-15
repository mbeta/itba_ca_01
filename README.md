# itba_ca_01
ETL Foundations - Betania Martinez

# IMDb Movie Dataset

El dataset de IMDb contiene una amplia variedad de datos sobre películas, series de televisión y otros tipos de medios visuales. Este dataset ha sido recopilado de IMDb, una de las bases de datos de películas más grandes y detalladas del mundo. Contiene información sobre títulos, géneros, directores, actores, años de lanzamiento, calificaciones, reseñas y mucho más. Este dataset es ideal para analizar tendencias en la industria del entretenimiento, realizar análisis de audiencia, y explorar datos históricos de producciones cinematográficas y televisivas.


**Enlace al dataset:** [IMBb Movies Dataset](https://www.kaggle.com/datasets/ashirwadsangwan/imdb-dataset)

El dataset está compuesto por varias tablas, cada una con diferentes tipos de información. Algunas de las tablas principales son:

1. **title.basics**: Información básica de cada título, incluyendo el tipo de título (película, serie, etc.), el nombre del título, el año de lanzamiento, la duración y el género.
2. **title.crew**: Información sobre el equipo de producción de cada título, incluyendo directores y guionistas.
3. **title.principals**: Información sobre los actores y otros miembros principales del reparto.
4. **title.ratings**: Información sobre las calificaciones y votos de cada título.
5. **title.akas**: Información sobre los diferentes nombres y versiones de cada título en distintos idiomas y regiones.

### Pregunta 1: ¿Cuáles son las películas mejor calificadas de la última década?

**Objetivo**: Identificar las películas con las mejores calificaciones de los últimos diez años para entender las tendencias y preferencias de la audiencia reciente.

### Pregunta 2: ¿Qué géneros de películas han sido más populares a lo largo de los años?

**Objetivo**: Analizar la popularidad de los diferentes géneros de películas a lo largo del tiempo para identificar cambios en las preferencias de la audiencia y posibles oportunidades de producción.

### Pregunta 3: ¿Cuáles son los directores más prolíficos y exitosos según las calificaciones promedio de sus películas?

**Objetivo**: Determinar qué directores han dirigido más películas y tienen las calificaciones promedio más altas para evaluar el impacto de los directores en el éxito de las películas.

### Pregunta 4: ¿Cómo se relacionan las calificaciones de IMDb con la duración de las películas?

**Objetivo**: Explorar la relación entre la duración de las películas y sus calificaciones para entender si existe una longitud óptima que tiende a recibir mejores evaluaciones por parte de la audiencia.


## Conclusión

Con este análisis y las respuestas a estas preguntas, se pueden obtener valiosas perspectivas sobre la industria del cine y las preferencias del público, lo que puede guiar futuras decisiones de producción y distribución en el ámbito del entretenimiento.


---
## Solución 

### Descripción del Proyecto
Este proyecto se encarga de procesar y analizar un dataset de películas de IMDb. Incluye la carga de datos en una base de datos PostgreSQL y la ejecución de consultas SQL para obtener información valiosa.

**Dataset:** [IMBb Movies Dataset](https://www.kaggle.com/datasets/ashirwadsangwan/imdb-dataset)

Para resolver el trabajo se diseño un Multi-conteiner que consta de 3 contenedores:
1. Contenedor postgres_12.7: Contiene la Base de datos PostgresSQL Version 12.7
    Datos de conexion:
    - user: user
    - password: password
    - base de datos: imdb-movies
    - puerto: 5432
2. Contenedor data_loader: Ejecuta un Script de populacion de datos en la base de datos desde archivos.
3. Contenedor data_report: Ejecuta un Script para realizar consultas.

Estos contenedores se configuran y construyen a partir de docker-compose donde se setea configuracion de volumenes de datos, carpetas compartidas, variables de entorno, acciones de ejecucion de script ademas de condicionales de ejecucion.

En el Contenedor postgres_12.7, corren los servicio de base de datos postgre ademas que al iniciarse, se ejecuta un script de creacion de tablas necesarias (create_tables.sql), el script se encuenta dentro del directorio initdb.

En el Contenedor data_loader, se ejecutará un script de populacion de datos "populate_db.py", que luego de chequear que los archivos para migracion ya se encuentran disponibles (archivos .tsv) se conecta a la base de datos, en caso de no encontrarse aun disponible espera para reintentar. Una vez obtenida la conexion de la DB desactiva la integridad referencial para iniciar la carga de datos, para la cual se toma cada archivo y se divide en bloques y lo procesa (por motivos de performance y necesidades de memoria). Se debe tener en cuenta que los archivos de datos son de gran tamaño por lo que toma un tiempo considerable procesarlos.
Una vez terminada la carga de datos vuelve a activar la integridad referencial.

El Contenedor data_report ejecuta un script para las consultas SQL que responde las preguntas funcionales, para lo cual era necesario que la carga de informacion, por lo que se agrego un condicionar en el docker-compose que se ejecute cuando data_loader haya terminado. Ejecuta las queries y guarda el resultado de las mismas en un archivo log (/logs/report_queries.log).

Se incorpora un .sh para la ejecucion del docker-compose y posterior vista del reporte de consultas.

## Instrucciones 

### Requisitos Previos
Antes de ejecutar este proyecto, asegúratese debe contar con los siguientes requisitos instalados en el sistema:

1. **Docker**: Docker es una plataforma que permite desarrollar, enviar y ejecutar aplicaciones dentro de contenedores.
   - [Instalar Docker](https://docs.docker.com/get-docker/)

2. **Docker Compose**: Docker Compose es una herramienta para definir y ejecutar aplicaciones Docker de múltiples contenedores.
   - [Instalar Docker Compose](https://docs.docker.com/compose/install/)

### Paso a Paso

1. Clonar este repositorio en un directorio a eleccion (Directorio RAIZ de ahora en mas)
2. Descargar archivos .tsv de:  [IMBb Movies Dataset](https://www.kaggle.com/datasets/ashirwadsangwan/imdb-dataset)
2. Guardarlos dentro la carpeta "files" del directorio raiz.
3. Ejecuta el script run_end2end.sh
    En windows puede utilizar Cygwin
    - Vaya al directorio Raiz
    - Ejecute: chmod +x run_end2end.sh
    - Ejecute: ./run_end2end.sh


