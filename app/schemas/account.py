from pydantic import BaseModel

class CreateAccountRequest(BaseModel):
    account_type: str
    

class AccountResponse(BaseModel):
    id: int
    balance_pence: int
    account_type: str