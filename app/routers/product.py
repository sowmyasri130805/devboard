from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models.product import Product
from app.models.user import User
from app.schemas.product import ProductCreate, ProductUpdate, ProductResponse
from app.oauth2 import get_current_user

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)


# ─── GET ALL PRODUCTS (public + search + filter) ──────────
@router.get("/", response_model=List[ProductResponse])
def get_products(
    db: Session = Depends(get_db),
    search: Optional[str] = Query(None, description="Search by name"),
    min_price: Optional[float] = Query(None, description="Minimum price"),
    max_price: Optional[float] = Query(None, description="Maximum price")
):
    query = db.query(Product)

    # Search by name if provided
    if search:
        query = query.filter(Product.name.ilike(f"%{search}%"))

    # Filter by min price
    if min_price is not None:
        query = query.filter(Product.price >= min_price)

    # Filter by max price
    if max_price is not None:
        query = query.filter(Product.price <= max_price)

    return query.all()


# ─── GET ONE PRODUCT (public) ─────────────────────────────
@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return product


# ─── CREATE PRODUCT (auth required) ──────────────────────
@router.post("/", response_model=ProductResponse, status_code=201)
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_product = Product(
        name=product.name,
        description=product.description,
        price=product.price,
        stock=product.stock
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


# ─── UPDATE PRODUCT (auth required) ──────────────────────
@router.patch("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    updated_product: ProductUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    if updated_product.name is not None:
        product.name = updated_product.name
    if updated_product.description is not None:
        product.description = updated_product.description
    if updated_product.price is not None:
        product.price = updated_product.price
    if updated_product.stock is not None:
        product.stock = updated_product.stock

    db.commit()
    db.refresh(product)
    return product


# ─── DELETE PRODUCT (auth required) ──────────────────────
@router.delete("/{product_id}", status_code=204)
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    db.delete(product)
    db.commit()
    return None