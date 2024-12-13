from fastapi import FastAPI, Depends, HTTPException
from typing import List
from database import Base, SessionLocal, engine
from models import Users
from sqlalchemy.orm import Session
from pydantic import BaseModel
#from fastapi.responses import JSONResponse 
from typing import Optional


# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency for database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()  # Add parentheses here

# Pydantic schemas
class UserSchema(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        orm_mode = True

class UserCreateSchema(BaseModel):
    name: str
    email: str
    password: str

# Create a new user
@app.post("/users", response_model=UserSchema)
def create_users(user: UserCreateSchema, db: Session = Depends(get_db)):
    new_user = Users(name=user.name, email=user.email, password=user.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)  # Refresh to get the generated ID
    return new_user

# Get all users
@app.get("/users", response_model=List[UserSchema])
def get_users(db: Session = Depends(get_db)):
    return db.query(Users).all()


#put
@app.put("/users/{user_id}", response_model=UserSchema)
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
@app.delete("/users/{user_id}",response_model = dict)
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

@app.patch("/users/{user_id}", response_model=UserSchema)
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
