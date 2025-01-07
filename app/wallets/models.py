from sqlalchemy import Column, String, Numeric
from database import Base


class Wallet(Base):
    __tablename__ = 'wallets'

    uuid = Column(String, primary_key=True, nullable=False)
    balance = Column(Numeric(precision=10, scale=2), nullable=False, default=0)
