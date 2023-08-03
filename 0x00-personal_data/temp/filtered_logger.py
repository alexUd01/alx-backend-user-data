#!/usr/bin/env python3
""" A module that contains a function `filter_datum` that returns the
log message obfuscated

Arguments:
    - fields: a list of strings representing all fields to obfuscate.
    - redaction: a string representing by what the field will be obfuscated.
    - message: a string representing the log line.
    - separator: a string representing by which character is separating all
      fields in the log line (message)

    The function uses a regex to replace occurrences of certain field values.
    `filter_datum` should be less than 5 lines long and use `re.sub` to
    perform the substitution with a single regex.
"""
from typing import List, Union
import re
import logging

PII_FIELDS = ('email', 'phone', 'ssn', 'password', 'ip')


def v(key: str, message: str, separator: str) -> Union[str, None]:
    """ A helper function: returns the value for a `key=val` pair """
    lst = message.split(separator)
    for item in lst:
        if item.startswith(key + '='):
            return item.split('=')[1]
    return None


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """ The function """
    for item in fields:
        if get_val(item, message, separator):
            message = re.sub(v(item, message, separator), redaction, message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Filters values in incoming log records using `filter_datum` above
        """
        record.msg = filter_datum(self.fields, self.REDACTION, record.msg,
                                  self.SEPARATOR)
        return super().format(record)


def get_logger() -> logging.Logger:
    """ Doc here """
    logger = loging.Logger(name='user_data', level=logging.INFO)
    logger.propagate = False
    logger.addHandler(logging.StreamHandler())
    logger.setFormatter(RedactingFormatter(PII_FIELDS))
    return logger
# Continue from: Task 3
