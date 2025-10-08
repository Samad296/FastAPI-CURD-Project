from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List
import uvicorn

# Create FastAPI instance
app = FastAPI(
    title="Product Management API",
    description="A simple FastAPI CRUD application for managing products",
    version="1.0.0"
)

# Product Model
class Product(BaseModel):
    id: int
    name: str = Field(..., min_length=2)
    price: float = Field(..., gt=0)
    in_stock: bool = True

# In-memory database (list)
products_db: List[Product] = []

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the Product Management API"}

# Create product
@app.post("/products/", response_model=Product)
def create_product(prod: Product):
    for p in products_db:
        if p.id == prod.id:
            raise HTTPException(status_code=400, detail="Product with given ID already exists")
    products_db.append(prod)
    return prod

# Get all products
@app.get("/products/", response_model=List[Product])
def get_all_products():
    return products_db

# Get product by ID
@app.get("/products/{product_id}", response_model=Product)
def get_product_by_id(product_id: int):
    for p in products_db:
        if p.id == product_id:
            return p
    raise HTTPException(status_code=404, detail="Product not found")

# Update product
@app.put("/products/{product_id}", response_model=Product)
def update_product(product_id: int, updated_product: Product):
    for index, p in enumerate(products_db):
        if p.id == product_id:
            products_db[index] = updated_product
            return updated_product
    raise HTTPException(status_code=404, detail="Product not found")

# Delete product
@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    for index, p in enumerate(products_db):
        if p.id == product_id:
            del products_db[index]
            return {"message": "Product deleted successfully"}
    raise HTTPException(status_code=404, detail="Product not found")

# Run the app
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
