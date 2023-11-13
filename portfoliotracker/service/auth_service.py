"""
-- Created by: Ashok Kumar Pant
-- Created on: 7/18/23
"""
from portfoliotracker.entities import AuthResponse, BaseResponse, User
from portfoliotracker.repo.auth_repo import AuthRepo
from portfoliotracker.utils import utils
from portfoliotracker.entities.auth import SignupRequest, LoginRequest


class AuthService:

    def __init__(self, auth_repo: AuthRepo):
        self.auth_repo = auth_repo
        self.auth_session: dict[str, AuthResponse] = {} # don't understand this, why colon

    def login(self, email: str, password: str) -> BaseResponse:
        try:
            if self.validate_login(email, password):
                auth_response = self._login(email, password)
                return BaseResponse(error=False, success=True, result=auth_response)
        except Exception as e:
            return BaseResponse(error=True, success=False, msg=str(e))

    def _login(self, email: str, password: str) -> AuthResponse:
        user = self.auth_repo.get_user_by_email(email)
        if user is None:
            raise Exception("User not found")
        success = self.auth_repo.login(email, password)
        if not success:
            raise Exception("Invalid password")
        token = utils.generate_uuid()
        auth_response = AuthResponse(token=token, user=user)
        self.auth_session[token] = auth_response
        return auth_response

    def logout(self, token: str):
        if token in self.auth_session:
            del self.auth_session[token]
        else:
            raise Exception("Invalid token")

    def signup(self, signup_request: SignupRequest) -> BaseResponse:
        try:
            if self.validate_signup(signup_request):
                auth_response = self._signup(signup_request)
                return BaseResponse(error=False, success=True, result=auth_response)
        except Exception as e:
            return BaseResponse(error=True, success=False, msg=str(e))

    def _signup(self, signup_request: SignupRequest) -> User:

        existing_user = self.auth_repo.get_user_by_email(signup_request.email)
        if existing_user is not None:
            raise Exception("User already exists")
        success = self.auth_repo.save_user(signup_request)
        if not success:
            raise Exception("Could not save user")
        return signup_request

    def validate_signup(self, signup_request: SignupRequest) -> bool:

        if signup_request.email == "":
            raise Exception("Email required!")
        if signup_request.username == "":
            raise Exception("Username required!")
        if signup_request.password== "":
            raise Exception("Password required!")
        return True

    def validate_login(self, email, password) -> bool:

        if email == "":
            raise Exception("Email required!")
        if password== "":
            raise Exception("Password required!")
        return True
    