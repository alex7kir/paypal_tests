from testconfig import config
from fw.application_manager import ApplicationManager
#from lomrest import lomrest

class BaseTest(object):

    #_multiprocess_can_split_ = True
    
    @classmethod
    def setup_class(cls, props = config):
        BaseTest.app = ApplicationManager()
        BaseTest.app.set_properties(props)
#        BaseTest.ssh = BaseTest.app.get_ssh_helper().open_ssh_session(BaseTest.app.get_property('mgmt_vm_host'), BaseTest.app.get_property('mgmt_vm_user'), BaseTest.app.get_property('mgmt_vm_password'), BaseTest.app.get_property('mgmt_vm_port'))
        BaseTest.ssh = BaseTest.app.get_ssh_helper().open_ssh_session(config['management_vm']['host'], config['management_vm']['username'], config['management_vm']['password'], config['management_vm']['port'])
        BaseTest.app.set_property('ssh', BaseTest.ssh)
        BaseTest.test_object = 'local_ui'
        BaseTest.app.set_property('test_object', BaseTest.test_object)
#        BaseTest.api = lomrest.RestApi(config['lom']['host'] + ':8000', 'root', 'swordfish')
#        BaseTest.app.set_property('api', BaseTest.api)
        BaseTest.ssh_lom = BaseTest.app.get_ssh_helper().open_ssh_session(config['lom']['host'], config['lom']['username'], config['lom']['password'], config['lom']['port'])
        BaseTest.app.set_property('ssh_lom', BaseTest.ssh_lom)
        
        
    app = ApplicationManager() # Added for autocompletion support, please do not delete
    config = config
    '''
    @classmethod
    def teardown_class(cls):
        BaseTest.app.stop() ['test_properties']
    '''