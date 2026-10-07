from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from pwdlib import PasswordHash

from .database import engine, Base, get_db
from . import models


# Create FastAPI app
app = FastAPI(
    title="FindBack",
    description="Campus Lost & Found System",
    version="1.0.0"
)


# Create database tables
Base.metadata.create_all(bind=engine)


# Password hashing
password_hash = PasswordHash.recommended()


# =========================
# USER REGISTRATION MODEL
# =========================

class UserCreate(BaseModel):
    name: str
    email: str
    student_id: str
    password: str


# =========================
# USER LOGIN MODEL
# =========================

class UserLogin(BaseModel):
    email: str
    password: str


# =========================
# HOME
# =========================

@app.get("/")
def home():
    return {
        "message": "Welcome to FindBack!",
        "status": "running"
    }


# =========================
# HEALTH CHECK
# =========================

@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


# =========================
# REGISTER
# =========================

@app.post("/register")
def register_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):

    # Check if email already exists
    existing_user = db.query(models.User).filter(
        models.User.email == user.email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    # Hash password
    hashed_password = password_hash.hash(user.password)

    # Create new user
    new_user = models.User(
        name=user.name,
        email=user.email,
        student_id=user.student_id,
        password=hashed_password
    )

    # Save user
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "Registration successful",
        "user_id": new_user.id,
        "name": new_user.name,
        "email": new_user.email
    }


# =========================
# LOGIN
# =========================

@app.post("/login")
def login_user(
    user: UserLogin,
    db: Session = Depends(get_db)
):

    # Find user by email
    existing_user = db.query(models.User).filter(
        models.User.email == user.email
    ).first()

    # If email doesn't exist
    if not existing_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    # Verify password
    if not password_hash.verify(
        user.password,
        existing_user.password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    return {
        "message": "Login successful",
        "user_id": existing_user.id,
        "name": existing_user.name,
        "email": existing_user.email,
        "role": existing_user.role
    }