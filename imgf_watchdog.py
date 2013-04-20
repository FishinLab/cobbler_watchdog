#image file watch dog

import os
import sys
import re
from cobbler.api import BootAPI as boot
from httplib import HTTPConnection as connect

class imgf_watchdog(boot):
    """
    
    """

    def __init__(self, server_ip, distros = None, profiles = None, install_tree_url = None):
        self.server_ip = 'localhost'
        self.distros = []
        self.profiles = []
        self.install_tree_url = []
        boot.__init__(self)
    
    def set_distros(self, distro):
        self.distros.append(distro)

    def set_profiles(self, profile):
        self.profiles.append(profile)

    def set_intall_tree_url(self, url):
        self.install_tree_url.append(url)
# ===========================================================================

    def gen_sys_distros(self):
        #get distros from system without parameters
        tmp_list = self.find_distro(return_list = True)

    
        for tmp in tmp_list:
            self.set_distros(tmp)
        
        return 0

    def gen_sys_profiles(self):
        if self.distros is not None:
            
            for distro in self.distros:
                tmp_list = (self.find_profile(return_list = True, distro = distro))
                
                for tmp in tmp_list:
                    self.set_profiles(tmp)

            return 0
        else:
            print 'error:can not get the config of distros, try cobbler list to find the distro'
            return 2

    def gen_sys_install_tree_url(self):
        
        if self.profiles is not None:
            for profile in self.profiles:

                url = 'http://' + self.server_ip + '' + profile.name + ''
                self.set_intall_tree_url(str(url))
            return 0

        else:
            print 'error:can not find install tree'
            return 2
# ====================================================================

    def check_install_tree(self):
        if self.install_tree_url is not None:
            for url in self.install_tree_url:
                con = connect(self.server_ip)
                con.request('get', url)

                if con.getresponse().status != 200:
                    print 'error:install tree has been relapse'
                    return 2
                else:
                    pass
            return 0

         else:
             print 'error:can not find the install_tree_urls'
             return 2
# ====================================================================

def run(self):
    watchdog = imgf_watchdog('localhost')

    if watchdog.gen_sys_distros() == 0:
        if watchdog.gen_sys_profiles() == 0:
            if watchdog.gen_sys_install_tree_url() == 0:
                return watchdog.check_install_tree()
            else:
                return 2
        else:
            return 2
    else:
        return 2
  
if __name__ == '__main__':
    run()
