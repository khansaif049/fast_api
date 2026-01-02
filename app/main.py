from fastapi import FastAPI,HTTPException,Query
from services.products import get_all_products
app = FastAPI()

@app.get('/')
def root():
    return {"message":"Welcome to fastAPi"}



@app.get("/products")
def list_products(name:str=Query(default=None,min_length=1,max_length=50,description="Search by Product name (case insensetivity)")):
    products = get_all_products()
    if name:
        needle = name.strip().lower()
        products = [p for p in products if needle in p.get("name","").lower()]
        if not products:
            raise HTTPException(status_code=404,detail=f"No product matching name ={name}")
        total = len(products)

        return{
            "total":total,
            "items":products
        }
    return name

