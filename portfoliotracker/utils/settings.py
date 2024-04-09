"""
-- Created by: Ashok Kumar Pant
-- Created on: 7/18/23
"""
import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    SQLITE_DB_PATH = os.getenv("SQLITE_DB_PATH")
    CSV_UPLOAD_PATH = os.getenv("CSV_UPLOAD_PATH")
    COMPANY_INFO_PATH = os.getenv("COMPANY_INFO_PATH")