import streamlit as st
import datetime
import yfinance as yf
import matplotlib.pyplot as plt

# Set up your web app
st.set_page_config(layout="wide", page_title="WebApp_Demo")

# Sidebar for ticker symbol input
st.sidebar.title("Input Ticker")
symbol = st.sidebar.text_input('Please enter the stock symbol: ', 'TSLA').upper()

# Sidebar for date selection
col1, col2 = st.sidebar.columns(2, gap="medium")
with col1:
    sdate = st.date_input('Start Date', value=datetime.date(2014, 1, 1))
with col2:
    edate = st.date_input('End Date', value=datetime.date.today())

st.title(f"{symbol}")

# Fetch stock data
stock = yf.Ticker(symbol)

# Display company information and financial ratios
try:
    st.write(f"# Sector: {stock.info['sector']}")
    st.write(f"# Company Beta: {stock.info['beta']}")
    st.sidebar.write(f"**P/E Ratio:** {stock.info['trailingPE']}")
    st.sidebar.write(f"**P/B Ratio:** {stock.info['priceToBook']}")
    st.sidebar.write(f"**Market Cap:** {stock.info['marketCap'] / 1e9:.2f} Billion USD")
except KeyError:
    st.error("Failed to fetch company information. Please check the ticker symbol.")

# Download historical data for the last 10 years
data = yf.download(symbol, start=sdate, end=edate)

# Plot closing prices
if not data.empty:
    st.line_chart(data['Close'], x_label="Date", y_label="Close, USD")
else:
    st.error("Failed to fetch historical data.")

# Fetch and display profits for the last 10 years
try:
    financials = stock.financials
    profits = financials.loc['Gross Profit']  # Fetch Gross Profit
    profits_years = profits.index.tolist()

    # Create a bar chart for profits
    plt.figure(figsize=(10, 5))
    plt.bar(profits_years, profits.values, color='royalblue')
    plt.title('Gross Profit Over the Years')
    plt.xlabel('Year')
    plt.ylabel('Gross Profit (USD)')
    plt.xticks(rotation=45)
    st.pyplot(plt)
except Exception as e:
    st.error(f"Failed to fetch financial data: {str(e)}")

# Display detailed financial information like Google Finance
st.header("Key Financials")

# Get balance sheet, income statement, and cash flow statement
try:
    balance_sheet = stock.balance_sheet
    income_statement = stock.financials
    cash_flow = stock.cashflow

    # Displaying Income Statement
    st.subheader("Income Statement")
    income_statement = income_statement.T  # Transpose for better readability
    st.dataframe(income_statement)

    # Displaying Balance Sheet
    st.subheader("Balance Sheet")
    balance_sheet = balance_sheet.T  # Transpose for better readability
    st.dataframe(balance_sheet)

    # Displaying Cash Flow Statement
    st.subheader("Cash Flow Statement")
    cash_flow = cash_flow.T  # Transpose for better readability
    st.dataframe(cash_flow)

except Exception as e:
    st.error(f"Failed to fetch financial statements: {str(e)}")
