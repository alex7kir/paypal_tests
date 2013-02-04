from webdriver_helper import WebDriverHelper
from ssh_helper import SshHelper
from fw.common_helper import CommonHelper
from fw.webdriver_helper import WebDriverWrapper
from fw.rabbitmq_helper import RabbitmqHelper

class ApplicationManager(object):
    
        _instance = None
        def __new__(cls, *args, **kwargs):
            if not cls._instance:
                cls._instance = super(ApplicationManager, cls).__new__(
                                    cls, *args, **kwargs)
                cls._instance.webdriverHelper = None
                cls._instance.webDriverWrapper = None
                cls._instance.sshHelper = None
                cls._instance.commonHelper = None
                cls._instance.rabbitmqHelper = None
            return cls._instance
        
#        def __init__(self):
#            self.webdriverHelper = None
#            self.webDriverWrapper = None
#            self.sshHelper = None
#            self.commonHelper = None
#            self.rabbitmqHelper = None
            
        
        
        
        def stop(self):
            if self.webdriverHelper != None:
                self.webdriverHelper.stop()
                
        def set_properties(self, props):
            self.props = props
            
        def set_property(self, prop_name, prop_value):
            self.props[prop_name] = prop_value
            
        def get_property(self, key):
            return self.props[key]
                
        def get_webdriver_helper(self):
            if self.webdriverHelper == None:
                self.webdriverHelper = WebDriverHelper(self)
            return self.webdriverHelper
        
        def get_webdriver_wrapper(self):
            if self.webDriverWrapper == None:
                self.webDriverWrapper = WebDriverWrapper(self)
            return self.webDriverWrapper
        
        def get_ssh_helper(self):
            if self.sshHelper == None:
                self.sshHelper = SshHelper(self)
            return self.sshHelper
        
        def get_common_helper(self):
            if self.commonHelper == None:
                self.commonHelper = CommonHelper(self)
            return self.commonHelper
        
        def get_rabbitmq_helper(self):
            if self.rabbitmqHelper == None:
                self.rabbitmqHelper = RabbitmqHelper(self)
            return self.rabbitmqHelper
        