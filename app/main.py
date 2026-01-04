from fastapi import FastAPI,HTTPException,Query,Path
from app.services.products import get_all_products,add_product

from schema.product import Product
from uuid import uuid4
from datetime import datetime

app = FastAPI()
@app.get('/')
def root():
    return {"message":"Welcome to fastAPi"}



@app.get("/products")
def list_products(name:str=Query(default=None,min_length=1,max_length=50,description="Search by Product name (case insensetivity)"),
        sort_by_price:bool=Query(default=False,description="sort"),
        order:str=Query(default="asc",description="sort products by asc and des"),
        limit:int=Query(default=10,ge=1,le=100,description="Number of items")):
    products = get_all_products()
    if name:
        needle = name.strip().lower()
        products = [p for p in products if needle in p.get("name","").lower()]
    if not products:
        raise HTTPException(status_code=404,detail=f"No product matching name ={name}")
    
    if sort_by_price:
        reverse = order == "des"
        products = sorted(products,key=lambda p:p.get("price",0),reverse=reverse)

    total = len(products)

    # products = products[0:limit]
    return{
        "total":total,
        "items":products
    }
    return name

@app.get("/products/{product_id}")
def get_product_by_id(product_id:str=Path(...,min_length=36,max_length=36,description="UUID of the product")):
    products = get_all_products()
    for product in products:
        if product['id']==product_id:
            return product
    raise HTTPException(status_code=404,detail=f"No product matching product_id ={product_id}")

@app.post("/products",status_code=201)
def create_product(product:Product):
    product_dict = product.model_dump(mode="json")
    product_dict["id"] = str(uuid4())
    product_dict['created_at']= datetime.utcnow().isoformat()+"Z"
    try:
        add_product(product_dict)
    except ValueError as e:
        raise HTTPException(status_code=400,detail=str(e))
    return product.model_dump(mode="json")



