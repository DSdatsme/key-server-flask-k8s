import unittest
import pytest

from constants import *
from lib.key_utils import is_key_present, search_key_by_prefix, search_key_by_suffix


@pytest.mark.unittest
class EmptyKeysTests(unittest.TestCase):

    def setUp(self):
        pass


################# TESTS #################

    test_keys = {
        "abc1": "value1",
        "abc2": "test1",
        "abc3": "test2",
        "xyz1": "newvalue1",
        "xyz2": "value2"
    }

    def test_is_key_present_success(self):

        self.assertEqual(is_key_present(self.test_keys, "abc2"), "test1")
        self.assertEqual(is_key_present(self.test_keys, "xyz2"), "value2")

    def test_is_key_present_failure(self):

        with self.assertRaises(Exception) as custom_exception:
            is_key_present(self.test_keys, "abc")

        self.assertEqual(
            custom_exception.exception.args[0], KEY_NOT_FOUND_MESSAGE.format("abc"))
        self.assertEqual(
            custom_exception.exception.args[1], KEY_NOT_FOUND_STATUS_CODE)

    def test_search_key_by_prefix(self):
        self.assertEqual(search_key_by_prefix(
            self.test_keys, "xyz"), ["xyz1", "xyz2"])
        self.assertEqual(search_key_by_prefix(
            self.test_keys, "abc"), ["abc1", "abc2", "abc3"])

    def test_search_key_by_suffix(self):
        self.assertEqual(search_key_by_suffix(self.test_keys, "c1"), ["abc1"])
        self.assertEqual(search_key_by_suffix(
            self.test_keys, "1"), ["abc1", "xyz1"])
        self.assertEqual(search_key_by_suffix(
            self.test_keys, "2"), ["abc2", "xyz2"])
