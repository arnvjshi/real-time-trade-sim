import tkinter as tk
from tkinter import ttk
import threading
import asyncio
from main import orderbook_client, process_data

class TradeSimulatorUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Crypto Trade Simulator")
        self.root.geometry("900x400")

        self.setup_ui()

        # Start WebSocket client in background thread
        threading.Thread(target=lambda: asyncio.run(orderbook_client(self.update_from_stream)), daemon=True).start()

    def setup_ui(self):
        self.left_frame = tk.Frame(self.root, width=300)
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        self.right_frame = tk.Frame(self.root)
        self.right_frame.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH, padx=10, pady=10)

        # Input Panel
        tk.Label(self.left_frame, text="Exchange:").pack(anchor='w')
        self.exchange = ttk.Combobox(self.left_frame, values=["OKX"])
        self.exchange.set("OKX")
        self.exchange.pack(fill='x')

        tk.Label(self.left_frame, text="Asset:").pack(anchor='w')
        self.asset = ttk.Combobox(self.left_frame, values=["BTC-USDT-SWAP"])
        self.asset.set("BTC-USDT-SWAP")
        self.asset.pack(fill='x')

        tk.Label(self.left_frame, text="Order Type:").pack(anchor='w')
        self.order_type = ttk.Combobox(self.left_frame, values=["market"])
        self.order_type.set("market")
        self.order_type.pack(fill='x')

        tk.Label(self.left_frame, text="Quantity (USD):").pack(anchor='w')
        self.quantity = tk.Entry(self.left_frame)
        self.quantity.insert(0, "100")
        self.quantity.pack(fill='x')

        # Output Panel
        self.output_text = tk.Text(self.right_frame, height=20)
        self.output_text.pack(fill='both', expand=True)

    def update_from_stream(self, data, tick_time):
        import io
        import sys
        buffer = io.StringIO()
        sys.stdout = buffer
        process_data(data, tick_time)
        sys.stdout = sys.__stdout__
        self.output_text.insert(tk.END, buffer.getvalue())
        self.output_text.see(tk.END)

    def ui_run():
        root = tk.Tk()
        app = TradeSimulatorUI(root)
        root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = TradeSimulatorUI(root)
    root.mainloop()

    
