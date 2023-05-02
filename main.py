from flask import Flask, jsonify, request, render_template
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)


@app.route('/get-rates', methods=['GET'])
def get_rates():
    # Get the currency conversion parameters from the query string
    from_currency = request.args.get('from_currency')
    to_currency = request.args.get('to_currency')
    amount = request.args.get('amount')

    # Customize the URL for the currency conversion
    url = f'https://www.calculator.net/currency-calculator.html?eamount={amount}&efrom={from_currency}&eto={to_currency}&ccmajorccsettingbox=1&type=1&x=Calculate'

    # Make a GET request to the URL and parse the HTML with Beautiful Soup
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract the conversion rate from the paragraph tag with id "verybigtext"
    rate = soup.find('p', {'class': 'verybigtext'}).text

    # Return the conversion rate as a JSON response
    return render_template("index.html", rates=rate)


if __name__ == '__main__':
    app.run()
