from pydantic import BaseModel

class ProductCreate(BaseModel):
    name: str
    price: float
    description: str

class ProductResponse(BaseModel):
    id: int
    name: str
    price: float
    description: str
    owner_id: int  

    class Config:
        from_attributes = True
