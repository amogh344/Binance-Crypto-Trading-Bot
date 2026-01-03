Perfect — below is a fully corrected, professional README.md written 100% in proper Markdown, with ALL steps included, clean headings, code blocks, and GitHub-ready formatting.

👉 Delete your current README.md and paste this exactly as-is.

⸻


# 🤖 Binance Futures Trading Bot (Testnet)

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![Binance API](https://img.shields.io/badge/Binance-Futures_Testnet-yellow.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

A professional, modular crypto trading bot designed for the **Binance Futures Testnet (USDT-M)**.  
This project demonstrates a production-ready backend architecture with CLI interaction, logging, and robust error handling.

---

## 🚀 Features

### Core Functionality
- **Futures Trading:** Places orders on the `USDT-M` Binance Futures Testnet
- **Order Types:** Market, Limit, and Stop-Market orders
- **Order Sides:** Buy and Sell supported
- **Wallet Balance:** Fetch and display USDT balance
- **Execution Feedback:** Outputs order status and execution details

### Advanced / Bonus Features
- **Interactive CLI Dashboard:** Enhanced terminal UI using `rich`
- **Stop-Loss Support:** Risk management via `STOP_MARKET` orders
- **Comprehensive Logging:** All API requests, responses, and errors logged to `trading.log`

---

## 🛠️ Installation & Setup

You can run this bot locally using Python.

### Prerequisites
- Python **3.8+**
- A **Binance Futures Testnet (USDT-M)** account  
  👉 https://testnet.binancefuture.com

---

## 📥 Step 1: Clone the Repository

```bash
git clone https://github.com/amogh344/Binance-Crypto-Trading-Bot.git
cd Binance-Crypto-Trading-Bot
```


## 🔐 Step 2: Configure API Credentials

Create a .env file in the project root directory.
⚠️ Never commit this file to GitHub.
```bash
BINANCE_API_KEY=your_testnet_api_key 
BINANCE_API_SECRET=your_testnet_api_secret
```


## 📦 Step 3: Set Up Python Environment

### Create a virtual environment (recommended)
```
python -m venv venv
```

### Activate virtual environment
```
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows
```



## 📚 Step 4: Install Dependencies

```
pip install -r requirements.txt
```
Dependencies include:
	•	python-binance
	•	rich
	•	python-dotenv


## ▶️ Step 5: Run the Trading Bot

```
python main.py
```



📂 Project Structure
```
├── bot.py             # Core trading logic and Binance Futures API wrapper
├── main.py            # CLI interface and user input validation
├── requirements.txt   # Python dependencies
├── .env               # API credentials (excluded from git)
└── trading.log        # Detailed API request/response logs

```


🖥️ Usage Overview
```
Once started, the CLI provides a menu-driven interface to:
	1.	Place Market Buy/Sell orders
	2.	Place Limit Orders at custom prices
	3.	Configure Stop-Loss (Stop-Market) orders
	4.	View wallet balance and order execution status
	5.	Monitor real-time feedback and errors
```


📝 Logging

All API interactions are logged in:
```
trading.log
```
Logs include:
```
   • Request payloads
   • API responses
   • Errors and exceptions
   • Order execution details
```

This ensures auditability and debugging support.



#### ⚠️ Disclaimer

This software is intended strictly for educational and evaluation purposes
and operates only on the Binance Futures Testnet.

#### ⚠️ Do NOT use this code with real funds without proper risk controls, audits, and safeguards.
