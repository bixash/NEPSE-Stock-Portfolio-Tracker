# stock-portfolio-tracker

Nepse Stock tracker using Python FastAPI

## Dependencies

```bash 
pip install -r requirements.txt
```

## To run the application

```bash
python -m uvicorn main:app --reload
```

## Setup database.db
 
```bash
cd db
sqlite3 database.db '.read scripts.sql'
```