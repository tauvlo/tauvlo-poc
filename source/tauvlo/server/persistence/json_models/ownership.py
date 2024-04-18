from typing import List

from pydantic import BaseModel, Field


class OwnershipRecord(BaseModel):
    user_id: str = Field(title="User ID", example="ABC")
    property_id: str = Field(title="Property ID", example="XYZ")
    num_tokens: int = Field(title="Tokens owned in property", example=0)


class OwnershipListRequest(BaseModel):
    user_id: str = Field(title="User ID", example="ABC", default=None)
    property_id: str = Field(title="Property ID", example="XYZ", default=None)


class OwnershipListResponse(BaseModel):
    records: List[OwnershipRecord] = Field(title="List of filtered ownership records")
