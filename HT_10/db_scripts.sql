CREATE TABLE IF NOT EXISTS atm (
    id                  INTEGER             PRIMARY KEY AUTOINCREMENT,
    created_at          DATETIME            DEFAULT CURRENT_TIMESTAMP,
    updated_at          DATETIME            DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS atm_balance (
    id                  INTEGER             PRIMARY KEY AUTOINCREMENT,
    atm_id              INTEGER             NOT NULL,
    balance             INTEGER             DEFAULT 0,
    FOREIGN KEY         (atm_id)            REFERENCES  atm(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS atm_currency (
    id                  INTEGER             PRIMARY KEY AUTOINCREMENT,
    atm_id              INTEGER             NOT NULL,
    denomination        INTEGER             NOT NULL,               -- # 10, 20, 50, 100, 200, 500, 1000
    quantity            INTEGER             NOT NULL DEFAULT 1,     -- количество купюр
    FOREIGN KEY         (atm_id)            REFERENCES atm(id) ON DELETE CASCADE,
    UNIQUE              (atm_id, denomination)
);

CREATE TABLE IF NOT EXISTS users (
    id                  INTEGER             PRIMARY KEY AUTOINCREMENT,
    username            TEXT                NOT NULL UNIQUE,
    password            TEXT                NOT NULL,
    role                TEXT                NOT NULL DEFAULT 'user', -- роль пользователя: 'user' или 'collector'
    balance             FLOAT               DEFAULT 0,
    created_at          DATETIME            DEFAULT CURRENT_TIMESTAMP,
    updated_at          DATETIME            DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS transactions (
    id                  INTEGER             PRIMARY KEY AUTOINCREMENT,
    user_id             INTEGER             NOT NULL,
    type_transaction    TEXT                NOT NULL,                   -- тип транзакции: 'deposit' или 'withdrawal'
    amount              INTEGER             NOT NULL,                   -- сумма транзакции
    created_at          DATETIME            DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY         (user_id)           REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE              (id, user_id)

);

-- ТРИГЕРЫ

-- Создание триггера для обновления updated_at в таблице atm при изменении баланса банкомата
CREATE TRIGGER IF NOT EXISTS update_atm_updated_at
    AFTER UPDATE
    ON atm_balance
BEGIN
    UPDATE atm
    SET updated_at = CURRENT_TIMESTAMP
    WHERE id = NEW.atm_id;
END;

-- Триггер для обновляющей таблицы atm updated_at при изменении данных
CREATE TRIGGER IF NOT EXISTS update_atm_balance_updated_at
AFTER UPDATE ON atm
BEGIN
    UPDATE atm
    SET updated_at = CURRENT_TIMESTAMP
    WHERE id = NEW.id;
END;

-- Триггер для обновляющей таблицы atm updated_at при создании atm_currency данных
CREATE TRIGGER IF NOT EXISTS update_atm_updated_at_insert
AFTER INSERT ON atm_currency
FOR EACH ROW
BEGIN
    UPDATE atm
    SET updated_at = CURRENT_TIMESTAMP
    WHERE atm.id = NEW.atm_id;
END;

-- Триггер для обновляющей таблицы atm updated_at при обновлении atm_currency данных
CREATE TRIGGER IF NOT EXISTS update_atm_updated_at_update
AFTER UPDATE ON atm_currency
FOR EACH ROW
BEGIN
    UPDATE atm
    SET updated_at = CURRENT_TIMESTAMP
    WHERE atm.id = NEW.atm_id;
END;

-- Триггер для таблицы users, устанавливающей created_at при создании данных
CREATE TRIGGER IF NOT EXISTS set_user_created_at
AFTER INSERT ON users
BEGIN
    UPDATE users
    SET created_at = CURRENT_TIMESTAMP
    WHERE id = NEW.id;
END;

-- Триггер для таблицы users, обновляющей updated_at при изменении данных
CREATE TRIGGER IF NOT EXISTS update_users_updated_at
AFTER UPDATE ON users
BEGIN
    UPDATE users
    SET updated_at = CURRENT_TIMESTAMP
    WHERE id = NEW.id;
END;