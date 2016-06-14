from ratwitter import RaTwitter
from rastoragemanager import RaStore
import datetime


class RaInfo(object):

        def __init__(self):
            self.message_recipient = "metabot32"
            self.tag_types = {
                "message": "`message`",
                "store": "`store`",
            }

        def process(self, message, tags):
            if self.tag_types['message'] in tags:
                rat = RaTwitter()
                rat.direct_message(self.message_recipient, message)
            if self.tag_types['store'] in tags:
                ras = RaStore()
                ras.save(message, tags)


if __name__ == '__main__':
    info = RaInfo()
    info.process(
        "test message{}".format(datetime.datetime.utcnow()),
        ["`message`", "`store`", 'someInnocuousTag']
    )
