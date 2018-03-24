CREATE DATABASE adega;

CREATE USER adega WITH PASSWORD 'adega';

ALTER ROLE myprojectuser SET client_encoding TO 'utf8';
ALTER ROLE myprojectuser SET default_transaction_isolation TO 'read committed';
ALTER ROLE myprojectuser SET timezone TO 'UTC-3';
GRANT ALL PRIVILEGES ON DATABASE adega TO adega;
