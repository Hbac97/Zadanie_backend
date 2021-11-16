FROM postgres:9.6
ENV POSTGRES_PASSWORD=test123
ENV POSTGRES_USER=postgres
ENV POSTGRES_DB=database
COPY create_table.sql /docker-entrypoint-initdb.d/
