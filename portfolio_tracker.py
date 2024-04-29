import tkinter as tk
from tkinter import messagebox
import requests

class StockPortfolioGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Stock Portfolio Tracker")

        self.portfolio = {}

        self.label_symbol = tk.Label(master, text="Stock Symbol:")
        self.label_symbol.grid(row=0, column=0, padx=5, pady=5)
        self.entry_symbol = tk.Entry(master)
        self.entry_symbol.grid(row=0, column=1, padx=5, pady=5)

        self.label_quantity = tk.Label(master, text="Quantity:")
        self.label_quantity.grid(row=1, column=0, padx=5, pady=5)
        self.entry_quantity = tk.Entry(master)
        self.entry_quantity.grid(row=1, column=1, padx=5, pady=5)

        self.add_button = tk.Button(master, text="Add Stock", command=self.add_stock)
        self.add_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

        self.remove_button = tk.Button(master, text="Remove Stock", command=self.remove_stock)
        self.remove_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

        self.track_button = tk.Button(master, text="Track Portfolio", command=self.track_portfolio)
        self.track_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

        self.result_text = tk.Text(master, height=10, width=50)
        self.result_text.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

    def add_stock(self):
        symbol = self.entry_symbol.get().strip().upper()
        quantity = self.entry_quantity.get().strip()
        if symbol and quantity.isdigit():
            quantity = int(quantity)
            if symbol in self.portfolio:
                self.portfolio[symbol] += quantity
            else:
                self.portfolio[symbol] = quantity
            self.entry_symbol.delete(0, tk.END)
            self.entry_quantity.delete(0, tk.END)
            messagebox.showinfo("Success", f"{quantity} shares of {symbol} added to portfolio.")
        else:
            messagebox.showerror("Error", "Please enter valid stock symbol and quantity.")

    def remove_stock(self):
        symbol = self.entry_symbol.get().strip().upper()
        quantity = self.entry_quantity.get().strip()
        if symbol and quantity.isdigit():
            quantity = int(quantity)
            if symbol in self.portfolio:
                if quantity >= self.portfolio[symbol]:
                    del self.portfolio[symbol]
                else:
                    self.portfolio[symbol] -= quantity
                self.entry_symbol.delete(0, tk.END)
                self.entry_quantity.delete(0, tk.END)
                messagebox.showinfo("Success", f"{quantity} shares of {symbol} removed from portfolio.")
            else:
                messagebox.showerror("Error", "Stock not found in portfolio.")
        else:
            messagebox.showerror("Error", "Please enter valid stock symbol and quantity.")

    def track_portfolio(self):
        self.result_text.delete(1.0, tk.END)
        total_value = 0
        for symbol, quantity in self.portfolio.items():
            price = self.get_stock_price(symbol)
            if price is not None:
                total_value += price * quantity
                self.result_text.insert(tk.END, f"{symbol}: {quantity} shares - ${price:.2f}\n")
            else:
                self.result_text.insert(tk.END, f"Error: Failed to fetch data for {symbol}\n")
        self.result_text.insert(tk.END, f"\nTotal Portfolio Value: ${total_value:.2f}")

    def get_stock_price(self, symbol):
        # Replace 'YOUR_API_KEY' with your Alpha Vantage API key
        api_key = 'BQ2VAJO73L1TJYEP'
        url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={api_key}'
        try:
            response = requests.get(url)
            data = response.json()
            if 'Global Quote' in data:
                return float(data['Global Quote']['05. price'])
            else:
                return None
        except Exception as e:
            print(e)
            return None

def main():
    root = tk.Tk()
    app = StockPortfolioGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
