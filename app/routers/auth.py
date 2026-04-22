from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse, UserLogin
from app.utils import hash_password, verify_password

router = APIRouter(
    prefix="/auth",       # all routes start with /auth
    tags=["Authentication"]  # groups in docs
)

# ─── REGISTER ────────────────────────────────────────────
@router.post("/register", response_model=UserResponse, status_code=201)
def register(user: UserCreate, db: Session = Depends(get_db)):

    # Check if email already exists
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    # Check if username already exists
    existing_username = db.query(User).filter(User.username == user.username).first()
    if existing_username:
        raise HTTPException(
            status_code=400,
            detail="Username already taken"
        )

    # Hash the password before saving
    hashed = hash_password(user.password)

    # Create new user object
    new_user = User(
        username=user.username,
        email=user.email,
        password=hashed
    )

    # Save to database
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# ─── LOGIN ───────────────────────────────────────────────
@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):

    # Find user by email
    db_user = db.query(User).filter(User.email == user.email).first()

    # Check if user exists
    if not db_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    # Check if password is correct
    if not verify_password(user.password, db_user.password):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    # For now return success (we'll add JWT token in Module 4!)
    return {
        "message": "Login successful!",
        "user_id": db_user.id,
        "username": db_user.username
    }