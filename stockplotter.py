import requests
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib

def plot_stock_data(symbol):
    matplotlib.use('WXAgg')
    # Define API parameters
    api_key = "CZY670E5HFXYKK3D" # Replace with your API key
    function = "TIME_SERIES_DAILY_ADJUSTED" # Time series function
    output_size = "compact" # Compact output size (last 100 data points)

    # Make API request
    url = f"https://www.alphavantage.co/query?function={function}&symbol={symbol}&outputsize={output_size}&apikey={api_key}"
    response = requests.get(url)

    # Parse API response
    data = response.json()["Time Series (Daily)"]
    data = pd.DataFrame.from_dict(data, orient="index")
    data.index = pd.to_datetime(data.index)
    data = data.sort_index()
    data["4. close"] = data["4. close"].apply(lambda x: round(float(x), 2))

    # Visualize data
    plt.figure(figsize=(12, 6)) # Set the figure size
    plt.plot(data["4. close"], color="blue") # Set the line color
    plt.xlabel("Date", fontsize=14) # Set the x-axis label and font size
    plt.ylabel("Closing Price", fontsize=14) # Set the y-axis label and font size
    plt.title(f"Stock Market Data for {symbol}", fontsize=18) # Set the title and font size
    plt.tick_params(axis="both", which="major", labelsize=12) # Set the tick label size
    plt.grid(alpha=0.3) # Add a grid with transparency of 0.3
    plt.show()

