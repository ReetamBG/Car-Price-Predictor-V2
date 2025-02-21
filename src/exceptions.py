import sys
from src.logger import logging

def get_error_details(error_message):
    _, _, exc_tb = sys.exc_info()                        # get the error traceback object
    file_name = exc_tb.tb_frame.f_code.co_filename       # get script in which error occurred
    line_number = exc_tb.tb_lineno                       # get line number of error

    error_details = f"""
    Error: {error_message}
    In File: {file_name}
    In Line Number: {line_number}
    """

    return error_details


class CustomException(Exception):

    def __init__(self, error_message):
        # super().__init__(error_message)       don't need it since we are using custom __str__()
        self.error_details = get_error_details(error_message)

    def __str__(self):
        return self.error_details


# Testing 
if __name__ == "__main__":
    try:
        1/0
    except:
        logging.info("Divide Weeee no Zero Zero")
        raise CustomException("Divide by Zero Exception")
