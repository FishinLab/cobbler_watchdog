#dhcpd
#tftpd
#xinetd
#apache-cobbler watch dogs

import os
import sys
import re
import commands

class dtxa_watchdog:

    is_dhcpd = False
    is_tftpd = False
    is_xinetd = False
    is_apache_cobbler = False

    def get_dhcpd_stat(self):
        return commands.getoutput('ps -ef | grep dhcpd')

    def get_tftpd_stat(self):
        return commands.getoutput('ps -ef | grep tftpd')

    def get_xinet_stat(self):
        return commands.getoutput('ps -ef | grep xinetd')

    def get_apacobb_stat(self):
        return commands.getoutput('ps -ef | grep apache-cobbler')


