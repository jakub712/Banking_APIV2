from pydantic import BaseModel, Field

class Transfer_Request(BaseModel):
    amount_pence: int = Field(gt=0)

class Deposit_Request(BaseModel):
    amount_pence: int = Field(gt=0)

class Withdraw_Request(BaseModel):
    amount_pence: int = Field(gt=0)