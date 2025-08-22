
import httpx, datetime, json, asyncio

SYMBOLS = {
    'ALTIN',
    'ONS',
    'USDKG',
    'EURKG',
    'AYAR22',
    'KULCEALTIN',
    'XAUXAG',
    'CEYREK_YENI',
    'CEYREK_ESKI',
    'YARIM_YENI',
    'YARIM_ESKI',
    'TEK_YENI',
    'TEK_ESKI',
    'ATA_YENI',
    'ATA_ESKI',
    'ATA5_YENI',
    'ATA5_ESKI',
    'GREMESE_YENI',
    'GREMESE_ESKI',
    'AYAR14',
    'GUMUSTRY',
    'XAGUSD',
    'GUMUSUSD',
    'XPTUSD',
    'XPDUSD',
    'PLATIN',
    'PALADYUM'
}

class SymbolNotFoundError(Exception): pass

URL = "https://www.haremaltin.com/ajax/cur/history"
HEADERS = {
    "Accept": "application/json",
    "X-Requested-With": "XMLHttpRequest",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "https://www.haremaltin.com",
    "Referer": "https://www.haremaltin.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36"
}

async def fetch_symbol(client, symbol, minute=1):
    now = datetime.datetime.now()
    data = {
        "interval": "dakika",
        "kod": symbol,
        "dil_kodu": "tr",
        "tarih1": (now - datetime.timedelta(minutes=minute)).strftime("%Y-%m-%d %H:%M:%S"),
        "tarih2": now.strftime("%Y-%m-%d %H:%M:%S"),
    }
    try:
        r = await client.post(URL, data=data, headers=HEADERS)
        r.raise_for_status()
        return {symbol: r.json()}
    except Exception as e:
        return {symbol: {"error": str(e)}}

async def get_price(symbols: str, minute=1):
    req = [s.strip().upper() for s in symbols.split(",") if s.strip()]
    invalid = [s for s in req if s not in SYMBOLS]
    if invalid:
        raise SymbolNotFoundError(f"Geçersiz semboller: {', '.join(invalid)}")
    async with httpx.AsyncClient(timeout=15) as client:
        results = await asyncio.gather(*(fetch_symbol(client, s, minute) for s in req))
        out = {}
        for r in results: out.update(r)
        return out

async def main():
    try:
        data = await get_price("KULCEALTIN,ONS", minute=1)
        print(json.dumps(data, indent=2, ensure_ascii=False))
    except SymbolNotFoundError as e:
        print(f"Hata: {e}")

if __name__ == "__main__":
    asyncio.run(main())
