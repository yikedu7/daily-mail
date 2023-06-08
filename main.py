import requests
from bs4 import BeautifulSoup
import re


def get_highlight_info(link):
    # Send a GET request to the webpage
    response = requests.get(link)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract the title of the webpage
    title = soup.title.string

    # Extract the page URL
    page_url = response.url.split('#')[0]

    # Extract the highlight URL
    highlight_url = response.url

    # Extract the highlighted word
    highlight, context = None, None

    # Extract the context
    # Find the text surrounding the highlighted word
    page_text = soup.get_text()

    anchor = parse_anchor(highlight_url)
    if anchor['text']:
        highlight = anchor['text']
    elif anchor['begin'] and anchor['end']:
        begin, end = anchor['begin'], anchor['end']
        print(begin, end)
        begin_index = page_text.find(begin)
        end_index = page_text.find(end)
        highlight = page_text[begin_index:end_index]


    return title, page_url, highlight_url, highlight, context


def parse_anchor(link):
    begin, end, text = None, None, None
    # Case1: https://www.coindesk.com/business/2022/01/17/mechanism-capital-launches-100m-play-to-earn-gaming-fund/#:~:text=Originally%20founded%20with,press%20release%20Monday.
    # begin = "Originally founded with", end = "press release Monday."
    # Case2: https://www.coindesk.com/business/2022/01/17/mechanism-capital-launches-100m-play-to-earn-gaming-fund/#:~:text=on%20decentralized%20finance
    # text = "on decentralized finance"
    # Case3: https://www.coindesk.com/business/2022/01/17/mechanism-capital-launches-100m-play-to-earn-gaming-fund/#:~:text=a%20focus%20on-,decentralized,-finance%20(DeFi)%20in
    # text = "a focus on decentralized finance (DeFi) in"

    url_text = link.split('#:~:text=')[-1]
    sub_text_len = len(url_text.split(','))
    if sub_text_len == 1:
        text = url_text
    elif sub_text_len == 2:
        begin, end = url_text.split(',')
    elif sub_text_len == 3:
        begin, text, end = url_text.split(',')
    return {'begin': begin, 'text': text, 'end': end}


# Example usage
link = input("Enter the link to the highlight: ")
title, page_url, highlight_url, word, context = get_highlight_info(link)

print("Title:", title)
print("Page URL:", page_url)
print("Highlight URL:", highlight_url)
print("Word:", word)
print("Context:", context)
