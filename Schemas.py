from pydantic import BaseModel, EmailStr

# Pydantic schemas
class UserCreateSchema(BaseModel):
    name: str
    email: EmailStr  # Validates email format
    password: str

class UserSchema(BaseModel):
    id: int
    name: str
    email: EmailStr

    class Config:
        orm_mode = True  # Ensures compatibility with SQLAlchemy models