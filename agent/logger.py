import logging

class JaimeLogger:
    def __init__(self):
        logging.basicConfig(filename='jaime.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    def log(self, message):
        logging.info(message)