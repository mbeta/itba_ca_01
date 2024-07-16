#!/bin/bash

PGPASSWORD=password psql -h localhost -U user -d soccer-movies -f create_tables.sql
