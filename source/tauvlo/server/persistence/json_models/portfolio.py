from pydantic import BaseModel, Field

from typing import List


class TauvloAsset(BaseModel):
    property_name: str = Field(title="Property name", example="Beachfront property 2", default=None)
    asset_code: str = Field(title="Asset code", example="TVL000X001")
    amount: str = Field(title="Amount owned", example="TVL000X001")
    total_value: str = Field(title="Value of the held asset type", example="$5,254.37")
    total_profit_pct: str = Field(title="Percentage profit on the asset type", example="+12.8%")


class PortfolioResponse(BaseModel):
    total_balance: str = Field(title="Total value of the asset", example="$124,783.00")
    total_gains: str = Field(title="Total profit across the entire portfolio", example="+$9,774.00")
    usdc_trusted: bool = Field(title="A flag indicating whether USDC is trusted", example=True)
    assets: List[TauvloAsset] = Field(title="Individual held assets")
