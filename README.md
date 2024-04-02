# NEPSE Stock Portfolio Tracker

Stock Portfolio Tracker is a portfolio tracking web tool designed for NEPSE that provides summary of the overall gains and loss using [Chart.js](https://www.chartjs.org) library after uploading the Meroshare transactions csv file. Stock Portfoilo Tracker gets live stock day prices data from [NepaliPaisa](https://www.nepalipaisa.com/api/GetTodaySharePrice) and stores in SQLite database and provides day to day gains/losses as well.
## Features
- Real stock prices updates from NepaliPaisa API.
- Upload Meroshare transactions csv file and get realtime portfolio summary.
- Sector and instrument wise distributions with charts.
- Company wise transactions summary.
- Search for specific company information.
- Update personal credentials anytime.
  
## Requirements
Python 3.8+
- [FastAPI](https://fastapi.tiangolo.com/) web framework
- Uvicorn ASGI web server
- Starllete for rendering templates
- Pydantic for data parts

SQLite3
  
## Getting started
- Download zip or clone this project and open the project folder in IDE.
- Install all the requirements:
```bash 
pip install -r requirements.txt
```

## Setup database
- Download [sqlite-tools-win-x64](https://www.sqlite.org/download.html) precompiled binaries from Windows section.
- Extract and rename the folder `sqlite3`
- Move to path `C:\sqlite3` and also setup environment variable path 
- Open project folder and navigate inside `\db` folder
- `scripts.sql` contains SQL query to create schemas.
- Create database using command: 
 ```
 sqlite3 database.db '.read scripts.sql'
 ```
Above command will create `database.db` file with necessary schemas.  

## Run the server
- Open the project folder and run this command in powershell/cmd:
```powershell
python -m uvicorn main:app --reload

INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [4296] using WatchFiles
INFO:     Started server process [18944]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```
- Now go to `http://127.0.0.1:8000` in your browser, you will see following page:

![Screenshot 2024-04-02 134711](https://github.com/bixash/NEPSE-Stock-Portfolio-Tracker/assets/83506059/430bbb5b-f796-44e0-b3c2-42be72ecf27b)
- Signup and navigate to `resources\static\uploads\example.csv` file to upload the transactions file. To generate your portfolio summary, download [Meroshare](https://meroshare.cdsc.com.np) transactions csv file and add unit price for each transactions as `example.csv`.  
  
- After uploading you will see following portfolio:
  
  ![Screenshot 2024-04-02 141012](https://github.com/bixash/NEPSE-Stock-Portfolio-Tracker/assets/83506059/1c699f3c-1088-4a62-b3de-ee1c420ab4bb)
  
## Contributors
- [Bikash Shrestha](https://github.com/bixash)  
- [Ashok Kumar Pant](https://github.com/ashokpant)

