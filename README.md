# Real Time Trade Sim

A high-performance cryptocurrency trade simulator that leverages real-time Level 2 orderbook data from OKX to estimate transaction costs including slippage, fees, and market impact.

## Features

- Connects to OKX's real-time L2 orderbook via WebSocket.
- Calculates expected slippage using regression models.
- Estimates trading fees based on exchange fee tiers.
- Implements Almgren-Chriss market impact model.
- Predicts maker/taker trade proportions.
- Displays detailed metrics and latency in a Tkinter GUI.
- Modular architecture with logging and error handling.

## Installation

1. Clone the repository:

```bash
git clone https://github.com/arnvjshi/real-time-trade-sim.git
cd real-time-trade-sim
````

2. Install required packages:

```bash
pip install -r requirements.txt
```

## Usage

Run the main application:

```bash
python main.py
```

Adjust input parameters on the left panel and monitor output metrics on the right panel.

## Project Structure

* `main.py` — Entry point to start the WebSocket client and data processing loop.
* `simulator_ui.py` — Tkinter-based user interface.
* `websocket/` — WebSocket client handling real-time data streaming.
* `models/` — Implementation of slippage, fee, and market impact models.
* `utils/` — Logger and utility functions.

## Dependencies

* Python 3.9+
* websockets
* numpy
* scikit-learn
* tkinter (usually included with Python)

## License

MIT License

## Acknowledgements

* OKX for providing public API endpoints.
* Almgren and Chriss for market impact modeling.
  

---