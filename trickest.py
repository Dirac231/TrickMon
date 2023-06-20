#!/usr/bin/python3
import requests
import time
from bs4 import BeautifulSoup
import hashlib

# Function to send a Telegram message using the Telegram API
def send_telegram_message(message):
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
    data = {'chat_id': CHAT_ID, 'text': message}
    response = requests.post(url, data=data)
    return response.json()


# Params
CHAT_ID = '[YOUR_CHAT_ID]'
BOT_TOKEN = '[YOUR_BOT_TOKEN]'

URL = 'https://github.com/trickest/inventory/commits/main'
URL_2 = 'https://github.com/trickest/cve/commits/main'

FILE_NAME = '/tmp/commits.txt'
FILE_CVES = '/tmp/cves.txt'

# Initial request to get the commit hrefs
response = requests.get(URL)
soup = BeautifulSoup(response.content, 'html.parser')
href_values = set([link.get('href') for link in soup.find_all('a', href=lambda href: href and '/commit/' in href)])

with open(FILE_NAME, 'w') as f:
    f.write('\n'.join(href_values))

response_2 = requests.get(URL_2)
soup = BeautifulSoup(response_2.content, 'html.parser')
href_values_2 = set([link.get('href') for link in soup.find_all('a', href=lambda href: href and '/commit/' in href)])

with open(FILE_CVES, 'w') as f:
    f.write('\n'.join(href_values_2))

# Loop to check the files for updates
while True:
    response = requests.get(URL)
    soup = BeautifulSoup(response.content, 'html.parser')
    current_href_values = set([link.get('href') for link in soup.find_all('a', href=lambda href: href and '/commit/' in href)])

    with open(FILE_NAME, 'r') as f:
        saved_href_values = set(f.read().splitlines())

    if current_href_values != saved_href_values:
        with open(FILE_NAME, 'w') as f:
            f.write('\n'.join(current_href_values))

        message = f'Changes detected in trickest inventory!'
        send_telegram_message(message)
        send_telegram_message(URL)

    response_cve = requests.get(URL_2)
    soup_2 = BeautifulSoup(response_cve.content, 'html.parser')
    current_href_values_2 = set([link.get('href') for link in soup_2.find_all('a', href=lambda href: href and '/commit/' in href)])

    with open(FILE_CVES, 'r') as f:
        saved_href_values_2 = set(f.read().splitlines())

    if current_href_values_2 != saved_href_values_2:
        with open(FILE_NAME, 'w') as f:
            f.write('\n'.join(current_href_values_2))

        message_2 = f'New CVE PoCs just dropped!'
        send_telegram_message(message_2)
        send_telegram_message(URL_2)

    time.sleep(120)
