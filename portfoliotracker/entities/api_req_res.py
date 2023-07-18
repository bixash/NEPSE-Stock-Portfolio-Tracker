"""
-- Created by: Ashok Kumar Pant
-- Created on: 7/18/23
"""
from typing import Optional, Any

from pydantic import BaseModel


class BaseResponse(BaseModel):
    error: bool = False
    msg: Optional[str] = None
    success: bool = False
    result: Optional[Any] = None
