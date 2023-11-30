CREATE TABLE IF NOT EXISTS users (
    id                INTEGER             PRIMARY KEY AUTOINCREMENT,
    name              TEXT                NOT NULL UNIQUE,
    password          TEXT                NOT NULL,
    role              TEXT                NOT NULL,
    created_at        DATETIME            DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS library_cards (
    id                INTEGER             PRIMARY KEY AUTOINCREMENT,
    status            TEXT                NOT NULL,         -- взял, вернул
    book_id           INTEGER             NOT NULL,
    user_id           INTEGER             NOT NULL,
    created_at        DATETIME            DEFAULT CURRENT_TIMESTAMP,
    updated_at        DATETIME            DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY       (book_id)           REFERENCES books(id) ON DELETE CASCADE,
    FOREIGN KEY       (user_id)           REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE            (book_id, user_id)
);


CREATE TABLE IF NOT EXISTS categories (
    id                INTEGER             PRIMARY KEY AUTOINCREMENT,
    title             TEXT                NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS books (
    id                INTEGER             PRIMARY KEY AUTOINCREMENT,
    title             TEXT                NOT NULL,
    author            TEXT                NOT NULL,
    category_id       INTEGER             NOT NULL,
    UNIQUE            (title, author, category_id),
    FOREIGN KEY       (category_id)       REFERENCES categories(id) ON DELETE CASCADE
);


CREATE TABLE IF NOT EXISTS assignments (
    id                INTEGER             PRIMARY KEY AUTOINCREMENT,
    teacher_id        INTEGER             NOT NULL,
    title             TEXT                NOT NULL,
    description       TEXT                NOT NULL,
    created_at        DATETIME            DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS assignment_submissions (
    id                INTEGER             PRIMARY KEY AUTOINCREMENT,
    assignment_id     INTEGER             NOT NULL,
    student_id        INTEGER             NOT NULL,
    created_at        DATETIME            DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS marks (
    id                INTEGER             PRIMARY KEY AUTOINCREMENT,
    subject           TEXT                NOT NULL,
    student_id        INTEGER             NOT NULL,
    mark              INTEGER             NOT NULL
);