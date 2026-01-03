# import logging
# import os
# from binance.client import Client

# # --- Handle different library versions for errors ---
# try:
#     from binance.exceptions import BinanceAPIException
# except ImportError:
#     from binance.error import BinanceAPIException, ClientError

# # --- Configure Logging ---
# logging.basicConfig(
#     level=logging.INFO,
#     format='%(asctime)s - %(levelname)s - %(message)s',
#     handlers=[
#         logging.FileHandler("trading.log"), 
#         logging.StreamHandler()             
#     ]
# )

# class FuturesBot:
#     def __init__(self, api_key, api_secret):
#         try:
#             # Initialize Client for Futures Testnet
#             self.client = Client(api_key, api_secret, testnet=True)
#             logging.info("Connected to Binance Futures Testnet.")
#         except Exception as e:
#             logging.error(f"Failed to connect: {e}")
#             raise

#     def get_balance(self):
#         """Fetch USDT balance from Futures wallet."""
#         try:
#             balances = self.client.futures_account_balance()
#             for b in balances:
#                 if b['asset'] == 'USDT':
#                     return float(b['balance'])
#             return 0.0
#         except Exception as e:
#             logging.error(f"Error fetching balance: {e}")
#             return None

#     def place_order(self, symbol, side, order_type, quantity, price=None, stop_price=None):
#         """Place a Futures Order (Market, Limit, or Stop)."""
#         try:
#             params = {
#                 'symbol': symbol,
#                 'side': side.upper(),
#                 'type': order_type.upper(),
#                 'quantity': quantity,
#             }

#             # Add extra parameters based on order type
#             if order_type.upper() == 'LIMIT':
#                 if not price: return None
#                 params['price'] = price
#                 params['timeInForce'] = 'GTC'

#             elif order_type.upper() == 'STOP_MARKET':
#                 if not stop_price: return None
#                 params['stopPrice'] = stop_price

#             logging.info(f"Sending Order: {params}")
            
#             # Execute the order on Binance Futures
#             order = self.client.futures_create_order(**params)
            
#             # Log the full response (Great for debugging and evidence)
#             logging.info(f"Binance Response: {order}")
            
#             # Safely grab the Order ID (prevents crashing if key is missing)
#             order_id = order.get('orderId', 'Unknown ID')
#             status = order.get('status', 'Unknown Status')
            
#             logging.info(f"Order Placed Successfully: ID {order_id} - Status: {status}")
#             return order

#         except Exception as e:
#             logging.error(f"Order Failed: {e}")
#             return None

#---------------------#---------------------#---------------------#---------------------#---------------------


#---------------------test---------------------
import logging
import os
from binance.client import Client

# --- Handle different library versions for errors ---
try:
    from binance.exceptions import BinanceAPIException
except ImportError:
    from binance.error import BinanceAPIException, ClientError

# --- Configure Logging ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("trading.log"), 
        logging.StreamHandler()             
    ]
)

class FuturesBot:
    def __init__(self, api_key, api_secret):
        try:
            # Initialize Client for Futures Testnet
            self.client = Client(api_key, api_secret, testnet=True)
            logging.info("Connected to Binance Futures Testnet.")
        except Exception as e:
            logging.error(f"Failed to connect: {e}")
            raise

    def get_balance(self):
        """Fetch USDT balance from Futures wallet."""
        try:
            balances = self.client.futures_account_balance()
            for b in balances:
                if b['asset'] == 'USDT':
                    return float(b['balance'])
            return 0.0
        except Exception as e:
            logging.error(f"Error fetching balance: {e}")
            return None

    def get_position(self, symbol):
        """Fetch current open position for a specific symbol."""
        try:
            positions = self.client.futures_position_information()
            for p in positions:
                if p['symbol'] == symbol:
                    amt = float(p['positionAmt'])
                    entry = float(p['entryPrice'])
                    unrealized_pnl = float(p['unRealizedProfit'])
                    return {
                        'amount': amt,
                        'entry_price': entry,
                        'pnl': unrealized_pnl,
                        'side': 'LONG' if amt > 0 else 'SHORT' if amt < 0 else 'FLAT'
                    }
            return None
        except Exception as e:
            logging.error(f"Error fetching position: {e}")
            return None

    def place_order(self, symbol, side, order_type, quantity, price=None, stop_price=None):
        """Place a Futures Order (Market, Limit, or Stop)."""
        try:
            params = {
                'symbol': symbol,
                'side': side.upper(),
                'type': order_type.upper(),
                'quantity': quantity,
            }

            # Add extra parameters based on order type
            if order_type.upper() == 'LIMIT':
                if not price: return None
                params['price'] = price
                params['timeInForce'] = 'GTC'

            elif order_type.upper() == 'STOP_MARKET':
                if not stop_price: return None
                params['stopPrice'] = stop_price

            logging.info(f"Sending Order: {params}")
            
            # Execute the order on Binance Futures
            order = self.client.futures_create_order(**params)
            
            # Log the full response (Great for debugging and evidence)
            logging.info(f"Binance Response: {order}")
            
            # Safely grab the Order ID (prevents crashing if key is missing)
            # Stop orders use 'algoId', Normal orders use 'orderId'
            order_id = order.get('orderId', order.get('algoId', 'Unknown ID'))
            status = order.get('status', order.get('algoStatus', 'Unknown Status'))
            
            logging.info(f"Order Placed Successfully: ID {order_id} - Status: {status}")
            return order

        except Exception as e:
            logging.error(f"Order Failed: {e}")
            return None