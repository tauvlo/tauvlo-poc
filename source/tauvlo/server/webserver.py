import json
from typing import Optional, Annotated

from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jinja2 import TemplateNotFound
from starlette import status
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from pydantic.json import pydantic_encoder

from tauvlo.server.controller import Controller
from tauvlo.server.logging import configure_logger, get_logger
from tauvlo.server.persistence.configuration import CONFIG
from tauvlo.server.persistence.json_models.base import ErrorMessage, ValidationErrorMessage, TestData
from tauvlo.server.persistence.json_models.ownership import OwnershipListResponse, OwnershipListRequest
from tauvlo.server.persistence.json_models.portfolio import PortfolioResponse
from tauvlo.server.persistence.json_models.property import PropertyListResponse, PropertyDetailResponse, \
    RegisterPropertyRequest
from tauvlo.server.persistence.json_models.stellar import XLMBalanceResponse, TauvloOffersResponse, \
    StellarTransactionResult, ExecuteTransactionRequest, PropertyBuyRequest, PropertySellRequest
from tauvlo.server.session import SessionCache, SessionData

API_VERSION = "0.0.1"
API_MAJOR_PREFIX = "v1"
RESPONSES = {
    401: {401: {"description": "Not authorized", "model": ErrorMessage}},
    404: {404: {"description": "Item not found", "model": ErrorMessage}},
    422: {422: {"description": "Validation error", "model": ValidationErrorMessage}}
}
TAGS_METADATA = []


class WebServer:

    def __init__(self, app: FastAPI, controller: Controller = None) -> None:
        self.app = app
        self.controller = controller
        self.templates = Jinja2Templates(directory=CONFIG.frontend_static_dir)
        self.session_cache = SessionCache(ttl_sec=3600)  # TODO add configurable session length

    @staticmethod
    def json_serializer(*args, **kwargs) -> str:
        return json.dumps(*args, default=pydantic_encoder, **kwargs)


configure_logger()
logger = get_logger(__name__)
controller = Controller()
app = FastAPI(title="Tauvlo Backend", version=API_VERSION, openapi_tags=TAGS_METADATA)
ws = WebServer(app, controller)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"/api/{API_MAJOR_PREFIX}/login")


async def get_session_data(request: Request, token: str = Depends(oauth2_scheme)) -> SessionData:
    """
    Function to retrieve session data if user is logged in. Uses OAuth2 scheme.
    """
    session_data = ws.session_cache.get(token)
    if session_data:
        return session_data
    else:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Not authorized")


@app.on_event("startup")
def startup_event():
    logger.info("Server started up")


@app.get(f"/api/{API_MAJOR_PREFIX}/stellar/get_balances",
         description="Retrieve XLM balance",
         response_description="XLM balance",
         tags=[],
         status_code=status.HTTP_200_OK,
         responses={**RESPONSES[422]},
         response_model=XLMBalanceResponse)
async def get_balances(session_data: SessionData = Depends(get_session_data)) -> XLMBalanceResponse:
    return ws.controller.get_xlm_balance(session_data.public_key)


@app.post(f"/api/{API_MAJOR_PREFIX}/ownership/list",
          description="List ownership records by user ID or property ID.",
          status_code=status.HTTP_200_OK,
          responses={**RESPONSES[422]},
          response_model=OwnershipListResponse)
def get_ownership_list(ownership_list_request: OwnershipListRequest) -> OwnershipListResponse:
    # TODO add invalid request
    return ws.controller.get_ownership_list(ownership_list_request.user_id, ownership_list_request.property_id)


@app.get(f"/api/{API_MAJOR_PREFIX}/property/list",
         description="List properties.",
         status_code=status.HTTP_200_OK,
         responses={**RESPONSES[422]},
         response_model=PropertyListResponse)
def get_property_list() -> PropertyListResponse:
    # TODO add paging
    return ws.controller.get_properties_page(page_number=1, page_size=10)


@app.post(f"/api/{API_MAJOR_PREFIX}/property/register",
          description="List properties.",
          status_code=status.HTTP_201_CREATED,
          responses={**RESPONSES[422]})
def register_property(new_property: RegisterPropertyRequest) -> StellarTransactionResult:
    if CONFIG.dev_admin_key == new_property.admin_access_key:
        return ws.controller.register_property(new_property)
    else:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Incorrect admin access key")


@app.get(f"/api/{API_MAJOR_PREFIX}/property/{{property_id}}",
         description="List properties.",
         status_code=status.HTTP_200_OK,
         responses={**RESPONSES[422]},
         response_model=PropertyDetailResponse)
def get_property_detail(property_id: str) -> PropertyDetailResponse:
    return ws.controller.get_property_detail(property_id)


@app.get(f"/api/{API_MAJOR_PREFIX}/portfolio",
         description="Get portfolio details.",
         status_code=status.HTTP_200_OK,
         responses={**RESPONSES[422]},
         response_model=PortfolioResponse)
