import requests
from bs4 import BeautifulSoup
from datetime import datetime

# app = Flask(__name__)

def psx_data(symbol):
    print(symbol.upper())
    url = f'https://dps.psx.com.pk/company/{symbol.upper()}'
    response = requests.get(url)

    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract the required information
    price_data = {'Timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

    try:
        company_name = soup.find('div', class_='quote__name').text.strip().split("XD")[0].strip()
        sector = soup.find('div', class_='quote__sector').text.strip()
        price = soup.find('div', class_='quote__close').text.strip()
        change_value = soup.find('div', class_='change__value').text.strip()
        percent_change = soup.find('div', class_='change__percent').text.strip()

        price_data['Company Name'] = company_name
        price_data['Sector'] = sector
        price_data['Price'] = price
        price_data['Change'] = change_value
        price_data['Percent Change'] = percent_change

        stats_items = soup.find_all('div', class_='stats_item')
        data = {}

        for item in stats_items:
            label_div = item.find('div', class_='stats_label')
            value_div = item.find('div', class_='stats_value')

            if label_div and value_div:
                label = label_div.text.strip()
                value = value_div.text.strip()
                data[label] = value

        price_data['Open'] = data.get('Open', 'N/A')
        price_data['High'] = data.get('High', 'N/A')
        price_data['Low'] = data.get('Low', 'N/A')
        price_data['Volume'] = data.get('Volume', 'N/A')

    except Exception as e:
        print(f"An error occurred: {e}")
        return {'error': str(e)}

    print(price_data)

    return price_data

psx_data('mlcf')