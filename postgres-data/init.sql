CREATE TABLE submission (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(100) NOT NULL,
    started TIMESTAMP NOT NULL,
    status VARCHAR(20) NOT NULL,
    filename VARCHAR(200) NOT NULL,
    grade VARCHAR(10),
    comments TEXT,
    errors TEXT
);
