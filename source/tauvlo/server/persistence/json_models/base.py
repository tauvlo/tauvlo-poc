from typing import Optional

from pydantic import BaseModel, Field


class TestData(BaseModel):
    optional_string: Optional[str] = Field(title="Test optional string field", example="something", default=None)
    number: int = Field(title="Test number field", example=5)


class ErrorMessage(BaseModel):
    detail: str


class ValidationErrorMessage(ErrorMessage):
    pass
