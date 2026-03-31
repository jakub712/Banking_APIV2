from pydantic import BaseModel

class CreateUserRequest(BaseModel):
    username: str
    first_name: str
    last_name: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str