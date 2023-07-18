"""
-- Created by: Ashok Kumar Pant
-- Created on: 7/18/23
"""
import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    KITTA_API_KEY = os.getenv("KITTA_API_KEY")
    SQLITE_DB_PATH = os.getenv("SQLITE_DB_PATH")
