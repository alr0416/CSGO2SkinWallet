# 🎮 Steam Inventory Value Checker

A desktop GUI app built with **Python + Tkinter** that allows users to **calculate the total market value of their Steam inventory** (specifically for CS:GO items). It fetches real-time prices from the **Steam Community Market** and displays the combined value of all owned items.

---

## 🧩 Features

- 🎯 Accepts **SteamID64** (17-digit ID) to fetch inventory
- 💰 Calculates **total value** using real-time prices from the Steam Market
- 🧠 Shows item quantity, price per item, and total per line

---

## 🚀 How to Run

### 1. 📦 Requirements

Make sure Python **3.7 or later** is installed.




```bash
python3 --version
```

---

### 2. 📥 Install Dependencies

Install the required Python module:

```bash
pip install requests
```


---

### 3. ▶️ Run the App

run:

```bash
python cs_inventory_checker.py
```

This will launch a desktop window. Paste your **SteamID64** and click “Check Inventory Value.”

---

## 📝 Notes

- 🔐 You **do not need to log in** to view your inventory (it must be public).
- 🎒 Recently purchased or traded items may take **up to 10 days** to appear via the API.
- ⏱️ Steam may **rate-limit** requests. The app handles this with built-in delays.

---

## 📁 Example SteamID64

```
12345678912345678
```

> You can find your SteamID64 from your Steam profile URL or use a converter like [steamid.io](https://steamid.io/).
