from pydantic import BaseModel

class SWallet(BaseModel):
    amount: float
    wallet_uuid: str


class SOperationRequest(BaseModel):
    operation_type: str
    amount: float


class SCreateWalletRequest(BaseModel):
    wallet_uuid: str
    initial_balance: float = 0.0


class SBalanceResponse(BaseModel):
    balance: float
