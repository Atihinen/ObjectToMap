__author__ = 'jjauhiainen'

from enum import Enum

class ErrorMessages(Enum):
    OK = 0
    EMPTY_VAL = 1
    TOO_LONG = 2
    NOT_NUMBER = 3

def validate_empty(value):
    if not value:
        return ErrorMessages.EMPTY_VAL
    return ErrorMessages.OK

def validate_length(val, length):
    if len(val) > length:
        return ErrorMessages.TOO_LONG
    return ErrorMessages.OK