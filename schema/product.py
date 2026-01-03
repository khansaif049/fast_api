from pydantic import BaseModel,Field,AnyUrl
from typing import Annotated,Literal,Optional
from uuid import UUID
from datetime import datetime

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
    #seller
    created_at:datetime