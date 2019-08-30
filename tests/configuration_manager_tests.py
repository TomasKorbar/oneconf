import unittest

from oneconf.configuration import ConfigurationManager
from oneconf.configuration import ConfigurationObject

class TestConfigurationManager(unittest.TestCase):

    def setUp(self):
        self.conf_manager = ConfigurationManager()

    def test_merge_normal(self):
        right_conf = {"var1":"val1", "var2":"val3", "var3":{"var4":"val5"}}

        o1 = ConfigurationObject(1, conf_dict={"var1":"val1", "var2":"val2"})
        o2 = ConfigurationObject(2, conf_dict={"var2":"val3",
                                               "var3":{"var4":"val4"}})
        o3 = ConfigurationObject(2, conf_dict={"var3":{"var4":"val5"}})

        o4 = self.conf_manager.merge_conf_objects([o1,o2,o3])
        self.assertEqual(right_conf, o4.configuration)
