import asyncio
import threading
import time
from datetime import datetime
from models.fee_model import calculate_fee
from models.market_impact import almgren_chriss_impact
from models.slippage_model import SlippageModel
from websocket.l2_orderbook_client import orderbook_client
from utils.logger import setup_logger

logger = setup_logger()

# Initialize the Slippage model once
slippage_model = SlippageModel()

# Global state to track processing latency
last_tick_time = None
processing_start = None

async def process_data(data, tick_time):
    global last_tick_time, processing_start
    last_tick_time = tick_time
    processing_start = time.perf_counter()

    # Extract data
    bids = data.get("bids", [])
    asks = data.get("asks", [])
    symbol = data.get("symbol", "")
    exchange = data.get("exchange", "")

    # For demo, fixed inputs; ideally fetch from UI input panel
    order_type = "market"
    quantity_usd = 100.0
    fee_tier = 0.001  # 0.1%
    daily_volume = 1_000_000_000  # example, replace with real data
    volatility = 0.02  # 2% daily volatility

    # Compute expected fees
    expected_fees = calculate_fee(quantity_usd, fee_tier)

    # Compute market impact
    market_impact = almgren_chriss_impact(quantity_usd, daily_volume, volatility)

    # Estimate slippage
    slippage = slippage_model.predict(quantity_usd)

    # Net cost
    net_cost = expected_fees + market_impact + slippage

    # Maker/Taker proportion (placeholder, e.g. 60% taker)
    maker_taker_ratio = "Maker: 40%, Taker: 60%"

    # Latency
    processing_end = time.perf_counter()
    internal_latency_ms = (processing_end - processing_start) * 1000

    # Compose output text
    output = (
        f"Symbol: {symbol}\n"
        f"Exchange: {exchange}\n"
        f"Order Type: {order_type}\n"
        f"Quantity (USD): {quantity_usd}\n"
        f"Expected Slippage: ${slippage:.2f}\n"
        f"Expected Fees: ${expected_fees:.2f}\n"
        f"Expected Market Impact: ${market_impact:.2f}\n"
        f"Net Cost: ${net_cost:.2f}\n"
        f"Maker/Taker Proportion: {maker_taker_ratio}\n"
        f"Internal Latency (ms): {internal_latency_ms:.2f}\n"
        f"Tick Timestamp: {tick_time}\n"
        f"{'-'*40}\n"
    )

    print(output)

def start_loop(loop):
    """Run the asyncio loop in a new thread."""
    asyncio.set_event_loop(loop)
    loop.run_forever()

def start_websocket_client(callback):
    """Start the websocket client in asyncio loop."""
    new_loop = asyncio.new_event_loop()
    t = threading.Thread(target=start_loop, args=(new_loop,), daemon=True)
    t.start()

    # Schedule the client coroutine on the new loop
    asyncio.run_coroutine_threadsafe(orderbook_client(callback), new_loop)

def update_callback(data, tick_time):
    # Wrapper for async call inside asyncio event loop
    asyncio.run_coroutine_threadsafe(process_data(data, tick_time), asyncio.get_event_loop())

if __name__ == "__main__":
    # Start websocket client
    # Using a wrapper so that process_data is called asynchronously
    # Because the UI runs on main thread, you may want to modify UI to accept these updates
    def callback(data, tick_time):
        asyncio.run(process_data(data, tick_time))

    print("Starting Trade Simulator Main...")
    # Run websocket client in background thread with callback
    start_websocket_client(callback)

    # To keep main thread alive for demo (replace with UI mainloop later)
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Shutting down...")
