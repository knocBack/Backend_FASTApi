from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import user_router,product_router,order_router,admin_router
from . import models
from .database import engine

# creates tables
models.Base.metadata.create_all(bind=engine)

# runs app
app = FastAPI()

# enabling CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# including other routers
app.include_router(user_router.router)
app.include_router(product_router.router)
app.include_router(order_router.router)
app.include_router(admin_router.router)

# main()
@app.get("/")
def main():
    return {"message": "Hello World! Working!"}
