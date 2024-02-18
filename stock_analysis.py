import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objs as go

# Function to fetch and process the stock data
def load_data(ticker):
    data = yf.download(ticker, period="max", interval="1d")
    data = data.dropna()
    # Calculating EMAs
    data['ShortEMA'] = data['Close'].ewm(span=12, adjust=False).mean()
    data['LongEMA'] = data['Close'].ewm(span=26, adjust=False).mean()
    data['LowerEMA'] = data['Close'].ewm(span=50, adjust=False).mean()
    data['ShortEMA_std'] = data['ShortEMA'].rolling(window=20).std()
    data['ShortEMA_LowerDeviation'] = data['ShortEMA'] - data['ShortEMA_std']
    return data

# Function to plot the data
def plot_data(data):
    fig = go.Figure()

    # Adding Close, LongEMA, and ShortEMA as solid lines
    fig.add_trace(go.Scatter(x=data.index, y=data['Close'], mode='lines', name='Close'))
    fig.add_trace(go.Scatter(x=data.index, y=data['LongEMA'], mode='lines', line_color='red', name='Long EMA'))
    fig.add_trace(go.Scatter(x=data.index, y=data['ShortEMA'], mode='lines',line_color='green', name='Short EMA'))

    # Adding LowerEMA as a dotted line
    fig.add_trace(go.Scatter(x=data.index, y=data['ShortEMA_LowerDeviation'], mode='lines', line_color='yellow', name='STDev', line=dict(dash='dot')))

    st.plotly_chart(fig)

# Main app function
def main():
    st.title('Stock Data Visualization')

    # User input for ticker symbol
    ticker = st.text_input('Enter ticker symbol:', 'RIVN')
    st.text('Look at the yellow line; if it starts to decrease after a golden cross, that is when to sell.')

    # Loading and plotting data
    data = load_data(ticker)
    plot_data(data)

if __name__ == "__main__":
    main()
