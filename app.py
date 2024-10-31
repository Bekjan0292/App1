import streamlit as st
import datetime
import plotly.graph_objs as go
import yfinance as yf

# Set the page configuration for the web app.
st.set_page_config(layout="wide", page_title="WebApp_Demo", page_icon="📈")

# Sidebar for input
st.sidebar.title("Input Ticker")
symbol = st.sidebar.text_input('Please enter the stock symbol:', 'NVDA').upper()
col1, col2 = st.sidebar.columns(2, gap="medium")
with col1:
    sdate = st.date_input('Start Date', value=datetime.date(2024, 1, 1))
with col2:
    edate = st.date_input('End Date', value=datetime.date.today())

# Display title
st.title(f"{symbol}")

# Fetch stock data and display additional financial information
stock = yf.Ticker(symbol)
if stock is not None:
    try:
        # Display company's basic information
        st.write(f"### Sector: {stock.info.get('sector', 'N/A')}")
        st.write(f"### Company Beta: {stock.info.get('beta', 'N/A')}")
        
        # Additional financial metrics
        st.write(f"### P/E Ratio: {stock.info.get('forwardPE', 'N/A')}")
        st.write(f"### P/B Ratio: {stock.info.get('priceToBook', 'N/A')}")
        st.write(f"### Market Cap: {stock.info.get('marketCap', 'N/A')}")
        st.write(f"### Profitability: {stock.info.get('profitMargins', 'N/A')}")

        # Attempt to retrieve annual financials and balance sheet data for more consistent data
        financials = stock.financials.transpose() if 'Net Income' in stock.financials else None
        balance_sheet = stock.balance_sheet.transpose() if 'Total Stockholder Equity' in stock.balance_sheet else None

        # Display the raw data to see what is available
        st.write("### Available Financial Data")
        st.write(financials if financials is not None else "Financial data not available.")
        st.write("### Available Balance Sheet Data")
        st.write(balance_sheet if balance_sheet is not None else "Balance sheet data not available.")

        if financials is not None and balance_sheet is not None:
            # Extract net income and total equity for the last 5 years (annual data preferred)
            net_income = financials["Net Income"].tail(5)
            total_equity = balance_sheet["Total Stockholder Equity"].tail(5)
            
            # Check if both series are non-empty and align
            if not net_income.empty and not total_equity.empty and len(net_income) == len(total_equity):
                # Calculate ROE (Net Income / Total Equity)
                roe = net_income / total_equity

                # Plot ROE and Profitability over the past 5 years
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=net_income.index, y=roe, mode='lines+markers', name="ROE"))
                fig.add_trace(go.Scatter(x=net_income.index, y=net_income, mode='lines+markers', name="Net Income (Profitability)"))
                
                fig.update_layout(
                    title=f"{symbol} - ROE and Profitability (Last 5 Years)",
                    xaxis_title="Year",
                    yaxis_title="Net Income (USD)",
                    yaxis2=dict(title="ROE", overlaying='y', side='right'),
                    legend=dict(x=0, y=1, bgcolor='rgba(0,0,0,0)')
                )
                st.plotly_chart(fig)
            else:
                st.warning("Insufficient data to calculate ROE or profitability over the last 5 years.")
        else:
            st.warning("Net Income or Total Stockholder Equity data is not available for the past 5 years.")
    
    except Exception as e:
        st.error(f"Error fetching company information or calculating ROE and profitability: {e}")
else:
    st.error("Failed to fetch company information.")

# Download historical data and plot
data = yf.download(symbol, start=sdate, end=edate)
if data is not None:
    st.line_chart(data['Close'], x_label="Date", y_label="Close, USD")
else:
    st.error("Failed to fetch historical data.")
