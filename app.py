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
        
        # Retrieve ROE if available
        roe = stock.info.get('returnOnEquity')
        if roe is not None:
            st.write(f"### Return on Equity (ROE): {roe}")
            # Plot ROE (for simplicity, using a static plot)
            fig, ax = plt.subplots()
            ax.bar(['ROE'], [roe], color='skyblue')
            ax.set_ylabel("Return on Equity")
            st.pyplot(fig)
        else:
            st.write("Return on Equity (ROE) data is not available.")
    except Exception as e:
        st.error("Error fetching company information.")
else:
    st.error("Failed to fetch company information.")

# Download historical data and plot
data = yf.download(symbol, start=sdate, end=edate)
if data is not None:
    st.line_chart(data['Close'], x_label="Date", y_label="Close, USD")
else:
    st.error("Failed to fetch historical data.")
