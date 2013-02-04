from base_test import *
def teardown_package(package):
#    package.BaseTest.app.get_ssh_helper().close_ssh_session(BaseTest.ssh)
#    package.BaseTest.app.get_lui_login_helper().logout()
    package.BaseTest.app.stop()