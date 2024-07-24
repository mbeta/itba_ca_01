#!/bin/bash

# Construir y ejecutar los contenedores
echo "Construyendo y ejecutando contenedores..."
docker-compose up --build -d

# Esperar a que el contenedor de carga de datos termine
echo "Esperando que el contenedor de carga de datos termine..."
while [ "$(docker inspect -f '{{.State.Running}}' data_loader)" == "true" ]; do
    sleep 5
done

# Mostrar los logs del contenedor de reportes
echo "Mostrando logs del contenedor de reportes..."
while [ "$(docker inspect -f '{{.State.Running}}' data_report)" == "true" ]; do
    sleep 5
done
cat ./logs/report_queries.log

echo "Proceso End-to-End completado."
