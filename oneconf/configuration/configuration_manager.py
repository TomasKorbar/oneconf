""" Module containing ConfigurationManager class
"""

from oneconf.configuration.configuration_object import ConfigurationObject

class ConfigurationManager:
    """Class containing methods for work with oneconf's configuration objects
    """
    def __init__(self):
        pass

    def merge_conf_objects(self, objects, priority=0):
        """Merge configuration objects and return the unified one

        Objects are merged with paying attention to priority so object with
        higher priority will override value of option defined in objects with
        lower priority

        Positional arguments:
        objects -- list of configuration objects to be merged

        Keyword arguments:
        priority -- priority for unified configuration
        """
        if len(objects) == 1:
            return objects[0]

        objects.sort(key=lambda obj: obj.priority)

        conf_dictionaries = [obj.configuration for obj in objects]
        final_dict = {}
        for conf_dict in conf_dictionaries:
            final_dict.update(conf_dict)

        return ConfigurationObject(priority, conf_dict=final_dict)
