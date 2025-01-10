from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError

from base_repo import BaseRepo
from database import async_session_maker
from app.wallets.models import Wallet


class WalletRepo(BaseRepo):
    model = Wallet

    @classmethod
    async def get_wallet(cls, wallet_uuid: str):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(uuid=wallet_uuid)
            result = await session.execute(query)
            return result.scalars().first()

    # @classmethod
    # async def update_balance(cls, wallet_uuid: str, amount: float, operation_type: str):
    #     async with async_session_maker() as session:
    #         try:
    #             wallet = await cls.get_wallet(wallet_uuid)
    #             if not wallet:
    #                 raise HTTPException(status_code=404, detail="Wallet not found")
    #
    #             if operation_type == 'DEPOSIT':
    #                 new_balance = float(wallet.balance) + amount
    #             elif operation_type == 'WITHDRAW':
    #                 new_balance = float(wallet.balance) - amount
    #             else:
    #                 raise HTTPException(status_code=404, detail="Invalid operation_type")
    #
    #             if new_balance < 0:
    #                 raise HTTPException(status_code=400, detail="Insufficient funds")
    #
    #             wallet.balance = new_balance
    #             session.add(wallet)
    #             await session.commit()
    #             return {"message": f"{operation_type} successful"}
    #         except Exception as e:
    #             return JSONResponse(content={"error": str(e)}, status_code=500)

    @classmethod
    async def update_balance(cls, wallet_uuid: str, amount: float, operation_type: str):
        async with async_session_maker() as session:
            try:
                async with session.begin():
                    query = (
                        select(Wallet)
                        .filter(Wallet.uuid == wallet_uuid)
                        .with_for_update(nowait=True)
                    )
                    result = await session.execute(query)
                    wallet = result.scalar_one_or_none()

                    if not wallet:
                        raise HTTPException(status_code=404, detail="Wallet not found")

                    if operation_type == 'DEPOSIT':
                        new_balance = float(wallet.balance) + amount
                    elif operation_type == 'WITHDRAW':
                        new_balance = float(wallet.balance) - amount
                    else:
                        raise HTTPException(status_code=404, detail="Invalid operation_type")

                    if new_balance < 0:
                        raise HTTPException(status_code=400, detail="Insufficient funds")

                    stmt = (
                        update(Wallet)
                        .where(Wallet.uuid == wallet_uuid)
                        .values(balance=new_balance)
                    )
                    await session.execute(stmt)

                    await session.commit()
                    return {"message": f"{operation_type} successful"}
            except IntegrityError as e:
                return JSONResponse(content={"error": str(e)}, status_code=500)
            except Exception as e:
                return JSONResponse(content={"error": str(e)}, status_code=500)

    @classmethod
    async def create_wallet(cls, wallet_uuid: str, balance: float):
        async with async_session_maker() as session:
            wallet = Wallet(uuid=wallet_uuid, balance=balance)
            session.add(wallet)
            await session.commit()
            return {"uuid": wallet.uuid, "initial_balance": wallet.balance}

    @classmethod
    async def delete_wallet(cls, wallet_uuid: str):
        async with async_session_maker() as session:
            wallet = await cls.get_wallet(wallet_uuid)
            if not wallet:
                raise HTTPException(status_code=404, detail="Wallet not found")
            await session.delete(wallet)
            await session.commit()
            return {"message": f"Wallet {wallet_uuid} deleted successfully"}
