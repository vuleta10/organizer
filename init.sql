CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,

    username VARCHAR(100)
    NOT NULL
    UNIQUE,

    password VARCHAR(255)
    NOT NULL
);

CREATE TABLE IF NOT EXISTS tasks (
    id SERIAL PRIMARY KEY,

    user_id INTEGER NOT NULL,

    datum DATE NOT NULL,

    task TEXT NOT NULL,

    done BOOLEAN NOT NULL
    DEFAULT FALSE,

    CONSTRAINT fk_task_user
    FOREIGN KEY (user_id)
    REFERENCES users(id)
);
