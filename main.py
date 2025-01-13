from api import api_auth, api_contacts
from fastapi import FastAPI, Depends 
from fastapi.middleware.cors import CORSMiddleware

from api import api_utils

# Ініціалізація FastAPI-додатку
app = FastAPI(title="Contacts API")

# Додавання CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Підключення роутерів
app.include_router(api_contacts.contact_router, prefix="/api")
app.include_router(api_utils.health_router, prefix="/api")
app.include_router(api_auth.router, prefix="/api")

# Точка входу для виконання в режимі розробки
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
