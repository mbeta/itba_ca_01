FROM python:3.7-slim

RUN pip install pandas psycopg2-binary

COPY populate_db.py /populate_db.py
COPY files/critic_reviews.csv /critic_reviews.csv
COPY files/movies.csv /movies.csv
COPY files/user_reviews.csv /user_reviews.csv

CMD ["python", "/populate_db.py"]
