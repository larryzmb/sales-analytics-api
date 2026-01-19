from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import asc, desc

from .database import Base, engine, get_db
from .models.user import User
from .models.product import Product
from .schemas.user import UserCreate, UserResponse
from .schemas.product import ProductCreate, ProductResponse
from .security import hash_password, verify_password, create_access_token
from .auth import get_current_user

app = FastAPI()

@app.get("/")
def root():
    return {"message": "API rodando."}


Base.metadata.create_all(bind=engine)



@app.post("/users", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(
        email=user.email,
        hashed_password=hash_password(user.password)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@app.get("/users", response_model=list[UserResponse])
def list_users(db: Session = Depends(get_db)):
    return db.query(User).all()


@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Email ou senha incorretos")

    token = create_access_token(
        data={"sub": user.email},
        expires_delta=timedelta(minutes=60)
    )

    return {"access_token": token, "token_type": "bearer"}


@app.get("/me", response_model=UserResponse)
def read_me(current_user: User = Depends(get_current_user)):
    return current_user




@app.post("/products", response_model=ProductResponse)
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_product = Product(
        name=product.name,
        price=product.price,
        description=product.description,
        owner_id=current_user.id
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


@app.get("/products", response_model=list[ProductResponse])
def list_products(
    search: str | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
    order_by: str | None = "name",
    order_dir: str | None = "asc",
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    query = db.query(Product)

    if search:
        query = query.filter(Product.name.ilike(f"%{search}%"))
    if min_price is not None:
        query = query.filter(Product.price >= min_price)
    if max_price is not None:
        query = query.filter(Product.price <= max_price)

    if order_by in ["name", "price"]:
        query = query.order_by(desc(getattr(Product, order_by)) if order_dir == "desc" else asc(getattr(Product, order_by)))

    return query.offset(skip).limit(limit).all()


@app.get("/my-products", response_model=list[ProductResponse])
def list_my_products(
    min_price: float | None = None,
    max_price: float | None = None,
    order_by: str | None = "name",
    order_dir: str | None = "asc",
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Product).filter(Product.owner_id == current_user.id)

    if min_price is not None:
        query = query.filter(Product.price >= min_price)
    if max_price is not None:
        query = query.filter(Product.price <= max_price)

    if order_by in ["name", "price"]:
        query = query.order_by(desc(getattr(Product, order_by)) if order_dir == "desc" else asc(getattr(Product, order_by)))

    return query.offset(skip).limit(limit).all()


@app.put("/products/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    updated: ProductCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    if product.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Você não pode editar este produto")

    product.name = updated.name
    product.price = updated.price
    product.description = updated.description

    db.commit()
    db.refresh(product)
    return product


@app.delete("/products/{product_id}", status_code=204)
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    if product.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Você não pode deletar este produto")

    db.delete(product)
    db.commit()
    return
