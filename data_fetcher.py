import requests
import pandas as pd

def fetch_option_chain():
    url = "https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    session = requests.Session()
    session.headers.update(headers)

    try:
        response = session.get(url, timeout=10)
        data = response.json()
        records = data['records']['data']
        expiry_dates = data['records']['expiryDates']
        spot_price = data['records']['underlyingValue']

        options = []

        for record in records:
            strike = record['strikePrice']
            expiry = record['expiryDate']

            ce = record.get('CE')
            pe = record.get('PE')

            if ce:
                options.append({
                    'type': 'CE',
                    'expiry': expiry,
                    'strike': strike,
                    'ltp': ce.get('lastPrice'),
                    'bid': ce.get('bidprice'),
                    'ask': ce.get('askPrice'),
                    'iv': ce.get('impliedVolatility'),
                    'oi': ce.get('openInterest'),
                    'change_oi': ce.get('changeinOpenInterest')
                })

            if pe:
                options.append({
                    'type': 'PE',
                    'expiry': expiry,
                    'strike': strike,
                    'ltp': pe.get('lastPrice'),
                    'bid': pe.get('bidprice'),
                    'ask': pe.get('askPrice'),
                    'iv': pe.get('impliedVolatility'),
                    'oi': pe.get('openInterest'),
                    'change_oi': pe.get('changeinOpenInterest')
                })

        df = pd.DataFrame(options)
        return df, spot_price, expiry_dates

    except Exception as e:
        print(f"Error fetching data: {e}")
        return pd.DataFrame(), 0, []