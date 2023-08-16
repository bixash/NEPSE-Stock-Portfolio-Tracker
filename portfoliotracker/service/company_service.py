from portfoliotracker.entities.company import Company
from portfoliotracker.repo.company_repo import CompanyRepo
from portfoliotracker.utils import Settings
import csv
import os


class CompanyService:

    def __init__(self, company_repo : CompanyRepo):
        self.company_repo = company_repo
        self.file_location = f"{os.path.join(Settings.CSV_UPLOAD_PATH)}/company-info.csv"
        
    def upload_company_csv(self):
        with open(self.file_location, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                company = Company(scrip= row['Symbol'], company_name = row['Name'], status = row['Status'], sector = row['Sector'], instrument= row['Instrument'], email = row['Email'], url = row['Website'])
                if not self.company_repo.insert_company_info(company):
                    return ("Can't insert company info!")
        return "Uploaded company info! "  
