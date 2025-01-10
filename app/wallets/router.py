from fastapi import APIRouter

from app.wallets.repo import WalletRepo
from app.wallets.shemas import SBalanceResponse, SOperationRequest, SWallet, SCreateWalletRequest

router = APIRouter(
    tags=["Кошелек"],
)


@router.get('/api/v1/wallets')
async def get_wallets():
    return await WalletRepo.get_all()


@router.post("/api/v1/wallets/{wallet_uuid}/operation")
async def do_operation(wallet_uuid: str, operation_request: SOperationRequest):
    return await WalletRepo.update_balance(wallet_uuid, operation_request.amount, operation_request.operation_type)


@router.post('/api/v1/wallets/create_wallet')
async def create_wallet(wallet: SCreateWalletRequest):
    return await WalletRepo.create_wallet(wallet.wallet_uuid, wallet.initial_balance)


@router.get('/api/v1/wallets/{wallet_uuid}')
async def get_wallet(wallet_uuid: str):
    wallet = await WalletRepo.get_wallet(wallet_uuid)
    return SBalanceResponse(balance=float(wallet.balance))


@router.delete('/api/v1/wallets/{wallet_uuid}')
async def delete_wallet(wallet_uuid: str):
    return await WalletRepo.delete_wallet(wallet_uuid)
