from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import user_router,product_router,order_router,admin_router
from . import models
from .database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router.router)
app.include_router(product_router.router)
app.include_router(order_router.router)
app.include_router(admin_router.router)

@app.get("/")
def main():
    return {"message": "Hello World! Working!"}
