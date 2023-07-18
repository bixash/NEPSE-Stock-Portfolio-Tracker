user_schema = """ CREATE TABLE user ( 
    id INTEGER NOT NULL, 
    username VARCHAR(50),
    email VARCHAR(150), 
    password VARCHAR(150), 
    PRIMARY KEY (id), 
    UNIQUE (email)
    );
"""

transactions_schema = """ CREATE TABLE transactions (
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
 """

stock_schema = """ CREATE TABLE stock(
    scrip VARCHAR(255) NOT NULL, 
    company_name VARCHAR(255) NOT NULL,
    previous_closing INTEGER NOT NULL, 
    trade_date DATE NOT NULL,
    closing_price INTEGER NOT NULL, 
    PRIMARY KEY (scrip)
    );
"""

insert_history = """ INSERT INTO transactions(
    scrip, transaction_date, 
    credit_quantity, 
    debit_quantity, balance_after_transaction, history_description, uid)
    values(?,?,?,?,?,?,?);
"""

fetch_scrip_balance_price = """ SELECT stock.scrip, balance_after_transaction, closing_price 
    FROM stock INNER JOIN transactions ON transactions.scrip = stock.scrip 
    WHERE transactions.scrip = ? and uid = ? ORDER BY transaction_date desc limit 1;
"""

fetch_history = """ SELECT 
    scrip, transaction_date, 
    credit_quantity, debit_quantity, balance_after_transaction, 
    history_description from transactions where uid = ?;
"""

insert_stockPrices = """ INSERT INTO stock (scrip, company_name, previous_closing,
    trade_date, closing_price) values(?,?,?,?,?);

"""

update_stockPrices = """ UPDATE stock 
    SET previous_closing = ?, trade_date = ?, closing_price = ? WHERE scrip = ?
"""