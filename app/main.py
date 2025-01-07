from fastapi import FastAPI, Request
from app.wallets.router import router as wallets_router

app = FastAPI()

app.include_router(wallets_router)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    response = await call_next(request)
    return response
