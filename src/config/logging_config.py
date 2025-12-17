import logging

def configure_logging(level=logging.INFO):
    logging.basicConfig(level=level,
                        filename='config.log', filemode='a',
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')