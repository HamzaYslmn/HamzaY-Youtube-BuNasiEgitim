from fastapi import APIRouter
from fastapi.responses import JSONResponse
import modules.haremaltin.xScraperRest as xScraper

router = APIRouter(tags=["Currency"])

@router.get("/get_currency/{symbols}", summary="Get currency prices")
async def get_currency(symbols: str):
    try:
        data = await xScraper.get_price(symbols)
        return JSONResponse(content=data)
    except xScraper.SymbolNotFoundError as e:
        return JSONResponse(status_code=404, content={"error": str(e)})