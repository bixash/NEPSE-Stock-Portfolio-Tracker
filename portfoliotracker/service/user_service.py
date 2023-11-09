
from portfoliotracker.entities import BaseResponse, User
from portfoliotracker.repo.user_repo import UserRepo



class UserService:

    def __init__(self, user_repo: UserRepo):
        self.user_repo = user_repo
        

    def get_user(self, user_id: int) -> BaseResponse:
        try:
            user = self.user_repo.get_user_by_id(user_id)
            return BaseResponse(error=False, success=True, result=user)
        except Exception as e:
            return BaseResponse(error=True, success=False, msg=str(e))

    
    def update_user_username(self, username:str, user_id: int) -> BaseResponse:
        try:
            if self.user_repo.update_user_username(username, user_id):
                return BaseResponse(error=False, success=True, result=username)
        except Exception as e:
            return BaseResponse(error=True, success=False, msg=str(e))
        
    def update_user_email(self, email:str, user_id: int) -> BaseResponse:
        try:
            if self.user_repo.update_user_email(email, user_id):
                return BaseResponse(error=False, success=True, result=email)
        except Exception as e:
            return BaseResponse(error=True, success=False, msg=str(e))
        
    def update_user_password(self, password:str, user_id: int) -> BaseResponse:
        try:
            if self.user_repo.update_user_password(password, user_id):
                return BaseResponse(error=False, success=True, result=password)
        except Exception as e:
            return BaseResponse(error=True, success=False, msg=str(e))

    