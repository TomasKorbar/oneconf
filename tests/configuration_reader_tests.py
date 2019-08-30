import os
import unittest
import tempfile

from oneconf.configuration import ConfigurationReader
from oneconf.exceptions import DecodeError, FileError

class TestConfigurationReader(unittest.TestCase):

    def setUp(self):
        self.reader = ConfigurationReader()
        self.temp_file_fd, self.temp_file_path = tempfile.mkstemp()

    def test_read_normal_json(self):
        right_dict = {"var1":"value1","var2":"value2"}
        with open(self.temp_file_path, "w") as conf_file:
            conf_file.write('{"var1":"value1","var2":"value2"}')
        # test read with specified file type
        conf_dict = self.reader.read_file(self.temp_file_path, "json")
        self.assertEqual(right_dict, conf_dict)
        # test read without specified file type
        conf_dict = None
        conf_dict = self.reader.read_file(self.temp_file_path)
        self.assertEqual(right_dict, conf_dict)

    def test_read_broken_json(self):
        with open(self.temp_file_path, "w") as conf_file:
            conf_file.write('broken')
        with self.assertRaises(DecodeError):
            conf_dict = self.reader.read_file(self.temp_file_path, "json")

    def test_read_normal_configobj(self):
        right_dict = {"sec1":{"var1":"value1"},"sec2":{"var2":"value2"}}
        with open(self.temp_file_path, "w") as conf_file:
            conf_file.write("[sec1]\nvar1=value1\n[sec2]\nvar2=value2")
        # test read with specified file type
        conf_dict = self.reader.read_file(self.temp_file_path, "configobj")
        self.assertEqual(right_dict, conf_dict)
        # test read without specified file type
        conf_dict = None
        conf_dict = self.reader.read_file(self.temp_file_path)
        self.assertEqual(right_dict, conf_dict)

    def test_read_broken_configobj(self):
        with open(self.temp_file_path, "w") as conf_file:
            conf_file.write('broken')
        with self.assertRaises(DecodeError):
            conf_dict = self.reader.read_file(self.temp_file_path, "configobj")

    def test_read_broken_file(self):
        with open(self.temp_file_path, "w") as conf_file:
            conf_file.write('broken')
        with self.assertRaises(DecodeError):
            conf_dict = self.reader.read_file(self.temp_file_path)

    def test_read_bad_format(self):
        with open(self.temp_file_path, "w") as conf_file:
            conf_file.write('not important')
        with self.assertRaises(ValueError):
            conf_dict = self.reader.read_file(self.temp_file_path, "junk")

    def test_read_nexistent_file(self):
        with self.assertRaises(FileError):
            conf_dict = self.reader.read_file('/non-existent-file.conf')

    def tearDown(self):
        os.close(self.temp_file_fd)
        os.remove(self.temp_file_path)
