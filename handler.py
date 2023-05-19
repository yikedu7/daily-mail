import os
import requests
import datetime
import asyncio
import telegram
from dotenv import load_dotenv


def arweave_data(path, date):
    base_url = 'https://api.viewblock.io/arweave/stats/advanced/charts'
    url = base_url + path
    headers = {
        'origin': 'https://viewblock.io',
    }
    rsp = requests.get(url, headers=headers)
    if rsp.status_code != 200:
        return 'NaN'
    rsp_data = rsp.json()
    stat_times = rsp_data['day']['data'][0]
    stat_datas = rsp_data['day']['data'][1]
    stat_index = len(stat_times) - 1
    for i in range(len(stat_times)).__reversed__():
        if datetime.datetime.fromtimestamp(stat_times[i] / 1000).date() == date.date():
            stat_index = i
            break
    return stat_datas[stat_index]


def cgc_data(coin, date, date_type):
    url_template = 'https://api.coingecko.com/api/v3/coins/{}/history?date={}&localization=false'
    url = url_template.format(coin, date.strftime('%d-%m-%Y'))
    headers = {
        'accept': 'application/json',
    }
    rsp = requests.get(url, headers=headers)
    if rsp.status_code != 200:
        return 'NaN'
    rsp_data = rsp.json()
    return rsp_data['market_data'][date_type]['usd']


def format_int_str(num):
    if num == 'NaN':
        return num
    return format(int(num), ',d')


def format_float_str(num):
    if num == 'NaN':
        return num
    return format(float(num), ',.3f')


def fetch_data():
    date = datetime.datetime.today() - datetime.timedelta(days=1)
    return {
        'date': date.strftime('%Y-%m-%d'),
        'ar_tx': format_int_str(arweave_data('/tx?network=mainnet', date)),
        'ar_tx_fee': format_float_str(arweave_data('/txFees?network=mainnet', date)) + ' AR',
        'ar_block_reward': format_float_str(arweave_data('/blockReward?network=mainnet', date)) + ' AR',
        'ar_endowment_growth': format_float_str(arweave_data('/endowmentGrowth?network=mainnet', date)) + ' AR',
        'pepe_volume': '$' + format_float_str(cgc_data('pepe', date, 'total_volume')),
    }


def send_tg_msg(tg_msg):
    bot_token = os.environ.get('TG_BOT_TOKEN')
    chat_id = os.environ.get('TG_CHAT_ID')
    asyncio.run(telegram.Bot(token=bot_token).send_message(chat_id=chat_id, text=tg_msg))


def run():
    load_dotenv()
    data = fetch_data()
    print('Fetched date: {}'.format(data))
    msg_template = 'Date: {}\nArweave transactions: {}\nArweave transaction fees: {}\nArweave block reward: {' \
                   '}\nArweave endowment growth: {}\nPepe volume: {}'
    msg = msg_template.format(data['date'], data['ar_tx'], data['ar_tx_fee'], data['ar_endowment_growth'],
                              data['ar_block_reward'], data['pepe_volume'])
    send_tg_msg(msg)


def handler(event, context):
    run()