def get_portfolio(session_data: SessionData = Depends(get_session_data)) -> PortfolioResponse:
    return ws.controller.get_assets(session_data.public_key)


@app.get(f"/api/{API_MAJOR_PREFIX}/offers",
         description="Get my current offers.",
         status_code=status.HTTP_200_OK,
         responses={**RESPONSES[422]},
         response_model=TauvloOffersResponse)
def get_offers(session_data: SessionData = Depends(get_session_data)) -> TauvloOffersResponse:
    return ws.controller.get_offers(session_data.public_key)


@app.get(f"/api/{API_MAJOR_PREFIX}/assets/trustline/{{asset_code}}",
         description="Get my current offers.",
         status_code=status.HTTP_200_OK,
         responses={**RESPONSES[422]})
def get_trustline_xdr(asset_code: str, session_data: SessionData = Depends(get_session_data)) -> str:
    return ws.controller.get_trustline_xdr(session_data.public_key, asset_code)


@app.get(f"/api/{API_MAJOR_PREFIX}/assets/offers/{{asset_code}}",
         description="Get offers for asset.",
         status_code=status.HTTP_200_OK,
         responses={**RESPONSES[422]},
         response_model=TauvloOffersResponse)
def get_offers_for_asset(asset_code: str,
                         session_data: SessionData = Depends(get_session_data)) -> TauvloOffersResponse:
    return ws.controller.get_offers_for_asset(asset_code)


@app.post(f"/api/{API_MAJOR_PREFIX}/assets/buy",
          description="Create XDR to buy property tokens.",
          status_code=status.HTTP_200_OK,
          responses={**RESPONSES[422]})
def buy_property_tokens_xdr(buy_request: PropertyBuyRequest,
                            session_data: SessionData = Depends(get_session_data)) -> str:
    return ws.controller.buy_property_tokens_xdr(buy_request, session_data.public_key)


@app.post(f"/api/{API_MAJOR_PREFIX}/assets/sell",
          description="Create XDR to sell property tokens.",
          status_code=status.HTTP_200_OK,
          responses={**RESPONSES[422]})
def sell_property_tokens_xdr(sell_request: PropertySellRequest,
                             session_data: SessionData = Depends(get_session_data)) -> str:
    return ws.controller.sell_property_tokens_xdr(sell_request, session_data.public_key)


@app.post(f"/api/{API_MAJOR_PREFIX}/execute_transaction",
          description="Execute a transaction on the blockchain using the provided XDR.",
          status_code=status.HTTP_200_OK,
          responses={**RESPONSES[422]},
          response_model=StellarTransactionResult)
def execute_transaction(execute_trn_request: ExecuteTransactionRequest,
                        session_data: SessionData = Depends(get_session_data)) -> StellarTransactionResult:
    return ws.controller.execute_transaction(execute_trn_request.transaction_xdr)


@app.post(f"/api/{API_MAJOR_PREFIX}/debug_fill_db",
          description="Fill DB with debug data.",
          status_code=status.HTTP_200_OK,
          responses={**RESPONSES[422]})
def debug_fill_db() -> None:
    ws.controller.debug_fill_db()
    return


@app.post(f"/api/{API_MAJOR_PREFIX}/test",
          description="Test endpoint",
          response_description="Test response",
          tags=[],
          status_code=status.HTTP_200_OK,
          responses={**RESPONSES[422]},
          response_model=TestData)
async def test_endpoint(test_request_data: TestData, session_data: SessionData = Depends(get_session_data)) -> TestData:
    return TestData(number=1)


@app.post(f"/api/{API_MAJOR_PREFIX}/login",
          description="Login endpoint",
          tags=[],
          status_code=status.HTTP_200_OK,
          responses={**RESPONSES[422]})
async def login_endpoint(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    public_key = form_data.username
    if form_data.password == CONFIG.dev_access_key:
        session_data = ws.session_cache.put(public_key)
        return {"access_token": session_data.access_token, "token_type": "bearer"}
    else:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Incorrect public key or password")


"""
Serve templates from the root directory
"""


@app.get("/", include_in_schema=False)
@app.get("/{filename}", include_in_schema=False)
async def serve_frontend(request: Request, filename: Optional[str] = None):
    if filename is None:
        filename = "index.html"

    if filename == "index.html":
        ip_addr = request.headers.get('header-name')
        if ip_addr is None:
            ip_addr = request.client.host
        ws.controller.log_visit(ip_addr, "index.html")

    try:
        return ws.templates.TemplateResponse(filename, {"request": request})
    except TemplateNotFound:
        return HTTPException(status.HTTP_404_NOT_FOUND, "Asset not found")


"""
Serve remaining static files
"""
app.mount("/", StaticFiles(directory=CONFIG.frontend_static_dir), name="assets")
