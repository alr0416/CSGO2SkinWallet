import requests
from urllib.parse import quote
import time
import re
from collections import defaultdict
import tkinter as tk
from tkinter import messagebox, ttk

APP_ID = 730
CONTEXT_ID = 2

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; PriceChecker/1.0)"
}

def get_inventory_descriptions(steam_id):
    url = f"https://steamcommunity.com/inventory/{steam_id}/{APP_ID}/{CONTEXT_ID}?l=english"
    try:
        resp = requests.get(url, headers=HEADERS)
        resp.raise_for_status()
        data = resp.json()
        return data.get("descriptions", [])
    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch inventory:\n{e}")
        return []

def get_price_from_market_page(market_hash_name):
    encoded_name = quote(market_hash_name)
    url = f"https://steamcommunity.com/market/listings/{APP_ID}/{encoded_name}"
    try:
        resp = requests.get(url, headers=HEADERS)
        if resp.status_code == 429:
            print("❌ Rate limited (429).")
            return None
        elif resp.status_code != 200:
            print(f"❌ HTTP {resp.status_code} error.")
            return None

        html = resp.text
        prices = re.findall(r'<span class="market_listing_price market_listing_price_with_fee">\s*\$([\d\.,]+)', html)
        if prices:
            return float(prices[0].replace(",", ""))
    except Exception as e:
        print(f"❌ Error fetching price for '{market_hash_name}': {e}")
    return None

def calculate_inventory_value(steam_id):
    descriptions = get_inventory_descriptions(steam_id)
    item_counts = defaultdict(int)

    for desc in descriptions:
        name = desc.get("market_hash_name")
        if name:
            item_counts[name] += 1

    total_value = 0.0
    for name, count in item_counts.items():
        price = get_price_from_market_page(name)
        if price is None:
            print(f"❌ Price not found for '{name}'")
        else:
            subtotal = price * count
            print(f"✅ {name} x{count} @ ${price:.2f} → ${subtotal:.2f}")
            total_value += subtotal
        time.sleep(1.25)

    return total_value

def run_inventory_check():
    steam_id = steam_entry.get().strip()
    if not steam_id.isdigit() or len(steam_id) < 17:
        messagebox.showwarning("Invalid Input", "Please enter a valid 17-digit SteamID64.")
        return

    result_label.config(text="⏳ Calculating, please wait...")
    disclaimer_label.config(text="")
    root.update()

    total = calculate_inventory_value(steam_id)
    result_label.config(text=f"💰 Total Inventory Value: ${total:.2f}")
    disclaimer_label.config(text="🕐 Note: Recently purchased skins may take up to 10 days to appear.")

# GUI setup
root = tk.Tk()
root.title("Steam Inventory Value Checker")
root.geometry("550x350")
root.configure(bg="#0e1a2b")  # Navy Blue

style = ttk.Style()
style.theme_use("clam")

# Orange: #ffae00
# Darker orange for hover: #cc8a00

style.configure("TButton",
                font=("Segoe UI", 12),
                padding=10,
                background="#ffae00",
                foreground="#0e1a2b",
                borderwidth=0)
style.map("TButton",
          background=[("active", "#cc8a00")],
          foreground=[("active", "#ffffff")])

style.configure("TLabel",
                background="#0e1a2b",
                foreground="#ffffff",
                font=("Segoe UI", 12))

style.configure("TEntry",
                padding=6,
                font=("Segoe UI", 11),
                fieldbackground="#ffffff")

# Title
title_label = ttk.Label(root, text="🎮 Steam Inventory Value Checker", font=("Segoe UI Bold", 18), foreground="#ffae00")
title_label.pack(pady=(20, 10))

# Steam ID input
input_frame = tk.Frame(root, bg="#0e1a2b")
input_frame.pack(pady=10)

ttk.Label(input_frame, text="Enter your 17-digit SteamID64:").pack()
steam_entry = ttk.Entry(input_frame, width=42)
steam_entry.pack(pady=6)

# Check button
check_button = ttk.Button(root, text="Check Inventory Value", command=run_inventory_check)
check_button.pack(pady=20)

# Result label
result_label = ttk.Label(root, text="", font=("Segoe UI", 14, "bold"), foreground="#ffae00")
result_label.pack()

# Disclaimer label
disclaimer_label = ttk.Label(root, text="", font=("Segoe UI", 10), foreground="#cccccc")
disclaimer_label.pack(pady=(10, 0))

# Footer
footer_label = ttk.Label(root, text="Powered by Steam Market Data", font=("Segoe UI", 9), foreground="#888888")
footer_label.pack(side="bottom", pady=10)

root.mainloop()
