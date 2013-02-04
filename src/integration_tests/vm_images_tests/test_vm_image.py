'''
Created on 16.05.2012

@author: akiryuhin
'''
from integration_tests.vm_images_tests.base_test import BaseTest
from nose.tools import eq_, ok_ #@UnresolvedImport
from testconfig import config
import subprocess


class TestVmImage(BaseTest):
    
    verificationErrors = []
    
    def test_generator(self):
        for vm in config['vm_list']:
            yield self.check_vm_image, vm
    
    def check_vm_image(self, vm):
        self.verificationErrors = []
        
        # Ping it
        print "\nStarting Ping..."
        self.ping(vm['host'])
        
        # Check SSH connection
        ssh = self.app.get_ssh_helper().open_ssh_session(vm['host'], vm['username'], vm['password'], vm['port'])
        assert not ssh is None, "SSH connection failed to host " + vm['host'] + ":" + str(vm['port']) + ". Skipping other tests for this host..."
        
        # Check packages
        package_list = self.get_packages_list(self.app.get_property('tests')[vm['type'] + '_components'])
        for package in package_list:
            self.check_if_package_is_present(ssh, package)

        # Check services
        service_list = self.get_services_list(self.app.get_property('tests')[vm['type'] + '_components'])
        for service in service_list:
            self.check_if_service_set_up(ssh, service)
            
        # Check eth0
        self.check_eth0(ssh)
        
        # Check ntp
        self.check_ntp(ssh)
            

        
        eq_([], self.verificationErrors, self.verificationErrors)

        

    def check_if_service_set_up(self, ssh, service_name):
        status = self.app.get_ssh_helper().send_ssh_command(ssh, "chkconfig | grep " + service_name)[1].read()
        service = status[:status.find('0')-1].strip()
        initlevel = status[status.find('3')+2:status.find('3')+4].strip()
        self.verifyEquals(service, service_name, "Service " + service_name + " not found")
        self.verifyEquals(initlevel, 'on', "Service " + service_name + " is off for initlevel 3")
        
    
    def check_if_package_is_present(self, ssh, package_name):
        status = self.app.get_ssh_helper().send_ssh_command(ssh, "yum list installed | grep " + package_name + " | grep -v ntp | awk '{print $1}'")[1].read()
        package = status[:status.find('.')]
        self.verifyEquals(package, package_name, "Package " + package_name + " not found")

        
    def get_packages_list(self, filename):
        list = self.get_list_of('package', filename)
        return list
    
    def get_services_list(self, filename):
        list = self.get_list_of('service', filename)
        return list
    
    def get_list_of(self, what, filename):
        f = open(filename, 'r')
        list = []
        for line in f:
            if not line.startswith('#'):
                if line.startswith(what + ':'):
                    list.append(line[line.find(':')+1:-1])
        f.close()
        return list
        
    def ping(self, ip):
        ping = subprocess.Popen(["ping", ip], shell=False) # for windows
#        ping = subprocess.Popen(["ping", "-c", "2", "-w", "1", ip], shell=False) for Linux
        ping.wait()
        eq_(ping.returncode, 0, "ERROR: failed to ping host. Please check.")
        print "Ping passed."

    
    def check_eth0(self, ssh):
        eth0_speed = self.app.get_ssh_helper().send_ssh_command(ssh, "ethtool eth0 | grep Speed | awk '{print $2}'")[1].read().strip()
        self.verifyEquals(eth0_speed, "1000Mb/s", "eth0 speed is not 1000Mb/s")
        
    def check_ntp(self, ssh):
        ntp = ""
        ntp_server_name = config['tests']['ntp_server_name']
        ntp = self.app.get_ssh_helper().send_ssh_command(ssh, "ntpq -pn | grep " + ntp_server_name)[1].read()
        self.verifyEquals(ntp, not "", "NTP server is not configured")




#__________________________________________________________________________________________

        
        
#    def setUp(self):
#        print "setUp Done"
#    
#    def test_simple1(self):
#        ssh = self.app.get_ssh_helper().open_ssh_session('172.18.196.62', 'root', '12345', '22')
#        self.check_if_package_is_present(ssh, 'dhcp-common')
#        
#    def test_simple2(self):
#        ssh = self.app.get_ssh_helper().open_ssh_session('172.18.22.153', 'root', '11111', '22')
#        self.check_if_package_is_present(ssh, 'wget')
#        eq_(0, 1)
#        
#    def test_simple3(self):
#        ssh = self.app.get_ssh_helper().open_ssh_session('172.18.196.62', 'root', '12345', '22')
#        self.check_if_package_is_present(ssh, 'dhcp-common')
#        
#    def test_simple4(self):
#        ssh = self.app.get_ssh_helper().open_ssh_session('172.18.22.153', 'root', '11111', '22')
#        self.check_if_package_is_present(ssh, 'wget')
#        eq_(0, 1)
#        
#    def test_simple5(self):
#        ssh = self.app.get_ssh_helper().open_ssh_session('172.18.196.62', 'root', '12345', '22')
#        self.check_if_package_is_present(ssh, 'dhcp-common')
#        
#    def test_simple6(self):
#        ssh = self.app.get_ssh_helper().open_ssh_session('172.18.22.153', 'root', '11111', '22')
#        self.check_if_package_is_present(ssh, 'wget')
#        eq_(0, 1)
#        
#    def test_simple7(self):
#        ssh = self.app.get_ssh_helper().open_ssh_session('172.18.196.62', 'root', '12345', '22')
#        self.check_if_package_is_present(ssh, 'dhcp-common')
#        
#    def test_simple8(self):
#        ssh = self.app.get_ssh_helper().open_ssh_session('172.18.22.153', 'root', '11111', '22')
#        self.check_if_package_is_present(ssh, 'wget')
#        eq_(0, 1)
#        
#    def test_simple9(self):
#        ssh = self.app.get_ssh_helper().open_ssh_session('172.18.196.62', 'root', '12345', '22')
#        self.check_if_package_is_present(ssh, 'dhcp-common')
#        
#    def test_simple10(self):
#        ssh = self.app.get_ssh_helper().open_ssh_session('172.18.22.153', 'root', '11111', '22')
#        self.check_if_package_is_present(ssh, 'wget')
#        eq_(0, 1)
        
#    @classmethod    
#    def teardown_class(cls):
#        eq_([], cls.verificationErrors, cls.verificationErrors)

#    def teardown(self):
#        eq_([], self.verificationErrors, self.verificationErrors)       
        