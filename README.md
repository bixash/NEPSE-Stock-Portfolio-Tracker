# NEPSE Stock Portfolio Tracker

Stock Portfolio Tracker is a portfolio tracking web tool designed for NEPSE that provides summary of the overall gains and loss using [Chart.js](https://www.chartjs.org) library after uploading the Meroshare transactions csv file. Stock Portfoilo Tracker gets live stock day prices data from [NepaliPaisa](https://www.nepalipaisa.com/api/GetTodaySharePrice) and stores in SQLite database and provides day to day gains/losses as well.

## Features
- User can upload their Meroshare transactions csv file 
## Dependencies
```bash 
pip install -r requirements.txt
```

## Setup database
 
```bash
cd db
sqlite3 database.db '.read scripts.sql'
```
## Run the application
```powershell
python -m uvicorn main:app --reload
```

For accurate information, download Meroshare transactions csv file and add unit price for each teransactions. 
```
S.N,Scrip,Transaction Date,Credit Quantity,Debit Quantity,Balance After Transaction,History Description,Unit Price
```

