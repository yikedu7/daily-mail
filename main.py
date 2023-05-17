import requests
import datetime


def fetch_data():
    data = {
        'date': (datetime.datetime.today() - datetime.timedelta(days=1)).strftime('%Y-%m-%d'),
        'arweave_tx': arweave_data('/tx?network=mainnet'),
    }
    return data


def arweave_data(path):
    base_url = 'https://api.viewblock.io/arweave/stats/advanced/charts'
    url = base_url + path
    headers = {
        'origin': 'https://viewblock.io',
    }
    tx_rsp = requests.get(url, headers=headers)
    if tx_rsp.status_code != 200:
        return 'NaN'
    tx_data = tx_rsp.json()
    # get yesterday's data
    tx = tx_data['day']['data'][1][-2]
    return format(int(tx), ',d')


if __name__ == '__main__':
    print(fetch_data())
