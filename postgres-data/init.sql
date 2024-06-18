CREATE TABLE IF NOT EXISTS items (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

CREATE TABLE submission (
    id SERIAL PRIMARY KEY,
    started TIMESTAMP,
    status VARCHAR(20),
    filename VARCHAR(200),
    grade VARCHAR(10),
    comments TEXT,
    errors TEXT
);
