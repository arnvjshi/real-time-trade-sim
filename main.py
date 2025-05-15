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
slippage_model = SlippageModel()

async def process_data(data, tick_time):
    # ... your process_data code here, same as you wrote ...
    bids = data.get("bids", [])
    asks = data.get("asks", [])
    symbol = data.get("symbol", "")
    exchange = data.get("exchange", "")

    order_type = "market"
    quantity_usd = 100.0
    fee_tier = 0.001
    daily_volume = 1_000_000_000
    volatility = 0.02

    expected_fees = calculate_fee(quantity_usd, fee_tier)
    market_impact = almgren_chriss_impact(quantity_usd, daily_volume, volatility)
    slippage = slippage_model.predict(quantity_usd)
    net_cost = expected_fees + market_impact + slippage
    maker_taker_ratio = "Maker: 40%, Taker: 60%"

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
        f"Tick Timestamp: {tick_time}\n"
        f"{'-'*40}\n"
    )
    print(output)

def start_loop(loop):
    """Start and run asyncio event loop forever."""
    asyncio.set_event_loop(loop)
    loop.run_forever()

def main():
    # Create a new event loop for the websocket client
    new_loop = asyncio.new_event_loop()
    thread = threading.Thread(target=start_loop, args=(new_loop,), daemon=True)
    thread.start()

    # Define the callback to process data
    def callback(data, tick_time):
        # Schedule process_data coroutine in the new event loop
        asyncio.run_coroutine_threadsafe(process_data(data, tick_time), new_loop)

    # Schedule websocket client to run in the new event loop
    asyncio.run_coroutine_threadsafe(orderbook_client(callback), new_loop)

    print("Trade Simulator started. Press Ctrl+C to stop.")
    try:
        while True:
            time.sleep(1)  # Keep main thread alive
    except KeyboardInterrupt:
        print("Shutting down...")

if __name__ == "__main__":
    main()
