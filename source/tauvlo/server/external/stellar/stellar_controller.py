import json
from decimal import Decimal
from typing import Union, Tuple, List

from stellar_sdk import Keypair, Network, Server, TransactionBuilder, Asset, TransactionEnvelope, Price

from tauvlo.server.persistence.configuration import CONFIG
from tauvlo.server.persistence.json_models.stellar import StellarTransactionResult, TauvloOffer, TauvloOfferType


class StellarBalances:
    def __init__(self,
                 xlm_balance: Decimal,
                 usdc_balance: Decimal,
                 usdc_trusted: bool,
                 tauvlo_balances: List[Tuple[str, Decimal]]):
        self.xlm_balance = xlm_balance
        self.usdc_balance = usdc_balance
        self.usdc_trusted = usdc_trusted
        self.tauvlo_balances = tauvlo_balances


class StellarController:
    def __init__(self):
        self.server = Server(horizon_url=CONFIG.stellar_horizon_url)
        self.issuer_public_key = CONFIG.stellar_issuer_public_key
        self.issuer_private_key = CONFIG.stellar_issuer_private_key
        self.usdc_issuer_public_key = CONFIG.stellar_usdc_issuer_public_key
        self.default_base_fee = CONFIG.stellar_default_base_fee
        self.default_trn_timeout_sec = CONFIG.stellar_default_trn_timeout_sec

        if CONFIG.stellar_use_mainnet:
            self.network_passphrase = Network.PUBLIC_NETWORK_PASSPHRASE
        else:
            self.network_passphrase = Network.TESTNET_NETWORK_PASSPHRASE

    def get_xlm_balance(self, public_key: str) -> Decimal:
        source_account = self.server.load_account(account_id=public_key)
        balances = source_account.raw_data.get("balances", [])
        for balance in balances:
            if balance.get("asset_type") == "native":
                return Decimal(balance.get("balance", "0"))

    def get_balances(self, public_key: str) -> StellarBalances:
        source_account = self.server.load_account(account_id=public_key)
        balances = source_account.raw_data.get("balances", [])
        xlm_balance = Decimal("0.0")
        usdc_balance = Decimal("0.0")
        usdc_trusted = False
        tauvlo_balances = []
        for balance in balances:
            if balance.get("asset_type") == "native":
                xlm_balance = Decimal(balance.get("balance", "0.0"))
            else:
                issuer = balance.get("asset_issuer", None)
                if issuer == self.issuer_public_key:
                    tauvlo_balances.append((balance.get("asset_code", None), Decimal(balance.get("balance", "0.0"))))
                elif issuer == self.usdc_issuer_public_key and balance.get("asset_code", None) == "USDC":
                    usdc_balance = Decimal(balance.get("balance", "0.0"))
                    usdc_trusted = True
        return StellarBalances(xlm_balance, usdc_balance, usdc_trusted, tauvlo_balances)

    def _build_base_transaction(self, source_account_public_key: str) -> TransactionBuilder:
        source_account = self.server.load_account(source_account_public_key)
        return TransactionBuilder(
            source_account=source_account,
            network_passphrase=self.network_passphrase,
            base_fee=self.default_base_fee
        ).set_timeout(
            self.default_trn_timeout_sec
        )

    def manage_tvl_sell_offer_xdr(self,
                                  selling_tokens_amount: str,
                                  usdc_price_per_token: str,
                                  account_public_key: str,
                                  tauvlo_asset_code: str,
                                  offer_id: int = 0) -> str:
        if Decimal(selling_tokens_amount) == Decimal("0.0"):
            calculated_price = Decimal("1.0")
            calculated_amount = Decimal("0.0")
        else:
            calculated_price = Decimal(usdc_price_per_token)
            calculated_amount = Decimal(selling_tokens_amount)
        transaction = (
            self._build_base_transaction(account_public_key)
            .append_manage_sell_offer_op(
                selling=Asset(tauvlo_asset_code, self.issuer_public_key),
                buying=Asset("USDC", self.usdc_issuer_public_key),
                amount=calculated_amount,
                price=calculated_price,
                offer_id=offer_id,
                source=account_public_key
            )
            .build()
        )
        return transaction.to_xdr()

    def manage_tvl_buy_offer_xdr(self,
                                 usdc_price_per_token: str,
                                 buying_tokens_amount: str,
                                 account_public_key: str,
                                 tauvlo_asset_code: str,
                                 offer_id: int = 0) -> str:
        if Decimal(buying_tokens_amount) == Decimal("0.0"):
            calculated_price = Decimal("1.0")
            calculated_amount = Decimal("0.0")
        else:
            calculated_price = usdc_price_per_token
            calculated_amount = Decimal(buying_tokens_amount) * Decimal(usdc_price_per_token)
        transaction = (
            self._build_base_transaction(account_public_key)
                .append_manage_sell_offer_op(
                selling=Asset("USDC", self.usdc_issuer_public_key),
                buying=Asset(tauvlo_asset_code, self.issuer_public_key),
                amount=calculated_amount,
                price=calculated_price,
                offer_id=offer_id,
                source=account_public_key
            )
            .build()
        )
        return transaction.to_xdr()

    def list_all_offers_for_asset(self, asset_code: str) -> List[TauvloOffer]:
        asset1 = Asset("USDC", self.usdc_issuer_public_key)
        asset2 = Asset(asset_code, self.issuer_public_key)
        orderbook_response = self.server.orderbook(selling=asset1, buying=asset2).call()

        offers = []

        for bid in orderbook_response.get("bids", list()):
            bid_price_r = bid.get("price_r", {})
            offers.append(TauvloOffer(
                offer_type=TauvloOfferType.SELLING,
                tauvlo_asset_code=asset_code,
                amount=bid.get("amount"),
                usdc_per_token=str(Decimal(bid_price_r.get("d")) / Decimal(bid_price_r.get("n")))
            ))

        for ask in orderbook_response.get("asks", list()):
            offers.append(TauvloOffer(
                offer_type=TauvloOfferType.BUYING,
                tauvlo_asset_code=asset_code,
                amount=ask.get("amount"),
                usdc_per_token=ask.get("price")
            ))

        return offers

    def list_all_tauvlo_offers(self, account_public_key: str) -> List[TauvloOffer]:
        offers_response = self.server.offers().for_account(account_public_key).call()
        offers_raw = offers_response.get("_embedded", dict()).get("records", list())
        tauvlo_offers = []

        for offer in offers_raw:
            selling = offer.get("selling", dict())
            buying = offer.get("buying", dict())
            amount = offer.get("amount", None)
            price = offer.get("price", None)
            offer_id = offer.get("id", None)

            if selling.get("asset_code") == "USDC" and selling.get("asset_issuer") == self.usdc_issuer_public_key:
                if buying.get("asset_issuer") == self.issuer_public_key:
                    tauvlo_offers.append(
                        TauvloOffer(
                            offer_type=TauvloOfferType.BUYING,
                            offer_id=offer_id,
                            tauvlo_asset_code=buying.get("asset_code", None),
                            amount=amount,
                            usdc_per_token=price
                        )
                    )
            if buying.get("asset_code") == "USDC" and buying.get("asset_issuer") == self.usdc_issuer_public_key:
                if selling.get("asset_issuer") == self.issuer_public_key:
                    tauvlo_offers.append(
                        TauvloOffer(
                            offer_type=TauvloOfferType.SELLING,
                            offer_id=offer_id,
                            tauvlo_asset_code=selling.get("asset_code", None),
                            amount=amount,
                            usdc_per_token=price
                        )
                    )

        return tauvlo_offers

    def issue_tokens(self,
                     token_identifier: str,
                     receiver_public_key: str,
                     amount: Decimal) -> StellarTransactionResult:
        issuer_keypair = Keypair.from_secret(self.issuer_private_key)
        asset = Asset(token_identifier, self.issuer_public_key)

        transaction = (
            self._build_base_transaction(self.issuer_public_key)
                .append_payment_op(receiver_public_key, asset, str(amount))
                .build()
        )

        transaction.sign(issuer_keypair)

        return self.execute_transaction(transaction)

    def create_trustline_xdr(self,
                             token_receiver_public_key: str,
                             token_identifier: str) -> str:
        if token_identifier == "USDC":
            issuer = self.usdc_issuer_public_key
        else:
            issuer = self.issuer_public_key
        asset = Asset(token_identifier, issuer)

        transaction = (
            self._build_base_transaction(token_receiver_public_key)
                .append_change_trust_op(
                asset=asset
            )
            .build()
        )

        return transaction.to_xdr()

    def execute_transaction(self, transaction: Union[TransactionEnvelope, str]) -> StellarTransactionResult:
        """
        Executes transaction on the Horizon server.
        @transaction: Transaction either in the form of the SDK object or XDR envelope string.
        @return: Stellar transaction result object.
        """
        try:
            return StellarTransactionResult(
                success_flag=True,
                is_json_response=True,
                response=self.server.submit_transaction(transaction))
        except Exception as err:
            try:
                return StellarTransactionResult(
                    success_flag=False,
                    is_json_response=True,
                    response=json.loads(err.message))
            except Exception as err2:
                print("Failed to interpret error result as a JSON:", err2)
                return StellarTransactionResult(
                    success_flag=False,
                    is_json_response=False,
                    response=str(err.message))
