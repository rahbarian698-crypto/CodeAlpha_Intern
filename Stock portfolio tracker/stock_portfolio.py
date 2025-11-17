import os
import pandas as pd
import yfinance as yf

# Portfolio CSV file
PORTFOLIO_FILE = "portfolio.csv"

# Load or create portfolio
if os.path.exists(PORTFOLIO_FILE):
    portfolio = pd.read_csv(PORTFOLIO_FILE)
    for col in ["Stock", "Shares", "BuyPrice"]:
        if col not in portfolio.columns:
            portfolio[col] = []
else:
    portfolio = pd.DataFrame(columns=["Stock", "Shares", "BuyPrice"])

# Company name → ticker mapping
company_tickers = {
    "Apple": "AAPL",
    "Microsoft": "MSFT",
    "Amazon": "AMZN",
    "Tesla": "TSLA",
    "Google": "GOOGL",
    "Meta": "META",
    "Netflix": "NFLX",
    "NVIDIA": "NVDA",
    "Intel": "INTC",
    "Coca Cola": "KO",
    "Pepsi": "PEP",
    "Disney": "DIS"
}

# Fetch current price for ticker
def fetch_price(ticker):
    try:
        ticker_obj = yf.Ticker(ticker)
        price = ticker_obj.history(period="1d")["Close"].iloc[0]
        return round(price, 2)
    except Exception:
        return None

# Add stock to portfolio
def add_stock():
    global portfolio
    company_name = input("Enter company name (e.g., Apple): ").strip().title()
    ticker = company_tickers.get(company_name)
    if not ticker:
        print("Company not supported or not found.")
        return

    try:
        shares = int(input("Enter number of shares: "))
    except ValueError:
        print("Invalid number of shares.")
        return

    current_price = fetch_price(ticker)
    if current_price is None:
        print("Could not fetch current price.")
        return

    # Update if already exists
    if ticker in portfolio["Stock"].values:
        portfolio.loc[portfolio["Stock"] == ticker, "Shares"] += shares
        portfolio.loc[portfolio["Stock"] == ticker, "BuyPrice"] = current_price
    else:
        new_row = pd.DataFrame([[ticker, shares, current_price]], columns=portfolio.columns)
        portfolio = pd.concat([portfolio, new_row], ignore_index=True)

    portfolio.to_csv(PORTFOLIO_FILE, index=False)
    print(f"{company_name} ({ticker}) added/updated at price ${current_price}.")

# View portfolio and market overview
def view_portfolio():
    if portfolio.empty:
        print("Portfolio is empty.")
        return

    # Prepare portfolio summary
    stock_data = []
    total_invested = 0
    total_current = 0

    for idx, row in portfolio.iterrows():
        current_price = fetch_price(row["Stock"])
        invested = row["Shares"] * row["BuyPrice"]
        current_value = row["Shares"] * current_price
        pl = current_value - invested
        pl_percent = (pl / invested) * 100 if invested != 0 else 0

        stock_data.append({
            "Stock": row["Stock"],
            "Shares": row["Shares"],
            "Invested": invested,
            "Current Value": current_value,
            "P/L($)": pl,
            "P/L(%)": pl_percent
        })

        total_invested += invested
        total_current += current_value

    # Allocation %
    for s in stock_data:
        s["Allocation %"] = (s["Invested"] / total_invested * 100) if total_invested != 0 else 0

    # Print user portfolio
    print("\n================ USER PORTFOLIO =================")
    print(f"{'Stock':<8}{'Shares':<8}{'Invested':<12}{'Current':<12}{'P/L($)':<12}{'P/L(%)':<10}{'Allocation %':<12}")
    print("-"*90)
    for s in stock_data:
        print(f"{s['Stock']:<8}{s['Shares']:<8.2f}{s['Invested']:<12.2f}{s['Current Value']:<12.2f}{s['P/L($)']:<12.2f}{s['P/L(%)']:<10.2f}{s['Allocation %']:<12.2f}")

    overall_percent = ((total_current - total_invested) / total_invested * 100) if total_invested != 0 else 0
    print("-"*90)
    print(f"{'TOTAL':<16}{total_invested:<12.2f}{total_current:<12.2f}{(total_current-total_invested):<12.2f}{overall_percent:<10.2f}{'100.00':<12}")
    print("=================================================\n")

    # Market overview
    print("\n================ MARKET OVERVIEW =================")
    print(f"{'Company':<15}{'Ticker':<8}{'Price':<12}")
    print("-"*40)
    for name, ticker in company_tickers.items():
        price = fetch_price(ticker)
        if price is not None:
            print(f"{name:<15}{ticker:<8}{price:<12.2f}")
    print("=================================================\n")

# Remove stock from portfolio
def remove_stock():
    global portfolio
    if portfolio.empty:
        print("Portfolio is empty.")
        return
    ticker = input("Enter ticker to remove: ").strip().upper()
    if ticker in portfolio["Stock"].values:
        portfolio = portfolio[portfolio["Stock"] != ticker]
        portfolio.to_csv(PORTFOLIO_FILE, index=False)
        print(f"{ticker} removed from portfolio.")
    else:
        print(f"{ticker} not found in portfolio.")

# Main menu
def menu():
    while True:
        print("1. Add Stock\n2. View Portfolio & Market Overview\n3. Remove Stock\n4. Exit")
        choice = input("Enter choice: ").strip()
        if choice == "1":
            add_stock()
        elif choice == "2":
            view_portfolio()
        elif choice == "3":
            remove_stock()
        elif choice == "4":
            print("Exiting portfolio tracker.")
            break
        else:
            print("Invalid choice. Try again.")

# Run the program
if __name__ == "__main__":
    menu()