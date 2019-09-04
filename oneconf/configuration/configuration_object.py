""" Module containing ConfigurationObject class
"""
from oneconf.configuration import ConfigurationReader

class ConfigurationObject:
    """ Class for Oneconf's configuration object
    """
    def __init__(self, priority, path=None, conf_dict=None, data_format=None):
        if path is None and conf_dict is None:
            msg = "Either path or conf_dict must be specified"
            raise ValueError(msg)

        self.priority = priority
        useless = None
        if conf_dict is not None:
            self.configuration = conf_dict
        else:
            self.configuration = ConfigurationReader().read_file(path,
                                                                 data_format)
