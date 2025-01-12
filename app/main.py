from fastapi import FastAPI
from app.database import engine, Base
from app.routers import users, contacts
from fastapi.middleware.cors import CORSMiddleware
from slowapi.middleware import SlowAPIMiddleware
from app.rate_limiter import limiter

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rate limiting middleware
app.add_middleware(SlowAPIMiddleware)

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.state.limiter = limiter

app.include_router(users.router)
app.include_router(contacts.router)