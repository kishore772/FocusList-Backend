from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from routers import task_router, user_router
from configuration.database import engine, Base

# Create the tables in the database asynchronously
async def create_tables():
    async with engine.begin() as conn:
        # Use run_sync to create the tables in the async engine
        await conn.run_sync(Base.metadata.create_all)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (POST, GET, etc.)
    allow_headers=["*"],  # Allow all headers (authorization, etc.)
)

# Your routes go here
# Example route
@app.get("/")
async def root():
    return {"message": "Hello World"}

# Run table creation on startup
@app.on_event("startup")
async def on_startup():
    await create_tables()

# Include the routers
app.include_router(task_router.router)

app.include_router(user_router.router)
