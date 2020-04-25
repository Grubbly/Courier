import logging
from datetime import datetime

class CourierLogger:
    def __init__(self, path=None):
        if path is None:
            self.path = datetime.now().strftime("%Y-%m-%d_%H:%M:%S_%p_courier.log")
        else:
            self.path = path
        logging.basicConfig(
            filename=self.path, 
            level=logging.DEBUG,
            format='%(asctime)s - %(name)s - %(levelname)-8s: %(message)s'
        )
        logging.info("Courier logging start.")
        
    def debug(self, msg):
        logging.debug(msg)
    def info(self, msg):
        logging.info(msg)
    def error(self, msg):
        logging.error(msg)
    def warning(self, msg):
        logging.warning(msg)
    

    