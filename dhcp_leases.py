#dhcp watch dog

import os
import sys
import re
import random

class DHCP_watchdog:

    """
    
    """

    def __init__(self, dhcp_sum, dhcp_occupied, dhcp_ip_start, dhcp_ip_end, dhcp_ip_map):
        
        self.dhcp_sum = 0
        self.dhcp_occupied = 0
        self.dhcp_ip_start = None
        self.dhcp_ip_end = None
        self.dhcp_ip_map = {}

    def set_dhcp_sum(self ,lease_num):
        
        self.dhcp_sum = lease_num

    def set_dhcp_occupied(self, lease_num):
        
        self.dhcp_occupied = lease_num

    def set_dhcp_ip_map(self ,ip_start, ip_end):
        
        rstart = re.compile(ip_start)
        rend = re.compile(ip_end)

        if ip_end > ip_start:
            return 2
        else:
            ip_range_num = (ip_end.split('.'))[3] - (ip_start.split('.'))[3] + 1
            ip = ip_start
            for i in range(ip_range):
                self.dhcp_ip_map[i].set_default(ip, 0)
                ips = ip.split('.')
                ip = ips[0] + '.' + ips[1] + '.' + ips[2] + '.' + str(int(ip.split('.'))[3] + 1)
    
    def set_dhcp_ip_start(self, ip_start):
        
        self.dhcp_ip_start = ip_start

    def set_dhcp_ip_end(self, ip_end):

        self.dhcp_ip_end = ip_end

    def get_dhcp_sum(self):
        
        lease_num = 0
        
        r_iprange = re.compile('\d+\.\d+\.\d+\.\d+')
        r_range = re.compile('range dynamic-bootp.*')
        
        sum_file_path = str('/etc/cobbler/dhcp.template')

        if os.path.exists(sum_file_path):
            f_cobblerd = file(sum_file_path)

            if f_cobblerd.tell() != 0:
                f_cobblerd.seek(0)

            range_list = r_range.findall(f_cobblerd.read() , 0)
            f_cobblerd.seek(0)

            ip_list = r_iprange.findall(range_list[0] , 0)
            f_cobblerd.seek(0)

            ip_range = ip_list[0].split(' ')
            
            a = ip_range[0].split('.')[3]
            b = r_iprange.findall(ip_range[1].split('.')[3])[0]
            c = abs(int(a) - int(b))

#            lease_num = abs(int((ip_range[0].split('.'))[3]) - int((iprange[1].split('.'))[3]))
            set_dhcp_sum(lease_num)

            set_dhcp_ip_map(self, ip_range[0] , ip_range[1])
            
            set_dhcp_ip_start(self, ip_range[0])
            set_dhcp_ip_end(self, ip_range[1])
            
    def get_dhcp_occupied(self):
        
        lease_num = 0
        rlease = re.compile('lease /d+/./d+/./d+/./d+')
        occupied_file_path = str('/var/lib/dhcpd/dhcpd.leases')
        
        if os.path.exists(occupied_file_path);
            f_occupied = file(occupied_file_path)

            if f_occupied.tell() != 0:
                f_occupied.seek(0)

            occupied_list =  rlease.findall(f_occupied.read() , 0)
            f_occupied.seek(0)
            
            i = 0
            for ip in self.dhcp_ip_map:

                if ip == occupied_list[0].split(' '):
                    
                    if self.dhcp_ip_map.get(ip) != 1:
                        self.dhcp_ip_map.set_default(ip, 1)
                else:
                    return 2

def run():
    
    watchdog = DHCP_watchdog(0 , 0 , None, None, None)
    watchdog.get_dhcp_sum()
    watchdog.get_dhcp_occupied()

    ip_start = watchdog.dhcp_ip_start
    ip_end = watchdog.dhcp_ip_end
    ip_sum = watchdog.dhcp_sum
    ip_map = watchdog.dhcp_ip_map
    ip_occupied = watchdog.dhcp_occupied

    if ip_sum < ip_occupied:
        return 2
    else:
        return 0
if __name__ == '__main__':
    run()
