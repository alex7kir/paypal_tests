from testconfig import config
from fw.application_manager import ApplicationManager

class BaseTest(object):
    _multiprocess_can_split_ = True
    
    @classmethod
    def setup_class(cls, props = config):
        BaseTest.app = ApplicationManager()
        BaseTest.app.set_properties(props)
#        BaseTest.ssh = BaseTest.app.get_ssh_helper().open_ssh_session(config['management_vm']['host'], config['management_vm']['username'], config['management_vm']['password'], config['management_vm']['port'])
#        BaseTest.app.set_property('ssh', BaseTest.ssh)
    
#    app = ApplicationManager() # Added for autocompletion support, please do not delete
    
    def verifyEquals(self, a, b, msg):
        try: assert a == b, msg
        except AssertionError, e: self.verificationErrors.append(str(e))
    '''
    @classmethod
    def teardown_class(cls):
        BaseTest.app.stop() 
    '''