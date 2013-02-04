'''
Created on 12.05.2012

@author: akiryuhin
'''
import paramiko
import scpclient
import re
from fw.helper_base import HelperBase
from testconfig import config
from requests.exceptions import SSLError
import time
import socket
from nose.tools import ok_#@UnresolvedImport
from paramiko.ssh_exception import AuthenticationException
#import struct, fcntl  #FCNTL exists under Linux only

class SshHelper(HelperBase):

    def __init__(self, manager):
        super(SshHelper, self).__init__(manager)
        
    def open_ssh_session(self, host, user, password, port=22, timeout=30):
        self.ssh = paramiko.SSHClient()
        paramiko.util.logging.disable(self.ssh)
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.load_system_host_keys()
#        self.ssh.connect(hostname=host, port=int(port), username=user, password=password, timeout=timeout)
        for i in range(timeout):
            try:
                self.ssh.connect(hostname=host, port=int(port), username=user, password=password, timeout=timeout)
                break
            except socket.error as err: "SSLError caught..."
            except AuthenticationException: 
                print "Authentication failed to host " + host + ":" + str(port)
                self.ssh = None
                break
            time.sleep(1)
        else: raise Exception("Couldn't establish SSH connection during" + str(timeout) + "sec")
        return self.ssh
    
    def close_ssh_session(self, ssh):
        ssh.close()
        
    def send_ssh_command(self, ssh, command):
        output = ssh.exec_command(command)
        return output
    
    def put_file(self, ssh, local_file, remote_folder):
        scp = scpclient.Write(ssh.get_transport(), remote_folder)
        scp.send_file(local_file)
        
    def put_file_with_check(self, ssh, local_file, remote_folder):
        k = local_file.split('/')
        local_file_name = k[len(k)-1]
        file_ready = False
        i=0
        while i < 11:
            self.put_file(ssh, local_file, remote_folder)
