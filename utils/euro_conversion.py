import requests
import xmltodict

def convert_eur_to_czk(eur_price):
    # Fetch the latest EUR to CZK exchange rate from ČNB
    url = 'https://www.cnb.cz/en/financial_markets/foreign_exchange_market/exchange_rate_fixing/daily.xml'
    response = requests.get(url)
    
    # Parse the XML data to get the EUR to CZK exchange rate
    data = xmltodict.parse(response.text)
    
    # Extract the EUR to CZK rate
    eur_to_czk = [x['Cube']['@rate'] for x in data['Envelope']['Cube']['Cube'] if x['@currency'] == 'EUR'][0]
    
    # Convert the rate to float
    eur_to_czk = float(eur_to_czk)
    
    # Return the price in CZK
    return eur_price * eur_to_czk