"""Module for notifying via TelegramBot about all process"""
import requests

import config


class Notifyer:
    """Class for notifying via TelegramBot"""
    def __init__(self, chat_id: int):
        self.token = config.tg_api_key
        self.chat_id = chat_id

    def send_message(self, message: str, silence: bool = False, markdown: bool = True) -> None:
        disable_notification = ""
        if silence:
            disable_notification = "&disable_notification=true"
        parse_mode = "parse_mode=markdown&"
        if not markdown:
            parse_mode = ""
        url = f'https://api.telegram.org/bot{self.token}/sendMessage?{parse_mode}chat_id={self.chat_id}{disable_notification}'
        requests.post(url, data={"text": message})  # this sends the message
