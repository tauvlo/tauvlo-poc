from typing import Optional

from pydantic import BaseModel, Field

from tauvlo.server.persistence.orm_model import TransactionRecordType


class TransactionDetails(BaseModel):
    description: str = Field(title="User name", example="John Doe")


class TransactionRecordDetail(BaseModel):
    transaction_id: int = Field(title="User ID", example="ABC")
    user_id: str = Field(title="ID of the user involved in the transaction", example="ABC")
    transaction_type: TransactionRecordType = Field(title="Transaction record type",
                                                    example=TransactionRecordType.BUY_TOKENS)
    property_id: str = Field(title="ID of the property figuring in the transaction, if any",
                             example="XYZ", default=None)
    details: TransactionDetails = Field(title="Transaction details")
