import logging


class RaLogging():

    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def write(self, string):
        self.logger.info(string)

if __name__ == '__main__':
    ral = RaLogging()
    ral.write("test log output")
