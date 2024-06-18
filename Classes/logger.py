import logging

def setup_logging(log_file, debug):
    logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')
    if debug:
        logging.getLogger().setLevel(logging.DEBUG)