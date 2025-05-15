import asyncio
import websockets
import json
from utils.logger import setup_logger

logger = setup_logger("L2OrderbookClient")

async def orderbook_client(callback, symbol="BTC-USDT-SWAP"):
    url = f"wss://ws.gomarket-cpp.goquant.io/ws/l2-orderbook/okx/{symbol}"
    try:
        async with websockets.connect(url) as ws:
            logger.info(f"Connected to {url}")

            async for message in ws:
                data = json.loads(message)
                timestamp = data.get("timestamp")
                if data.get("exchange") == "OKX" and data.get("symbol") == symbol:
                    # Send data to callback for processing and UI update
                    await callback(data, timestamp)
                else:
                    logger.warning("Received unexpected message or symbol")

    except (websockets.ConnectionClosed, asyncio.CancelledError):
        logger.warning("WebSocket connection closed")
    except Exception as e:
        logger.error(f"WebSocket client error: {e}")

# Example usage:
# asyncio.run(orderbook_client(your_callback_function))
