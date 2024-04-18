import enum
from typing import Union, List, Optional

from pydantic import BaseModel, Field


class XLMBalanceResponse(BaseModel):
    xlm_balance: str = Field(title="Account XLM balance", example="10.0", default=None)


class StellarTransactionResult(BaseModel):
    success_flag: bool = Field(title="Transaction success flag", example=True)
    is_json_response: bool = Field(title="Result is interpretable as JSON", example=True)
    response: Union[dict, str] = Field(title="Transaction response", example={"success": True})


class TauvloOfferType(str, enum.Enum):
    BUYING = "BUYING"
    SELLING = "SELLING"


class TauvloOffer(BaseModel):
    offer_type: TauvloOfferType = Field(title="Offer type", example=TauvloOfferType.BUYING)
    offer_id: Optional[str] = Field(title="Stellar offer ID", example="123", default=None)
    tauvlo_asset_code: str = Field(title="Tauvlo asset", example="TVL000X001")
    amount: str = Field(title="Tauvlo asset amount", example="1.0")
    usdc_per_token: str = Field(title="USDC price for the whole amount", example="1.0")


class TauvloOffersResponse(BaseModel):
    offers: List[TauvloOffer] = Field(title="List of active offers")


class ExecuteTransactionRequest(BaseModel):
    transaction_xdr: str = Field(title="Transaction XDR (base64)")


class PropertySellRequest(BaseModel):
    selling_tokens_amount: str = Field(title="Amount of tokens to sell")
    usdc_price_per_token: str = Field(title="Asked USDC amount per token")
    tauvlo_asset_code: str = Field(title="Asset code")
    offer_id: int = Field(title="ID of an existing offer, optional, defaults to 0", default=0)


class PropertyBuyRequest(BaseModel):
    buying_tokens_amount: str = Field(title="Amount of tokens to buy")
    usdc_price_per_token: str = Field(title="Offered USDC amount per token")
    tauvlo_asset_code: str = Field(title="Asset code")
    offer_id: int = Field(title="ID of an existing offer, optional, defaults to 0", default=0)
