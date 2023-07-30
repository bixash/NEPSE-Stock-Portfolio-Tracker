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
    uid INTEGER NOT NULL, 
    FOREIGN KEY(uid) REFERENCES user(id), 
    FOREIGN KEY(scrip) REFERENCES stock(scrip), 
    PRIMARY KEY (id)
    );
