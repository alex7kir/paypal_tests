from fw.helper_base import HelperBase
from nose.tools import assert_regexp_matches
import yaml
import string
import random

class CommonHelper(HelperBase):
    def __init__(self, manager):
        super(CommonHelper, self).__init__(manager)

    def assert_eq_dic_lst(self, lst1, lst2):		# Used in assert_eq_dic(dict1, dict2)
        for i in range(len(lst2)):
            if not isinstance(lst2[i], list):
                if isinstance(lst2[i], dict):
                    self.assert_eq_dic(lst1[i], lst2[i])
            else:
                self.assert_eq_dic_lst(lst1[i], lst2[i])

    def assert_eq_dic(self, dict1, dict2):		# Compare two dictionaries
        for x in dict2.keys():
            if not isinstance(dict2[x], dict):
                if isinstance(dict2[x], list):
                    self.assert_eq_dic_lst(dict1[x], dict2[x])
                else:
                    assert_regexp_matches(str(dict1[x]), str(dict2[x]), msg="Error in '{k}': '{v1}' not matched '{v2}'".format(k = x, v1 = str(dict1[x]), v2 = str(dict2[x])))
            else:
                self.assert_eq_dic(dict1[x], dict2[x])

    def read_yaml_file(self, filename):
        stream = file(filename, 'r')
        dict = yaml.load(stream)
        return dict
    
    def id_generator(self, size=10, chars=string.ascii_letters + string.digits):
        return ''.join(random.choice(chars) for x in range(size))
