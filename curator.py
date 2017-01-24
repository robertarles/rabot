from comms import Comms
from vault import Vault
import datetime


class Curator(object):

        def __init__(self):
            self.message_recipient = "metabot32"
            self.tag_types = {
                "message": "`message`",
                "messaged": "`messaged`",
                "store": "`store`",
            }

        def process(self, message, tags, author='rabot32'):
            if self.tag_types['message'] in tags:
                comms = Comms()
                if comms.direct_message(self.message_recipient, message) is True:
                    # If the message failed to send, then no 'messaged' tag will be added
                    tags.append(self.tag_types['messaged'])
            if self.tag_types['store'] in tags:
                vault = Vault()
                vault.store(message, tags=['store'], author=author)

        def process_trends(self, trends, tags, author='rabot32'):
            if self.tag_types['store'] in tags:
                vault = Vault()
                vault.store_trends(trends, ["`store`", "trends"], author=author)


        def get_recent_vault_activity(self, limit=10, author='rabot32', author_contains=None):
            vault = Vault()
            recent_vault_activity = vault.get_recent_activity(
                limit=limit, author=author, author_contains=author_contains
            )
            return recent_vault_activity


if __name__ == '__main__':
    curator = Curator()
    curator.process(
        "test message{}".format(datetime.datetime.utcnow()),
        ["`message`", "`store`", 'someInnocuousTag']
    )
