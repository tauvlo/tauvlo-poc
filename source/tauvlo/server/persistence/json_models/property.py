from typing import List

from pydantic import BaseModel, Field


class PropertyDetails(BaseModel):
    name: str = Field(title="Property name", example="Urban rental apartment in downtown Prague")
    image_urls: List[str] = Field(title="List of image urls", example="[\"/images/blog-4-detail-p-500.png\"]")
    type: str = Field(Title="Property type", example="Residential")
    status: str = Field(Title="Property status", example="Generating income")
    sto_value: str = Field(Title="Property STO value", example="$500k")
    tokens_issued: str = Field(Title="Amount of total issued tokens", example="1000")
    price_per_token: str = Field(Title="Property price per token", example="$20")
    yield_irr_pct: str = Field(Title="Property yield percentage", example="5.3%")
    highlight_text: str = Field(Title="Property highlight text", example="Urban rental apartment in downtown Prague")


class PropertyDetailResponse(BaseModel):
    property_id: str = Field(title="Property ID", example="TVL000X001")
    poster_id: str = Field(title="Original property poster user ID", example="ABC")
    details: PropertyDetails = Field(title="Property details")


class RegisterPropertyRequest(PropertyDetailResponse):
    admin_access_key: str = Field(title="Admin access key", example="1234ABCD")


class PropertyListResponse(BaseModel):
    properties: List[PropertyDetailResponse]

