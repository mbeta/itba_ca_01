FROM python:3.7-slim

WORKDIR /app

COPY populate_db.py .
COPY files/ /files

#COPY files/critic_reviews.csv /critic_reviews.csv
#COPY files/movies.csv /movies.csv
#COPY files/user_reviews.csv /user_reviews.csv

# Instalar las dependencias
RUN pip install pandas psycopg2-binary

CMD ["python", "/populate_db.py"]
