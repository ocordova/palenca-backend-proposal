from pydantic import BaseModel


class LoginUser(BaseModel):
    user_name: str
    password: str


class LoginBody(BaseModel):
    user: LoginUser
