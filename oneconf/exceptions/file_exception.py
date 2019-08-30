"""Module containing FileError class"""
from oneconf.exceptions import OneconfError

class FileError(OneconfError):
    """Error raised when file is unacessible"""
    def __init__(self, path):
        """FileError's constructor

        Positional arguments:
        path -- path to file that could not be opened
        """
        msg = "file %s cannot be opened" % path
        super(FileError, self).__init__(msg)
