from comms import Comms
from vault import Vault
import datetime


class Curator(object):

        def __init__(self):
            self.message_recipient = "metabot32"
            self.tag_types = {
                "message": "`message`",
                "store": "`store`",
            }

        def process(self, message, tags):
            if self.tag_types['message'] in tags:
                comms = Comms()
                comms.direct_message(self.message_recipient, message)
            if self.tag_types['store'] in tags:
                vault = Vault()
                vault.store(message, tags)


if __name__ == '__main__':
    curator = Curator()
    curator.process(
        "test message{}".format(datetime.datetime.utcnow()),
        ["`message`", "`store`", 'someInnocuousTag']
    )
