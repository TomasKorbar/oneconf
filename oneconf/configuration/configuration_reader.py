""" Module containing ConfigurationReader class
"""
import json
import configparser

from oneconf.exceptions import DecodeError, FileError

class ConfigurationReader:
    """ Class containing Oneconf's methods for parsing of configuration files"""
    def __init__(self):
        """ConfigurationReader's constructor"""

    def read_file(self, path, filetype=None):
        """Read configuration file and return it's dictionary representation

        If filetype is not specified then ConfigurationReader will try to
        determine it by attempts to parse file with all accessible parsers.

        Raises:
        DecodeError -- in case of bad syntax of configuration file or inability
                        to decode it
        FileError -- in case of inability to open the file
        ValueError -- in case of unknown filetype

        Positional arguments:
        path -- path to configuration file

        Keyword arguments:
        filetype -- type of configuration file
                    possible values: "json", "configobj"
        """
        # try to open file
        file_content = self._get_files_content(path)

        config_dict = self._string2dict(file_content, path, filetype)

        return config_dict

    def _string2dict(self, string, path, format=None):
        """Parse string in format and return it's dictionary representation

        If format is not specified then ConfigurationReader will try to
        determine it by attempting to parse string with all accessible parsers.

        Raises:
        DecodeError -- in case of bad syntax of string or inability
                       to decode it
        ValueError -- in case of unknown format.

        Positional arguments:
        string -- string to be parsed
        path -- path to file which contains string

        Keyword arguments:
        format -- format of string
                    possible values: "json", "configobj"
        """
        # try to determine type of file if filetype has not been supplied
        if format is None:
            configuration = (self._json2dict(string, path, False)
                             or self._python_configobj2dict(string, path, False)
                            )
            if configuration is None:
                msg = ("Oneconf was not able to decode %s", path)
                raise DecodeError(msg, path)
        elif format == "json":
            configuration = self._json2dict(string, path, True)
        elif format == "configobj":
            configuration = self._python_configobj2dict(string, path, True)
        else:
            # bad filetype argument has been supplied
            raise ValueError("Unknown filetype %s" % format)
        return configuration

    def _json2dict(self, string, path, raise_error=True):
        """Parse JSON string and return it's dictionary representation

        Raises:
        DecodeError -- in case of problems with decoding and if raise_error is
                       set to True

        Positional arguments:
        string --  JSON string to be parsed
        path -- path to file which contains string

        Keyword arguments:
        raise_error -- indicates whether Error should be risen on problems with
                       decoding
        """
        configuration = None
        try:
            configuration = dict(json.loads(string))
        except json.decoder.JSONDecodeError as err:
            if raise_error:
                # we have to mock JSONDecodeError's message format because
                # JSONDecodeError does not save it's message to public variable
                parser_msg = ("%s: line %d column %d (char %d)"
                            % (err.msg, err.lineno, err.colno, err.pos))
                raise DecodeError("Oneconf was not able to decode json file",
                                path,
                                parser_msg,
                                err.lineno,
                                ) from None
        return configuration

    def _python_configobj2dict(self, string, path, raise_error=True):
        """Parse configobj string and return it's dictionary representation

        Raises:
        DecodeError -- in case of problems with decoding and if raise_error is
                       set to True

        Positional arguments:
        string -- configobj string to be parsed
        path -- path to file which contains string

        Keyword arguments:
        raise_error -- indicates whether Error should be risen on problems with
                       decoding
        """
        configuration = None
        try:
            conf = configparser.ConfigParser(dict_type=dict)
            conf.read_string(string)
            configuration = dict(conf._sections)
        except configparser.Error as err:
            if raise_error:
                msg = "Oneconf was not able to decode python config file"
                raise DecodeError(msg, path, err.message) from None
        return configuration

    def _get_files_content(self, path):
        """ Open a file on path and return it's file-like object

        Raises:
        FileError -- in case of inability to open file

        Positional arguments:
        path -- path on which is file located
        """
        try:
            with open(path, "r") as file_object:
                return file_object.read()
        except IOError:
            raise FileError(path) from None
