"""Module containing OneconfError class"""

class OneconfError(Exception):
    """Oneconf's base error class"""
    def __init__(self, message):
        """OneconfError's constructor

        Positional arguments:
        message -- message describing the cause of Error
        """
        self.message = message
        super(OneconfError, self).__init__(message)
