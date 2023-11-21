from portfoliotracker.repo.db import DBConnection
from portfoliotracker.entities.company import Company

class CompanyRepo:
    def __init__(self, db: DBConnection):
        self.db = db

    def insert_company_info(self, company: Company) -> bool:
        cur = self.db.get_connection()
        con = self.db._commit()
        cur.execute("INSERT INTO company (scrip, company_name, status, sector, instrument, email, url) values(?, ?, ?, ?, ?, ?, ?)",(company.scrip, company.company_name, company.status, company.sector, company.instrument, company.email, company.url ))
        con.commit()
        return True
    
    def retrieve_companyInfo_all_limit(self, limit: int) -> list:
        cur = self.db.get_connection()
        con = self.db._commit()
        cur.execute("SELECT scrip, company_name, status, sector, instrument, email, url FROM company limit ?", (limit, ))
        return cur.fetchall()
    
    def retrieve_companyInfo_by_scrip(self, scrip: str) -> bool:
        cur = self.db.get_connection()
        con = self.db._commit()
        cur.execute("SELECT scrip, company_name, status, sector, instrument, email, url FROM company WHERE scrip = ?", (scrip,))
        return cur.fetchone()
    
    def get_company_like(self, scrip:str):
        cur = self.db.get_connection()
        con = self.db._commit()
        cur.execute("SELECT scrip, company_name FROM company WHERE scrip LIKE ? or company_name LIKE ?  limit 8",(scrip, scrip, ))
        return cur.fetchall()
    
    def select_status_sector_instrument(self, scrip: str) -> bool:
        cur = self.db.get_connection()
        con = self.db._commit()
        cur.execute("SELECT scrip, status, sector, instrument FROM company WHERE scrip = ?", (scrip,))
        return cur.fetchone()
    
    def select_all_distinct_status(self):
        cur = self.db.get_connection()
        con = self.db._commit()
        cur.execute("SELECT DISTINCT status FROM company")
        return cur.fetchall()
    
        
    def select_all_distinct_sector(self):
        cur = self.db.get_connection()
        con = self.db._commit()
        cur.execute("SELECT DISTINCT sector FROM company")
        return cur.fetchall()
    
    def select_all_distinct_instrument(self):
        cur = self.db.get_connection()
        con = self.db._commit()
        cur.execute("SELECT DISTINCT instrument FROM company")
        return cur.fetchall()
    
    def select_company_by_scrip(self, scrip: str):
        cur = self.db.get_connection()
        con = self.db._commit()
        cur.execute("SELECT scrip, sector, instrument, status FROM company WHERE scrip = ?", (scrip, ))
        return cur.fetchall()