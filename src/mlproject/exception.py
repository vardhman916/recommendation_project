import sys
from src.mlproject.logger import logging

#Here, sys is used to retrieve detailed error information, including the file name and line number where the error occurred.

class CustomException(Exception):
    def __init__(self,error_message,error_details:sys):
        super().__init__(str(error_message))
        self.error_message=error_message_detail(error_message,error_details)

    def __str__(self):
        return self.error_message
    
def error_message_detail(error,error_detail:sys):
    _,_,exc_tb = error_detail.exc_info()
    file_name = exc_tb.tb_frame.f_code.co_filename
    error_message = "Error occured in python script name [{0}] line number [{1}] error message [{2}]".format(
    file_name,exc_tb.tb_lineno,str(error))

    return error_message

#Error occurred in python script name [my_script.py] line number [4] error message: division by zero
