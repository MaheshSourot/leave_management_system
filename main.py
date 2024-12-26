from fastapi import FastAPI
from database import Base, engine
# from routers import auth, leaves, analytics
from fastapi.middleware.cors import CORSMiddleware
from routers import auth,leaves,analytics

# Initialize app
app = FastAPI()

# Create tables
Base.metadata.create_all(bind=engine)

# Register routers
app.include_router(auth.router,prefix='/auth', tags=["Employee Registration and Login"])
app.include_router(leaves.router, prefix="/leaves", tags=["Employee Leave Management"])
app.include_router(analytics.router, prefix="/analytics", tags=["Leave Analysis"])


app.add_middleware(
    CORSMiddleware,
    allow_origins='*',
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
    
)
