import os
import requests
import datetime
import asyncio
import telegram
from dotenv import load_dotenv
import pandas as pd


def arweave_data(path, date):
    base_url = 'https://api.viewblock.io/arweave/stats/advanced/charts'
    url = base_url + path
    headers = {
        'origin': 'https://viewblock.io',
    }
    try:
        rsp = requests.get(url, headers=headers)
        rsp.raise_for_status()
    except Exception as e:
        print(e)
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


def cgc_coin_data(coin, date, date_type):
    url_template = 'https://api.coingecko.com/api/v3/coins/{}/history?date={}&localization=false'
    url = url_template.format(coin, date.strftime('%d-%m-%Y'))
    headers = {
        'accept': 'application/json',
    }
    try:
        rsp = requests.get(url, headers=headers)
        rsp.raise_for_status()
    except Exception as e:
        print(e)
        return 'NaN'
    rsp_data = rsp.json()
    return rsp_data['market_data'][date_type]['usd']


def cgc_global_data(date_type):
    url = 'https://api.coingecko.com/api/v3/global'
    headers = {
        'accept': 'application/json',
    }
    try:
        rsp = requests.get(url, headers=headers)
        rsp.raise_for_status()
    except Exception as e:
        print(e)
        return 'NaN'
    rsp_data = rsp.json()
    return rsp_data['data'][date_type]['usd']


def pretty_num(num):
    if type(num) is int:
        return format(num, ',d')
    elif type(num) is float:
        return format(num, ',.3f')
    else:
        if num.isdigit():
            return format(int(num), ',d')
        elif num.replace('.', '', 1).isdigit():
            return format(float(num), ',.3f')
        else:
            return num


def get_yesterday():
    return datetime.datetime.today() - datetime.timedelta(days=1)


def fetch_data(date):
    total_volume = cgc_global_data('total_volume')
    pepe_volume = cgc_coin_data('pepe', date, 'total_volume')
    pepe_volume_percent = float(pepe_volume) / float(total_volume) * 100
    return pd.DataFrame(
        {
            date.strftime('%Y-%m-%d'): [
                pretty_num(arweave_data('/tx?network=mainnet', date)),
                pretty_num(arweave_data('/txFees?network=mainnet', date)) + ' AR',
                pretty_num(arweave_data('/blockReward?network=mainnet', date)) + ' AR',
                pretty_num(arweave_data('/endowmentGrowth?network=mainnet', date)) + ' AR',
                '$' + pretty_num(total_volume),
                '$' + pretty_num(pepe_volume),
                pretty_num(pepe_volume_percent) + '%'
            ]
        },
        index=[
            'Arweave Transactions',
            'Arweave Transaction Fees',
            'Arweave Block Reward',
            'Arweave Endowment Growth',
            'Total Volume',
            'Pepe Volume',
            'Pepe Volume / Total Volume'
        ]
    )


def send_tg_msg(data):
    bot_token = os.environ.get('TG_BOT_TOKEN')
    chat_id = os.environ.get('TG_CHAT_ID')
    bot = telegram.Bot(token=bot_token)
    asyncio.run(
        bot.send_message(
            chat_id=chat_id,
            text='```\n' + data.to_string() + '\n```',
            parse_mode=telegram.constants.ParseMode.MARKDOWN_V2
        )
    )


def run():
    load_dotenv()
    date = get_yesterday()
    data = fetch_data(date)
    print('Fetched data:\n' + data.to_string())
    send_tg_msg(data)


def handler(event, context):
    run()
