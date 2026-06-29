import urllib.request
import json
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Commodity-Market-Server")

TICKERS = {
    "corn": "ZC=F",
    "wheat": "ZW=F",
    "soybeans": "ZS=F"
}

@mcp.tool()
async def fetch_commodity_price(commodity: str) -> dict:
    """Fetch commodity market rates and trend indicators for crops.

    Args:
        commodity: Crop name (corn, wheat, soybeans).
    """
    name = commodity.lower().strip()
    if name not in TICKERS:
        return {"status": "error", "message": f"Unsupported commodity '{commodity}'. Use corn, wheat, or soybeans."}
        
    ticker = TICKERS[name]
    try:
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        res = urllib.request.urlopen(req, timeout=5)
        data = json.loads(res.read().decode())
        
        meta = data['chart']['result'][0]['meta']
        raw_price = meta['regularMarketPrice']
        
        usd_price = round(raw_price / 100.0, 2)
        
        prev_close = meta.get('chartPreviousClose', raw_price)
        change_pct = round(((raw_price - prev_close) / prev_close) * 100, 2)
        trend = "up" if change_pct >= 0 else "down"
        
        return {
            "commodity": name,
            "price_usd": usd_price,
            "unit": "bushel",
            "ticker": ticker,
            "change_percent": change_pct,
            "trend": trend,
            "source": "Yahoo Finance Real-Time Futures API"
        }
    except Exception as e:
        fallback_rates = {"corn": 4.50, "wheat": 6.12, "soybeans": 11.20}
        return {
            "commodity": name,
            "price_usd": fallback_rates[name],
            "unit": "bushel",
            "note": f"Fallback simulated rates (Real API error: {e})",
            "trend": "up"
        }
