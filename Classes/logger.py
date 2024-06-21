import logging

def setup_logging(log_file, debug):
    logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')
    
    if isinstance(debug,str):
        debug = debug.lower() in ['true','1','yes']

    if debug:
        print('THIS WAS HIT')
        logging.getLogger().setLevel(logging.DEBUG)