FROM python:3.7-slim

WORKDIR /app

COPY report_queries.py .

# Instalar las dependencias
RUN pip install psycopg2-binary pandas

CMD ["python", "/report_queries.py"]
