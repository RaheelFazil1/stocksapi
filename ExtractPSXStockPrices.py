import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd


def psx_data(symbol):
    print(symbol.upper())
    # Fetch the web page
    # url = 'https://dps.psx.com.pk/company/EFERT'
    url = f'https://dps.psx.com.pk/company/{symbol.upper()}'
    response = requests.get(url)

    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract the required information
    price_data = {'Timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

    try:

        # Extract the company name
        company_name = soup.find('div', class_='quote__name').text.strip().split("XD")[0].strip()

        # Extract the sector
        sector = soup.find('div', class_='quote__sector').text.strip()

        # Extract the price
        price = soup.find('div', class_='quote__close').text.strip()

        # Extract the change value
        change_value = soup.find('div', class_='change__value').text.strip()

        # Extract the percent change
        percent_change = soup.find('div', class_='change__percent').text.strip()

        price_data['Company Name'] = company_name
        price_data['Sector'] = sector
        price_data['Price'] = price
        price_data['Change'] = change_value
        price_data['Percent Change'] = percent_change


        # Find all divs with the class 'stats_item'
        stats_items = soup.find_all('div', class_='stats_item')

        # Initialize a dictionary to store extracted values
        data = {}

        stats_section = soup.find('div', class_='stats stats--noborder')

        if stats_section:
            # Find all stats_item divs within this section
            stats_items = stats_section.find_all('div', class_='stats_item')
            # Iterate over the stats items
            for item in stats_items:
                # Find the label and value
                label_div = item.find('div', class_='stats_label')
                value_div = item.find('div', class_='stats_value')
                # Check if both label and value are found
                if label_div and value_div:
                    label = label_div.text.strip()
                    value = value_div.text.strip()
                    data[label] = value

        price_data['Open'] = data['Open']
        price_data['High'] = data['High']
        price_data['Low'] = data['Low']
        price_data['Volume'] = data['Volume']


    except Exception as e:
        print(f"An error occurred: {e}")
        return

    return price_data


out = psx_data('kosm')
print(out)

new_df = pd.DataFrame([out])
file_path = "PSX_stock_prices.csv"
try:
    old_df = pd.read_csv(file_path)
except FileNotFoundError:
    old_df = pd.DataFrame(columns=new_df.columns)
updated_df = pd.concat([old_df, new_df], ignore_index=True)
updated_df.to_csv(file_path, index=False)
print(updated_df)


