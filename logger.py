# logger.py
import logging

logging.basicConfig(filename='my_app.log', level=logging.DEBUG)

def log_info(message):
    logging.info(message)

def log_error(message):
    logging.error(message)

def log_exception(e):
    logging.error(f"Det uppstod ett fel: {str(e)}", exc_info=True)
