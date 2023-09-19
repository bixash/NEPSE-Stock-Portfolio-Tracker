 CREATE TABLE IF NOT EXISTS user ( 
    id INTEGER NOT NULL, 
    username VARCHAR(50),
    email VARCHAR(150), 
    password VARCHAR(150), 
    PRIMARY KEY (id), 
    UNIQUE (email)
    );

CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER NOT NULL, 
    scrip VARCHAR(225) NOT NULL,
    transaction_date DATE NOT NULL, 
    credit_quantity INTEGER NOT NULL, 
    debit_quantity INTEGER NOT NULL,
    balance_after_transaction INTEGER NOT NULL,
    history_description VARCHAR(225), 
    unit_price FLOAT NOT NULL,
    uid INTEGER NOT NULL, 
    FOREIGN KEY(uid) REFERENCES user(id), 
    FOREIGN KEY(scrip) REFERENCES stock(scrip), 
    PRIMARY KEY (id)
    );


CREATE TABLE IF NOT EXISTS company (
    scrip VARCHAR(225) NOT NULL,
    company_name VARCHAR(225) NOT NULL,
    status VARCHAR(225) NOT NULL,
    sector VARCHAR(225) NOT NULL,
    instrument VARCHAR(225) NOT NULL,
    email VARCHAR(225) NOT NULL,
    url VARCHAR(225),
    PRIMARY KEY (scrip)
    );

CREATE TABLE IF NOT EXISTS stock(
    scrip VARCHAR(255) NOT NULL,
    previous_closing FLOAT NOT NULL,
    trade_date DATE NOT NULL,
    closing_price FLOAT NOT NULL,
    difference_rs FLOAT NOT NULL ,
    percent_change FLOAT NOT NULL,
    PRIMARY KEY (scrip)
    );