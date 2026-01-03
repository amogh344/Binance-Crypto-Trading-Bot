import os
import sys
import time
from dotenv import load_dotenv
from bot import FuturesBot
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, FloatPrompt
from rich.align import Align
from rich import box


load_dotenv()
console = Console()


def get_bot():
    """Initializes the bot with a loading spinner."""
    api_key = os.getenv('BINANCE_API_KEY')
    api_secret = os.getenv('BINANCE_API_SECRET')

    if not api_key:
        console.print("[bold red]❌ Error: Keys not found in .env[/bold red]")
        sys.exit()

    with console.status("[bold green]Connecting to Binance Futures Testnet...", spinner="dots"):
        try:
            bot = FuturesBot(api_key, api_secret)
            time.sleep(1) 
            return bot
        except Exception:
            console.print("[bold red]❌ Connection Failed. Check logs.[/bold red]")
            sys.exit()

def display_dashboard(bot, symbol):
    
    with console.status("[bold cyan]Fetching Account Data...", spinner="earth"):
        balance = bot.get_balance()
        position = bot.get_position(symbol)
    
    os.system('cls' if os.name == 'nt' else 'clear')

    console.print(Panel(Align.center(f"[bold gold1]⚡ BINANCE FUTURES CLI ⚡[/bold gold1]\n[grey53]Testnet Environment • {symbol}[/grey53]"), style="bold white"))

    table = Table(show_header=True, header_style="bold magenta", box=box.ROUNDED, expand=True)
    table.add_column("💰 Wallet Balance (USDT)", justify="center")
    table.add_column("Current Position", justify="center")
    table.add_column("Entry Price", justify="center")
    table.add_column("Unrealized PnL", justify="center")

    pos_str = "[grey50]FLAT[/grey50]"
    entry_str = "-"
    pnl_str = "-"
    
    if position and position['amount'] != 0:
        color = "green" if position['pnl'] >= 0 else "red"
        pos_str = f"[{color}]{position['amount']} {position['side']}[/{color}]"
        entry_str = f"{position['entry_price']:.2f}"
        pnl_str = f"[{color}]{position['pnl']:.2f} USDT[/{color}]"

    bal_str = f"{balance:.2f}" if balance is not None else "Error"
    
    table.add_row(f"[bold green]{bal_str}[/bold green]", pos_str, entry_str, pnl_str)
    console.print(table)
    console.print("")

def print_receipt(order):
    if not order:
        console.print(Panel("[bold red]❌ Order Failed. Check trading.log for details.[/bold red]", title="Error"))
        return

    oid = order.get('orderId', 'Unknown')
    if oid == 'Unknown': 
        oid = order.get('algoId', 'Unknown')
    
    status = order.get('status', order.get('algoStatus', 'SUBMITTED'))
    side = order.get('side', 'Unknown')
    qty = order.get('quantity', order.get('origQty', '0'))
    
    grid = Table.grid(expand=True)
    grid.add_column()
    grid.add_column(justify="right")
    grid.add_row("Order ID:", str(oid))
    grid.add_row("Status:", f"[bold blue]{status}[/bold blue]")
    grid.add_row("Side:", f"[bold {'green' if side=='BUY' else 'red'}]{side}[/]")
    grid.add_row("Quantity:", str(qty))

    console.print(Panel(grid, title="[bold green]✅ Order Receipt[/bold green]", width=50))

def main():
    bot = get_bot()
    symbol = "BTCUSDT"

    while True:
        display_dashboard(bot, symbol)

        menu = Table(box=box.SIMPLE, show_header=False)
        menu.add_column("Cmd", style="cyan", no_wrap=True)
        menu.add_column("Action")
        menu.add_row("1", "Market Buy")
        menu.add_row("2", "Market Sell")
        menu.add_row("3", "Limit Order")
        menu.add_row("4", "Stop Loss (Bonus)")
        menu.add_row("5", "Refresh")
        menu.add_row("q", "Quit")
        console.print(menu)

        choice = Prompt.ask("Select Command").lower()

        if choice == 'q':
            console.print("[yellow]Exiting...[/yellow]")
            sys.exit()
        
        elif choice == '5':
            continue 


        if choice in ['1', '2', '3', '4']:
            side = ""
            if choice == '1': side = "BUY"
            if choice == '2': side = "SELL"
            

            if choice in ['1', '2']:
                qty = FloatPrompt.ask(f"Enter {side} Quantity")
                with console.status("[bold yellow]Submitting Market Order..."):
                    order = bot.place_order(symbol, side, 'MARKET', qty)
                    print_receipt(order)


            elif choice == '3':
                side = Prompt.ask("Side", choices=["BUY", "SELL"])
                qty = FloatPrompt.ask("Quantity")
                price = Prompt.ask("Limit Price")
                with console.status("[bold yellow]Submitting Limit Order..."):
                    order = bot.place_order(symbol, side, 'LIMIT', qty, price=price)
                    print_receipt(order)
            
            elif choice == '4':
                side = "SELL" 
                qty = FloatPrompt.ask("Quantity")
                stop = Prompt.ask("Trigger Price")
                with console.status("[bold red]Submitting Stop Order..."):
                    order = bot.place_order(symbol, side, 'STOP_MARKET', qty, stop_price=stop)
                    print_receipt(order)

            Prompt.ask("\n[grey50]Press Enter to continue...[/grey50]")

if __name__ == "__main__":
    main()