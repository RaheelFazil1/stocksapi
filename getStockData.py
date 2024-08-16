import requests
import pandas as pd
import json

# url = "https://weatherbit-v1-mashape.p.rapidapi.com/forecast/3hourly"

url = "https://api.stockdio.com/data/financial/prices/v1/getlatestprices?app-key=089BDFE6C2C04DD3BDCB0CAE8329AE4E&stockExchange=USA&symbols=AAPL;MSFT;GOOG;META;ORCL"
# querystring = {"lat":"35.5","lon":"-78.5","units":"imperial","lang":"en"}

# headers = {
# 	"x-rapidapi-key": "d25323e04bmsh4b177d99ec540acp1dca45jsnf0eeca2ff834",
# 	"x-rapidapi-host": "weatherbit-v1-mashape.p.rapidapi.com"
# }

# response = requests.get(url, headers=headers, params=querystring)
response = requests.get(url)
json_data = response.json()

# print(json_data)
# print('-|-|-|-|-|-|-|-|-|-|-|-|')

columns = json_data['data']['prices']['columns']
values = json_data['data']['prices']['values']

new_df  = pd.DataFrame(values, columns=columns)
print(new_df )
print('-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|')

file_path = "stock_prices.csv"
try:
    old_df = pd.read_csv(file_path)
except FileNotFoundError:
    old_df = pd.DataFrame(columns=columns)

# Append new data to the old DataFrame
updated_df = pd.concat([old_df, new_df], ignore_index=True)

# Save the updated DataFrame back to the CSV file
updated_df.to_csv(file_path, index=False)

# Print the updated DataFrame
print(updated_df)






