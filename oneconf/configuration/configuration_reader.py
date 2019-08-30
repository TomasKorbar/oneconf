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
        file_object = self._open_file(path)

        config_dict = self._file2dict(file_object, filetype)
        # we have to close file_object
        file_object.close()

        return config_dict

    def _file2dict(self, file_object, filetype=None):
        """Read contents of file_object and return them as dictionary

        If filetype is not specified then ConfigurationReader will try to
        determine it by attempts to parse file with all accessible parsers.

        Raises:
        DecodeError -- in case of bad syntax of configuration file or inability
                       to decode it
        ValueError -- in case of unknown filetype.

        Positional arguments:
        file_object -- file-like object of configuration file

        Keyword arguments:
        filetype -- type of configuration file
                    possible values: "json", "configobj"
        """
        # try to determine type of file if filetype has not been supplied
        if filetype is None:
            configuration = (self._json2dict(file_object, False)
                             or self._python_configobj2dict(file_object,
                                                            False)
                            )
            if configuration is None:
                msg = ("Oneconf was not able to decode %s"
                       % file_object.name)
                raise DecodeError(msg, file_object.name)
        elif filetype == "json":
            configuration = self._json2dict(file_object, True)
        elif filetype == "configobj":
            configuration = self._python_configobj2dict(file_object, True)
        else:
            # bad filetype argument has been supplied
            raise ValueError("Unknown filetype %s" % filetype)
        return configuration

    def _json2dict(self, file_object, raise_error=True):
        """Read contents of JSON file_object and return them as dictionary

        Raises:
        DecodeError -- in case of problems with decoding and if raise_error is
                       set to True

        Positional arguments:
        file_object --  file-like object of JSON configuration file

        Keyword arguments:
        raise_error -- indicates whether Error should be risen on problems with
                       decoding
        """
        configuration = None
        try:
            configuration = dict(json.load(file_object))
        except json.decoder.JSONDecodeError as err:
            if raise_error:
                # we have to mock JSONDecodeError's message format because
                # JSONDecodeError does not save it's message to public variable
                parser_msg = ("%s: line %d column %d (char %d)"
                            % (err.msg, err.lineno, err.colno, err.pos))
                file_object.close()
                raise DecodeError("Oneconf was not able to decode json file",
                                file_object.name,
                                parser_msg,
                                err.lineno,
                                ) from None
        finally:
            # return to the first line of file
            file_object.seek(0)
        return configuration

    def _python_configobj2dict(self, file_object, raise_error=True):
        """Read contents of configobj file_object and return them as dictionary

        Raises:
        DecodeError -- in case of problems with decoding and if raise_error is
                       set to True

        Positional arguments:
        file_object --  file-like object of configobj configuration file

        Keyword arguments:
        raise_error -- indicates whether Error should be risen on problems with
                       decoding
        """
        configuration = None
        try:
            conf = configparser.ConfigParser(dict_type=dict)
            conf.read_file(file_object)
            configuration = dict(conf._sections)
        except configparser.Error as err:
            if raise_error:
                msg = "Oneconf was not able to decode python config file"
                file_object.close()
                raise DecodeError(msg, file_object.name, err.message) from None
        finally:
            # return to the first line of file
            file_object.seek(0)
        return configuration

    def _open_file(self, path):
        """ Open a file on path and return it's file-like object

        Raises:
        FileError -- in case of inability to open file

        Positional arguments:
        path -- path on which is file located
        """
        try:
            file_object = open(path, "r")
        except IOError:
            raise FileError(path) from None
        return file_object