#            scp = scpclient.Write(ssh.get_transport(), remote_folder)
#            scp.send_file(local_file)
            cred_file = self.send_ssh_command(self.ssh, 'cat ' + remote_folder + '/' + local_file_name)
            file_content = cred_file[1].read()
            error_mes = cred_file[2].read()
            if not file_content == '' and error_mes == '':
                file_ready = True
                return
            elif file_content == '' and not error_mes == '':
                print "File " + local_file_name + " cannot be read: " + error_mes
                print "\nTrying again..."
                time.sleep(5)
                i = i + 1
        if file_ready is False:
            ok_(False, 'Sending file ' + local_file_name + ' failed.')
            
    def check_file_accessibility(self, remote_folder, remote_file):
        file_ready = False
        cred_file = self.send_ssh_command(self.ssh, 'cat ' + remote_folder + '/' + remote_file)
        file_content = cred_file[1].read()
        error_mes = cred_file[2].read()
        if not file_content == '' and error_mes == '':
            file_ready = True
            return
        elif file_content == '' and not error_mes == '':
            print "File " + remote_file + " cannot be read: " + error_mes
            time.sleep(5)
        if file_ready is False:
            ok_(False, 'File ' + remote_file + ' reading failed. Substitution failed.')
        
    def put_dir(self, ssh, local_dir, remote_folder):
        scp = scpclient.WriteDir(ssh.get_transport(), remote_folder)
        scp.send_dir(local_dir)
        
    def substitute_file(self, ssh, local_folder, local_filename, destination_folder, remote_file, add = ''):
        self.send_ssh_command(ssh, 'mv '+ destination_folder + '/' + remote_file + ' ' + destination_folder + '/' + remote_file + '.bak' + add)
        self.put_file(ssh, local_folder + '/' + local_filename, destination_folder)
        self.send_ssh_command(ssh, 'mv '+ destination_folder + '/' + local_filename + ' '+ destination_folder + '/' + remote_file)
        
    def substitute_file_with_check(self, ssh, local_folder, local_filename, destination_folder, remote_file, add = ''):
        self.send_ssh_command(ssh, 'mv '+ destination_folder + '/' + remote_file + ' ' + destination_folder + '/' + remote_file + '.bak' + add)
        self.put_file_with_check(ssh, local_folder + '/' + local_filename, destination_folder)
        self.send_ssh_command(ssh, 'mv '+ destination_folder + '/' + local_filename + ' '+ destination_folder + '/' + remote_file)
        self.check_file_accessibility(destination_folder, remote_file)
        
    def restore_substituted_file(self, ssh, destination_folder, remote_file):
        self.send_ssh_command(ssh, 'rm -f '+ destination_folder + '/' + remote_file)
        self.send_ssh_command(ssh, 'mv '+ destination_folder  + '/' + remote_file + '.bak ' + destination_folder + '/' + remote_file)
        
    def get_file(self, ssh, remote_file, local_folder):
        #my_host = self.get_local_ip_linux()
        #print "\ncurrent IP: ", my_host
        #if my_host is None:
            #return False
        #command = "scp -v -P 10010 root@192.168.17.141:/opt/mescalero/reactor/log.txt /home/miroslav/log"
        sftp = ssh.open_sftp()
        sftp.get(remote_file, local_folder)
        sftp.close()
        #scp = scpclient.Read(ssh.get_transport(), remote_file)
        #scp.receive_file(local_folder, False, None, '/var/tmp_debug.log', None)
        return True
    
    def check_tunnel_to_appliance_with_ping(self, ssh, iface, remote_ip):
        _command = "ping -c 4 -I {0} {1} | gawk '{{for(i=1;i<NF;i++) {{if($i ~/%/) {{print $i}} }} }}'".format(iface, remote_ip)
        _response = self.send_ssh_command(ssh, _command)[1].read()
        _response = _response.replace("\n","")
        _response = _response.replace("%","")
        _response = int(_response)
        if str(_response) == "0":
            return True
        else:
            return False 
        
    def get_packet_route_with_ping(self, ssh, iface, remote_ip):
        '''
        Returns list of IP addresses and sites on the packet way to destination site
        '''
        _command = "ping -c 4 -R -I {0} {1} | gawk -v i=0 '{{if ($0 ~/RR/ || i==1) {{if ($0 ~/RR/){{i++}}; if (NF==0) exit 0; else print; next}} }}'".format(iface, remote_ip)
        _response = self.send_ssh_command(ssh, _command)[1].read()
        _response = _response.replace("RR:","")
        _response = _response.rstrip("\n")
        _response = _response.replace("\n",",")
        return _response
    
    def send_rest_request_via_ssh(self, ssh, rest_url=None, request_data=None, request_type=None, user=None, password=None):
        import json
        import types
        
        if request_type is None:
            request_type = "GET"
        if user is None:
            user = self.manager.get_property("lom_user")
        if password is None:
            password = self.manager.get_property("lom_password")
        if rest_url is None:
            rest_url = "http://{0}/rest/sys/appliances/list".format(self.manager.get_property("lom_host"))
        if request_data is not None:
            if isinstance(request_data, types.DictionaryType):
                request_data = json.dumps(request_data)
        
        if request_type == "GET":
            #           curl -k -s -i -u root:swordfish -H "Accept: application/json" -X GET http://192.168.17.141:8000/rest/sys/appliances/list
            _command = "curl -k -s -i -u {0}:{1} -H 'Accept: application/json' -X {2} {3}".format(user, password, request_type, rest_url)
        else:
            #           curl -k -s -i -u root:swordfish -H "Accept: application/json" -XPOST http://192.168.17.141:8000/rest/auth/service/verify -d '{"password":"ee9casllp3cf8czh"}'
            _command = "curl -k -s -i -u {0}:{1} -H 'Accept: application/json' -X{2} {3} -d '{4}'".format(user, password, request_type, rest_url, request_data)
            
        _response = self.send_ssh_command(ssh, _command)[1].read()
        return _response
    
    #Method below gets current local IP for given interface. Works under Linux only
    # def get_local_ip_linux(self,iface = 'eth0'):
        # sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # sockfd = sock.fileno()
        # SIOCGIFADDR = 0x8915
        # ifreq = struct.pack('16sH14s', iface, socket.AF_INET, '\x00'*14)
        # try:
            # res = fcntl.ioctl(sockfd, SIOCGIFADDR, ifreq)
        # except:
            # return None
        # ip = struct.unpack('16sH2x4s8x', res)[2]
        # return socket.inet_ntoa(ip)
    
