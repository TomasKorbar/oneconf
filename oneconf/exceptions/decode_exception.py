"""Module containing DecodeError class"""

from oneconf.exceptions.oneconf_exception import OneconfError

class DecodeError(OneconfError):
    """Error raised when configuration file can not be parsed"""
    def __init__(self,
                 message,
                 path,
                 parser_msg=None,
                 lineno=None,
                 ):
        """DecodeError's constructor

        Positional arguments:
        message -- message describing the cause of Error
        path -- path to file which caused this Error

        Keyword arguments:
        parser_msg -- message from parser which failed to parse targeted file
        lineno -- line on which the problem is located
        """
        self.path = path
        self.lineno = lineno
        if parser_msg is not None:
            parser_msg = "\n" + parser_msg
        super(DecodeError, self).__init__("%s%s" % (message, parser_msg))
