from pydantic import BaseModel,Field,AnyUrl,field_validator,model_validator,computed_field,EmailStr
from typing import Annotated,Literal,Optional
from uuid import UUID
from datetime import datetime


class Seller(BaseModel):
    id:UUID
    name:Annotated[
        str,
        Field(
            min_length=2,
            max_length=60,
            title="Seller Name",
            description="Name of the seller (2-60)",
            examples=["mistore.in","Apple Store Mumbai"]
        )
    ]
    email:EmailStr
    website:AnyUrl


    @field_validator("email",mode="after")
    @classmethod
    def validate_seller_email_format(cls,value:EmailStr):
        allowed_domains =['mistore.in',"hpstore.in"]
        domain = str(value).split('@')[-1].lower()
        if domain not in allowed_domains:
            raise ValueError("domain not allowed : {domain}")
        return value

class Product(BaseModel):
    id:UUID
    sku:Annotated[str,Field(min_length=6,max_length=30,title="Sku",
    description="stock keeping unit",
    examples=["123-123123"])]
    name:Annotated[
        str,
        Field(
            min_length=3,
            max_length=80,
            title="Product Name",
            description="Readable Product name",
            examples=["Moto"]
        )
    ]

    description:Annotated[
        str,
        Field(max_length=200,description="short product"),
    ]

    category:Annotated[
        str,
        Field(min_length=3,
            max_length=30,
            description="Category like Mob/lap/ele",
            examples=["mobiles","laptop"]
            ),
    ]

    brand:Annotated[
        str,
        Field(min_length=2,max_length=50,examples=["Xiaomi","Apple"]),
    ]

    prices:Annotated[
        float,
        Field(gt=0,strict=True,description="Base Prices in INR")
    ]
    currency:Literal["INR"] = "INR"

    discount_percent:Annotated[
        int,
        Field(ge=0,le=90,description="Discount"),
    ]

    stock:Annotated[
        int,
        Field(ge=0,description="Available")
    ]

    is_active:Annotated[
        bool,
        Field(description="Is Product Availabe")
    ]

    rating:Annotated[
        float,
        Field(ge=0,le=5,strict=True,description="Rating out of 5")
    ]

    tags:Annotated[
        Optional[list[str]],
        Field(default=None,max_length=10,description="upto 10 tags")
    ]

    image_url:Annotated[
        list[AnyUrl],
        Field(max_length=1,description="atleat 1 url")
    ]

    #dimension_cm
    seller:Seller
    created_at:datetime

    @field_validator("sku",mode="after")
    @classmethod
    def validate_sku_format(cls,value:str):
        if "-" not in value:
            raise ValueError("Sku must have '-'")
        last = value.split("-")[-1]
        if not len(last) ==3 and last.isdigit():
            raise ValueError("Sku must ends with 3 digit seq like this -234")
        
        return value
        
    @model_validator(mode="after")
    @classmethod
    def validate_business_rules(cls,model:"Product"):
        if model.stock == 0 and model.is_active is True:
            raise ValueError("if stock is 0 active must be False")
        
        if model.discount_percent>0 and model.rating == 0:
            raise ValueError("Discountedr price must have rating != 0")
        
        return model
        

    @computed_field
    @property
    def final_price(self) -> float:
        return round(self.prices*(1-self.discount_percent/100),2)