import asyncio
import websockets
import json
import time
import numpy as np
from sklearn.linear_model import LinearRegression, LogisticRegression

# Model classes
class SlippageModel:
    def __init__(self):
        self.model = LinearRegression()

    def train(self, X, y):
        self.model.fit(X, y)

    def predict(self, X):
        return self.model.predict(X)

class MarketImpactModel:
    def __init__(self, eta=0.1, lambd=0.01):
        self.eta = eta
        self.lambd = lambd

    def calculate_impact(self, Q, volatility):
        return self.eta * Q + 0.5 * self.lambd * (volatility ** 2) * (Q ** 2)

class FeeModel:
    def __init__(self, fee_rate=0.001):
        self.fee_rate = fee_rate

    def calculate_fee(self, Q, price):
        return self.fee_rate * Q * price

class MakerTakerModel:
    def __init__(self):
        self.model = LogisticRegression()

    def train(self, X, y):
        self.model.fit(X, y)

    def predict_proba(self, X):
        return self.model.predict_proba(X)

# WebSocket handler
async def orderbook_client(callback):
    url = "wss://ws.gomarket-cpp.goquant.io/ws/l2-orderbook/okx/BTC-USDT-SWAP"
    async with websockets.connect(url) as ws:
        while True:
            msg = await ws.recv()
            tick_time = time.perf_counter()
            data = json.loads(msg)
            callback(data, tick_time)

# Callback function
models = {
    "slippage": SlippageModel(),
    "impact": MarketImpactModel(),
    "fee": FeeModel(),
    "maker_taker": MakerTakerModel()
}

def process_data(data, tick_time):
    # Simplified example
    bids = data.get("bids", [])
    asks = data.get("asks", [])
    if not bids or not asks:
        return

    mid_price = (float(bids[0][0]) + float(asks[0][0])) / 2
    quantity = 100 / mid_price
    volatility = 0.01  # Placeholder, should be computed

    fee = models["fee"].calculate_fee(quantity, mid_price)
    impact = models["impact"].calculate_impact(quantity, volatility)

    # Placeholder input for slippage and maker/taker
    X_sample = np.array([[volatility, quantity]])
    slippage = models["slippage"].predict(X_sample)[0] if hasattr(models["slippage"], 'model') else 0
    maker_taker = models["maker_taker"].predict_proba(X_sample)[0] if hasattr(models["maker_taker"], 'model') else [0.5, 0.5]

    net_cost = fee + impact + slippage

    latency = time.perf_counter() - tick_time

    print(f"Mid Price: {mid_price:.2f}, Quantity: {quantity:.6f}, Fee: {fee:.4f}, Impact: {impact:.4f}, Slippage: {slippage:.4f}, Net Cost: {net_cost:.4f}, Maker Prob: {maker_taker[0]:.2f}, Taker Prob: {maker_taker[1]:.2f}, Latency: {latency*1000:.2f}ms")

# Entry point
if __name__ == "__main__":
    asyncio.run(orderbook_client(process_data))
