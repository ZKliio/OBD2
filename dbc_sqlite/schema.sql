DROP TABLE IF EXISTS car_models;
DROP TABLE IF EXISTS dbc_files;
DROP TABLE IF EXISTS messages;
DROP TABLE IF EXISTS signals;
DROP TABLE IF EXISTS transmitters;
DROP TABLE IF EXISTS signal_comments;
DROP TABLE IF EXISTS signal_values;

CREATE TABLE car_models (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE
);

CREATE TABLE dbc_files (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    car_model_id INTEGER,
    variant TEXT,
    FOREIGN KEY (car_model_id) REFERENCES car_models(id)
);

CREATE TABLE messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    message_id INTEGER,  -- actual CAN ID
    name TEXT,
    dlc INTEGER,
    sender TEXT,
    car_model_id INTEGER,
    dbc_id INTEGER,
    FOREIGN KEY (car_model_id) REFERENCES car_models(id),
    FOREIGN KEY (dbc_id) REFERENCES dbc_files(id)
);

CREATE TABLE signals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    message_id INTEGER,
    name TEXT,
    start_bit INTEGER,
    length INTEGER,
    byte_order TEXT,
    is_signed BOOLEAN,
    factor REAL,
    offset REAL,
    min REAL,
    max REAL,
    unit TEXT,
    receiver TEXT,
    FOREIGN KEY (message_id) REFERENCES messages(id)
);

CREATE TABLE transmitters (
    message_id INTEGER,
    transmitter TEXT,
    FOREIGN KEY (message_id) REFERENCES messages(id)
);

CREATE TABLE signal_comments (
    message_id INTEGER,
    signal_name TEXT,
    comment TEXT,
    FOREIGN KEY (message_id) REFERENCES messages(id)
);

CREATE TABLE signal_values (
    message_id INTEGER,
    signal_name TEXT,
    value INTEGER,
    meaning TEXT,
    FOREIGN KEY (message_id) REFERENCES messages(id)
);
