from pydantic import BaseModel, Field


class UserDetails(BaseModel):
    name: str = Field(title="User name", example="John Doe")


class UserDetailResponse(BaseModel):
    user_id: str = Field(title="User ID", example="ABC")
    details: UserDetails = Field(title="User details")
