from portfoliotracker.entities.company import Company
from portfoliotracker.entities.api_req_res import BaseResponse
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


    def get_company_info(self, scrip: str) -> BaseResponse:
        try:
            result = self.company_repo.retrieve_companyInfo_by_scrip(scrip)
            company_info = Company(scrip = result[0], company_name= result[1], status = result[2], sector= result[3], instrument=result[4], email = result[5], url = result[6])
            return BaseResponse(error=False, success=True, msg="success", result = company_info)
        except Exception as e:
                return BaseResponse(error=True, success=False, msg=str(e))

    def get_company_info_limit(self, limit: int) -> BaseResponse:
        try:
            result = self.company_repo.retrieve_companyInfo_all_limit(limit)
            infoList = []
            for item in result:
                company_info = dict(scrip = item[0], company_name= item[1], status = item[2], sector= item[3], instrument=item[4], email = item[5], url = item[6])
                infoList.append(company_info)
            return BaseResponse(error=False, success=True, msg="success", result=infoList)
        except Exception as e:
            return BaseResponse(error=True, success=False, msg=str(e))
    
    def company_like(self, scrip: str) -> BaseResponse:
        try:
            result = self.company_repo.get_company_like(scrip)
            return BaseResponse(error=False, success=True, msg="success", result= result)
        except Exception as e:
            return BaseResponse(error=True, success=False, msg=str(e))
    
    def get_status_sector_instrument(self, scripSymbol: list) ->BaseResponse:
        try:
            resultList =[]
            for scrip in scripSymbol:
                result = self.company_repo.select_status_sector_instrument(scrip)
                resultList.append(result)
            return BaseResponse(error=False, success=True, msg="success", result= resultList)
        except Exception as e:
            return BaseResponse(error=True, success=False, msg=str(e))
    
    def get_all_sectors(self):
        try:
            result = self.company_repo.select_all_distinct_sector()
            return BaseResponse(error=False, success=True, msg="success", result= result)
        except Exception as e:
            return BaseResponse(error=True, success=False, msg=str(e))
        
    def get_all_status(self):
        try:
            result = self.company_repo.select_all_distinct_status()
            return BaseResponse(error=False, success=True, msg="success", result= result)
        except Exception as e:
            return BaseResponse(error=True, success=False, msg=str(e))
        
    def get_all_instrument(self):
        try: 
            result = self.company_repo.select_all_distinct_instrument()
            return BaseResponse(error=False, success=True, msg="success", result= result)
        except Exception as e:
            return BaseResponse(error=True, success=False, msg=str(e))