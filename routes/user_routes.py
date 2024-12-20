from fastapi import FastAPI,APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.exc import IntegrityError
from Schemas import UserCreateSchema, UserSchema  # Pydantic schemas
from database import Base, SessionLocal, engine
from models import Users
from sqlalchemy.orm import Session
from pydantic import BaseModel
#from fastapi.responses import JSONResponse 
from typing import Optional
from database import get_db  # Function to get database session

# Create a router instance
router = APIRouter(
    prefix="/users",  # Optional URL prefix for all routes in this router
    tags=["Users"]    # Group routes under the "Users" tag in Swagger
)

# Create a new user
@router.post("/", response_model=UserSchema)
def create_users(user: UserCreateSchema, db: Session = Depends(get_db)):
    """
    Create a new user.
    """
    new_user = Users(name=user.name, email=user.email, password=user.password)
    try:
        # Add user to the database
        db.add(new_user)
        db.commit()  # Commit the transaction
        db.refresh(new_user)  # Refresh to fetch generated ID
        return new_user

    except IntegrityError as e:  # Handle duplicate email error
        db.rollback()  # Rollback the transaction to avoid corruption
        status_code=400,
        raise HTTPException(
            status_code=400,
            detail="Email already exists. Please use a different email.")
       # logger.error(f"IntegrityError: {str(e)}")  # Log the error

        
        # For any other database error
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred while creating the user."
        )
    # try:
    #     db.add(new_user)     # Add to database session
    #     db.commit()          # Commit the transaction
    #     db.refresh(new_user) # Refresh to get the generated ID
    #     return new_user      # Return the created user
    # except IntegrityError:   # Catch duplicate email error
    #     db.rollback()        # Rollback the transaction
    #     raise HTTPException(
    #         status_code=400,
    #         detail="Email already exists. Please use a different email.")

    
# Route for fetching a user by ID
# Get all users
@router.get("/", response_model=List[UserSchema])
def get_users(db: Session = Depends(get_db)):
    return db.query(Users).all()


# READ user by id 
@router.get("/{user_id}", response_model=UserSchema)
def read_user(user_id: int, db: Session = Depends(get_db)):
    """
    Fetches a user by their ID.
    """
    user = db.query(Users).filter(Users.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


#put
@router.put("/{user_id}", response_model=UserSchema)
def update_user(user_id: int, user: UserSchema, db: Session = Depends(get_db)):
    # Retrieve the user from the database
    existing_user = db.query(Users).filter(Users.id == user_id).first()
    
    if not existing_user:
        # Raise an HTTPException if the user does not exist
        raise HTTPException(status_code=404, detail="User not found")
    
    # Update user details
    existing_user.name = user.name
    existing_user.email = user.email

    # Commit changes to the database
    db.commit()
    db.refresh(existing_user)  # Refresh to get the updated data

    return existing_user

#Delete
@router.delete("/{user_id}",response_model = dict)
#@app.delete("/users/{user_id}",response_class = JSONResponse)
def delete_user(user_id:int, db: Session = Depends(get_db)):

    # Retrieve the user from the database
    user_to_delete = db.query(Users).filter(Users.id == user_id).first()


    if not user_to_delete :
        raise HTTPException(status_code=404, detail="User not found")


    db.delete(user_to_delete)
    db.commit()

    return {"message": f"user with ID {user_id} has been deleted"}

#patch mapping
class UserUpadteSchema(BaseModel):
    name:Optional[str] = None
    email:Optional[str] = None
    password:Optional[str] = None

@router.patch("/{user_id}", response_model=UserSchema)
def patch_user(user_id: int, user: UserUpadteSchema, db: Session = Depends(get_db)):
    # Retrieve the user from the database
    user_to_update = db.query(Users).filter(Users.id == user_id).first()
    
    if not user_to_update:
        # Raise an HTTPException if the user does not exist
        raise HTTPException(status_code=404, detail="User not found")
    
    # Update only the provided fields
    if user.name is not None:
        user_to_update.name = user.name
    if user.email is not None:
        user_to_update.email = user.email
    if user.password is not None:
        user_to_update.password = user.password  # You can hash the password here if needed

    # Commit the changes to the database
    db.commit()
    db.refresh(user_to_update)  # Refresh to get the updated data


    return user_to_update
