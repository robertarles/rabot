import requests
import json
import os


class Comms():

    # configuration for sending as rabot32
    def __init__(self):
        self.config = None
        # read the twitter api secrets from ~/.twitter
        with open((os.path.expanduser('~') + '/.rabot/comms.conf'), 'r') as json_config:
            self.config = json.load(json_config)

    def direct_message(self, handle, message):
        payload={"text": message}
        response = requests.post(self.config["slack_url"],
                      data=json.dumps(payload))
        if response.status_code != 200:
            print("[ERROR] Comms.direct_message() got a non 'http 200' response from slack.")

if __name__ == '__main__':
    comms = Comms()
    comms.direct_message('metabot32', 'tacko eatin, hambre')
