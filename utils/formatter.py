# -*- coding: utf-8 -*-
__author__ = 'jjauhiainen'
from validator import ErrorMessages
def convert_to_integer(val):
    try:
        val = int(val)
        return val
    except ValueError:
        return ErrorMessages.NOT_NUMBER

def convert_to_float(val):
    try:
        val = float(val)
        return val
    except ValueError:
        return ErrorMessages.NOT_NUMBER