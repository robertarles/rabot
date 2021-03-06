import requests
import json
import os


class Comms():

    def __init__(self):
        self.config = None
        with open((os.path.expanduser('~') + '/.rabot/comms.conf'), 'r') as json_config:
            self.config = json.load(json_config)

    def direct_message(self, handle, message):
        payload = {
            "text": '{}, {}'.format(handle, message),
            "icon_emoji": ":ghost:",
            # "channel": "#channel-name",
            # "channel": "@username",
            "username": "rabot32"
        }
        response = requests.post(self.config["slack_url"],
                      data=json.dumps(payload))
        if response.status_code != 200:
            print("[ERROR] Comms.direct_message() got a non 'http 200' response from slack.")

    def telegraph_message(self, handle, message):
        pass

if __name__ == '__main__':
    comms = Comms()
    # comms.direct_message('metarobert', 'tacko eatin, hambre.')
    comms.telegraph_message('metarobert', 'hack the cyber, fat bed sitting cyber hacker')
