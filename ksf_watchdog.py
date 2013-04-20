#ks file watch dog

import os
import sys
import re
from httplib import HTTPConnection as connection
from cobbler.api import BootAPI as boot

class ksf_watchdog:
    """
    """

    server_ip = str('')
    ks_name = str('')
    ks_file = None
    distro_name = None
    snippet_name_local = []
    snippet_name_remote = []
    ks_url_list = []
    ks_path_list = []
    
    def __init__(self, server_ip, distro_name):
        self.server_ip = server_ip
        self.distro_name = distro_name

    def gen_ks_url_path(self, distro_name):
        api = boot()
        profiles = api.find_profile(return_list = True , distro = distro_name)
        
        for profile in profiles:
            self.ks_url_list.append('http://' + self.server_ip + ':8801/cblr/svc/op/ks/profile/' + profile.name)
            self.ks_path_list.append('/var/lib/cobbler/kickstarts/rhel_5.4_ks/' + profile.name)

#    def check_ks_exist(self):
#        
#        for ks_path in self.ks_path_list:
#            if os.path.exists(ks_path) is True:
#                pass
#            else:
#                return 2

    def check_ks_file_stat(self):
        con = connection(self.server_ip, 8801)
        snippetr = re.compile('SNIPPET')

        for url in self.ks_url_list:
            con.request('get', url)
            pf = con.getresponse()

            if pf.status != 200:
                return 2
            
            snippets = snippetr.findall(pf.read())
            for snippet in snippets:
                
                self.snippet_name_remote.append(str.split(snippet)[1])

        for path in self.ks_path_list:
            fd = file(path)
            snippets = snippetr.findall(fd.read())
            
            if os.path.exists(path) is True:
                pass
            else: return 2

            for snippet in snippets:

                self.snippet_name_local.append(str.split(snippet)[1])
        return 0

    def cmp_files(self):

        flag = cmp(self.snippet_name_local , self.snippet_name_remote)
        if flag == 1:
            print 'error info'
            return 2
        elif flag == -1:
            print 'error info'
            return 2
        else:
            return 0

def run(server_ip, distro_name):

    watchdog = ksf_watchdog(server_ip , distro_name)
    watchdog.gen_ks_url_path()
    if watchdog.check_ks_file_stat() == 0:
        pass
    else: return 2

    if watchdog.cmp_files() == 0:
        pass
    else: return 2

