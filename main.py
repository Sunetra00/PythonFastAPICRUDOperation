# from fastapi import FastAPI, Depends, HTTPException
# from typing import List
# from sqlalchemy.exc import IntegrityError
# from Schemas import UserCreateSchema, UserSchema  # Pydantic schemas
from database import Base, SessionLocal, engine
# from models import Users
# from sqlalchemy.orm import Session
# from pydantic import BaseModel
# #from fastapi.responses import JSONResponse 
# from typing import Optional
# from database import get_db  # Function to get database session
import logging
from fastapi import FastAPI
from routes.user_routes import router as user_router  # Import user routes


# Configure logging for debugging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create tables
Base.metadata.create_all(bind=engine)

#app = FastAPI()
app = FastAPI(
    title="My FastAPI App",
    description="An organized FastAPI app with routing separation",
    version="1.0.0"
)

# Include the user routes
app.include_router(user_router)



