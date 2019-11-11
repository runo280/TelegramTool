import configparser
from Telegram import MyTelegram

account_config = "config.conf"

config = configparser.RawConfigParser(allow_no_value=False)
config.read(account_config)

target_account = config['current']['current']

phone_number = config[target_account]['phone']
password = config[target_account]['password']

client = config[target_account]['client']
name = config[client]['name']
api_id = config[client]['api_id']
api_hash = config[client]['api_hash']

telegram = MyTelegram(name, api_id, api_hash, phone_number, password)
telegram.get_channels_list()
