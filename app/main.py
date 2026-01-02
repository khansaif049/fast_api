from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def root():
    return {"message":"Welcome to fastAPi"}

@app.get('product/{id}')
def get_product_from_id(id:int):
    products = ['Brush','monitor']

    return products[id]