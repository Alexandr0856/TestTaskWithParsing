CREATE TABLE countries (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    population BIGINT NOT NULL,
    region VARCHAR(100) NOT NULL
);
