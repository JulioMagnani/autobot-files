import subprocess
import time
import re
import pyshark
import os


class NetworkOps:

    def connection_up(self, issd):
        """Function to connect to the WiFi AP, in case the issd and pswd
        was already set up the connection is stablished via network management
        by linux. The output is boolean, if it's True, means the connection was
        stablished"""

        self.wifi_connection_up = subprocess.Popen(['nmcli', 'con', 'up', '%s'
                                                   % issd],
                                                   stdout=subprocess.PIPE)
        self.wifi_connection_up.wait()

        self.terminal_output = self.wifi_connection_up.stdout.readlines()
        self.output_list = self.terminal_output_cleaning(self.terminal_output)

        self.con_success_flag = True

        if len(self.output_list) == 0:
            self.con_success_flag = False  # connection failed
            print("A new profile for DUT will be created")

        else:
            for self.element in self.output_list:
                if 'successfully' not in self.element:
                    # connection failed - a new profile will be created
                    self.con_success_flag = False

        return self.con_success_flag

    def wifi_connection(self, ssid=None, pswd=None, timeout='20'):
        """Connect to WiFi network via nmcli command

        Attributes:
        ssid -- name of the network
        pswd -- password
        timeout -- max time before connection fail
        """

        with subprocess.Popen(['nmcli', '--wait', '%s' % timeout, 'device',
                               'wifi', 'connect', '%s' % ssid, 'password',
                               '%s' % pswd],
                              stdin=subprocess.PIPE,
                              stderr=subprocess.PIPE,
                              stdout=subprocess.PIPE) as proc:
            shell_output = proc.stdout.readlines()
            output_list = self.terminal_output_cleaning(shell_output)

        if output_list:
            con_success_flag = True
        else:
            con_success_flag = False

        for element in output_list:
            if 'successfully' not in element:
                con_success_flag = False  # connection failed

        return con_success_flag

    def ping_attempt(self, wifi_iface, IP, count='5'):
        """Function to attempt to ping to the Host using the wifi interface,
        via ping function by linux. The output is boolean, and if its true,
        means the ping was successful"""
        with subprocess.Popen(['ping', '-c', '%s' % count, '-I',
                               '%s' % wifi_iface, '%s' % IP],
                              stdout=subprocess.PIPE) as ping_attempt:

            terminal_output = ping_attempt.stdout.readlines()
            output_list = self.terminal_output_cleaning(terminal_output)
            ping_success_flag = True

            if len(output_list) == 0:
                ping_success_flag = False  # connection failed
                print("Ping failed")

            for line in output_list:
                print(line)
                words = line.split(" ")
                for line in words:
                    message = line.lower()
                    if (message == 'unreachable'):
                        ping_success_flag = False  # ping failed
                        print("Ping failed")

        return ping_success_flag

    def wifi_iface_name(self):
        """Function to get the wifi network interface name """
        with subprocess.Popen(['nmcli', 'd'],
                              stdout=subprocess.PIPE) as check_wifi_iface:
            check_wifi_iface.wait()

            terminal_output = check_wifi_iface.stdout.readlines()
            output_list = self.terminal_output_cleaning(terminal_output)

            for element in output_list:
                if 'wifi' in element:
                    words = element

            words = words.split('wifi')
            wlan = words[0]
            wlan = wlan.replace(" ", "")

        return wlan

    def terminal_output_cleaning(self, terminal_readlines_output):
        """ Function to clean the output given by the terminal.
        The function output is a list with every line as element"""
        terminal_output = terminal_readlines_output
        terminal_output = map(lambda s: s.strip(), terminal_output)
        terminal_output = list(terminal_output)

        output_list = []

        for element in terminal_output:
            aux_var = element.decode('utf-8')
            if aux_var:
                output_list.append(aux_var)

        return output_list

    def wifi_connection_nosec(self, ssid=None, timeout='10'):
        """Connect to a wifi without security.
        Returns: True or false
        """

        # nmcli device wifi connect NET_2G215F64 password 58215F64
        with subprocess.Popen(
            ['nmcli', '--wait', '%s' % timeout, 'device', 'wifi', 'connect',
             '%s' % ssid], stdout=subprocess.PIPE) as proc:
            terminal_output = proc.stdout.readlines()
            output_list = self.terminal_output_cleaning(terminal_output)

        for line in output_list:
            if 'successfully' in line:
                return True
        return False

    def eth_iface_name(self):
        """Function to get the wifi network interface name """

        with subprocess.Popen(['nmcli', 'd'],
                              stdout=subprocess.PIPE) as check_eth_iface:

            check_eth_iface.wait()

            terminal_output = check_eth_iface.stdout.readlines()
            output_list = self.terminal_output_cleaning(terminal_output)

            for element in output_list:
                if 'ethernet' in element and 'connected' in element:
                    words = element

            words = words.split('ethernet')
            eth_name = words[0]
            eth_name = eth_name.replace(" ", "")

        return eth_name

    def disconnect_iface(self, iface):
        with subprocess.Popen(
            ['nmcli', 'd', 'disconnect', '%s' % iface],
                stdout=subprocess.PIPE) as disconnect:
                disconnect.wait()
                terminal_output = disconnect.stdout.readlines()
                output_list = self.terminal_output_cleaning(terminal_output)

        dis_success_flag = True
        for element in output_list:
            if 'successfully' not in element:
                dis_success_flag = False  # connection failed

        return dis_success_flag

    def connect_iface(self, iface):
        """ connect the network interface"""
        # ex: nmcli connection up ifname enp0s31f6
        with subprocess.Popen(
            ['nmcli', 'connection', 'up', 'ifname', '%s' % iface],
            stdout=subprocess.PIPE) as connect:
            connect.wait()

            terminal_output = connect.stdout.readlines()
            output_list = self.terminal_output_cleaning(terminal_output)

            con_success_flag = True

            for element in output_list:
                if 'successfully' not in element:
                    con_success_flag = False  # connection failed

        return con_success_flag

    def delete_wifi_profile(self, ssid=None):
        """Function to delete wifi profile by ssid."""

        # ex: nmcli connection delete ssid
        with subprocess.Popen(['nmcli', 'connection', 'delete', 'id',
                               '%s' % ssid], stdout=subprocess.PIPE) as proc:
                                shell_output = proc.stdout.readlines()
                                output_list = self.terminal_output_cleaning(
                                                                shell_output)

        for element in output_list:
            if 'successfully' in element:
                return True
        return False

    def reset_network_mngr(self):
        """reset network manager"""
        with subprocess.Popen(['nmcli', 'radio', 'wifi', 'off'],
                              stdout=subprocess.PIPE):
            time.sleep(5)
        with subprocess.Popen(['nmcli', 'radio', 'wifi', 'on'],
                              stdout=subprocess.PIPE):
            time.sleep(5)

    def ping6_attempt(self, net_iface, host=None):
        """Function to attempt to ping by ipv6 to the Host using the any interface,
        via ping6 function by linux. The output is boolean, and if it's true,
        means the ping was successful"""

        with subprocess.Popen(
                ['ping6', '-c', '5', '-I', '%s' % net_iface, '%s' % host],
                stdout=subprocess.PIPE) as ping6_attempt:

                ping6_attempt.wait()
                terminal_output = ping6_attempt.stdout.readlines()

                output_list = self.terminal_output_cleaning(terminal_output)
                print(output_list)
                ping6_success_flag = True

                print("interface: " + net_iface)
                print("host: " + host)

                if len(output_list) == 0:
                    ping6_success_flag = False  # connection failed
                    print("Ping6 failed")

                else:
                    for line in output_list:
                        words = line.split(" ")
                        print(words)
                        for line in words:
                            message = line.lower()
                            if (message == 'unreachable'):
                                ping6_success_flag = False  # ping failed
                                print("Ping6 failed")

        return ping6_success_flag

    def get_global_ipv6(self, iface, mac_dut):
        """This function get the global ipv6 of DUT.
        It uses tshark combined with ping6.
        First tshark starts to capture the packages,
        meanwhile, ping6 sends icmpv6 requests to arris website.

        The output is a string containing the ipv6 of DUT.
        """

        ws_filter = "ipv6.dst and eth.dst == " + mac_dut

        with subprocess.Popen(['tshark', '-i', '%s' % iface, '-Y', '%s' % ws_filter,
                                              '-T', 'fields', '-e', 'ipv6.src', '-a', 'duration:10'],
                                             stdout=subprocess.PIPE) as tshark_process:
            self.ping6_attempt(iface)
            tshark_process.wait()
            terminal_output = tshark_process.stdout.readlines()

            output_list = self.terminal_output_cleaning(terminal_output)

        try:
            ipv6_dut = output_list[0]
            if ',' in ipv6_dut:
                aux_var = ipv6_dut.split(',')
                ipv6_dut = aux_var[0]

            return ipv6_dut

        except:
            return None

    def ssid_check(self, ssid=None):
        """Check if an ssid shows up in a wifi scan.
        Returns: True or False
        """
        for line in self.scan_wifi():
            if ssid in line:
                return True

        return False

    def ssid_isconnected(self, ssid=None):
        """Check if client is connected to a ssid
        """
        with subprocess.Popen(['nmcli', 'connection', 'show', '--active'],
                              stdout=subprocess.PIPE) as proc:
            shell_output = proc.stdout.readlines()
            output_list = self.terminal_output_cleaning(shell_output)

        for line in output_list:
            if ssid in line:
                return True

        return False

    def scan_wifi(self):
        """Scan for wifi networks using nmcli.
        Returns: A string list with all available networks
        """
        with subprocess.Popen(['nmcli', 'device', 'wifi', 'list'],
                              stdout=subprocess.PIPE) as proc:
            shell_output = proc.stdout.readlines()
            output_list = self.terminal_output_cleaning(shell_output)

        return output_list

    def ping_attempt_100(self, wifi_iface, IP, count='5'):
        """Function to attempt to ping to the Host using the wifi interface,
        via ping function by linux.
        It verifies if the ping was 100% successful.
        The output is boolean, and if its true, means the ping was successful"""
        with subprocess.Popen(
                ['ping', '-c', '%s' % count, '-I', '%s' % wifi_iface,'%s' % IP],
                stdout=subprocess.PIPE) as ping_attempt:

            terminal_output = ping_attempt.stdout.readlines()
            output_list = self.terminal_output_cleaning(terminal_output)
            ping_success_flag = True

            if len(output_list) == 0:
                ping_success_flag = False  # connection failed
                print("Ping failed")

            for line in output_list:
                print(line)
                words = line.split(" ")
                for line in words:
                    message = line.lower()
                    if (message == 'unreachable'):
                        ping_success_flag = False  # ping failed
                        print("Ping failed")

            for line in output_list:
                words = line.split(",")
                for line in words:
                    message = line.lower()
                    if 'loss' in message:
                        print(message)
                        # extract the number
                        loss_pct = re.findall('\d+', message)
                        # convert from list to string
                        loss_pct = ''.join(loss_pct)
                        print("Loss packages: " + loss_pct + "percent")

                        if loss_pct != '0':
                            ping_success_flag = False

            return ping_success_flag

    def transfer_data(self, url):
        """This function download a file through URL.
        The output is the data size.
        After running, the function automatically delete the file."""
        with subprocess.Popen(
                ['wget', '-o', 'download.log', '-O', 'transferred_data', '%s' % url],
                stdout=subprocess.PIPE) as proc:
            proc.wait()

        file_found = False
        with open("download.log", "r") as f:
            read_data = f.read()
            if "100%" in read_data:
                file_found = True

        # delete log file and transferred data
        with subprocess.Popen(
                ['rm', 'download.log', 'transferred_data'],
                stdout=subprocess.PIPE) as proc:
            proc.wait()

        return file_found

    def find_ssid_bychannel(self, iface, channel=None, ssid=None, tout='20'):
        """
        Analyze broadcast beacon by channel filter.
        return True if ssid is in packet recovered
        """

        ws_filter = 'wlan_radio.channel== {0}'.format(str(channel))
        with subprocess.Popen(['tshark', '-i', '%s' % iface, '-Y',
                               '%s' % ws_filter, '-T', 'fields',
                               '-e', 'wlan.ssid', '-a',
                               'duration:%s' % tout],
                              stdout=subprocess.PIPE) as tshark_process:
            tshark_process.wait()
            terminal_output = tshark_process.stdout.readlines()

            output_list = self.terminal_output_cleaning(terminal_output)

        if ssid in output_list:
            return True

        return False

    def check_ht_tag(self, ssid='NET_5G215F64', iface='', pckt_count='1'):
        """
        Capture live packet and search for a given tag
        """

        filter = 'wlan.ssid==%s'.format(str(ssid))
        cap = pyshark.LiveCapture(interface=iface, display_filter=filter)

        for packet in cap.sniff_continuously(packet_count=pckt_count):
            pckt_headers = str(packet.layers[3]).split('\n').strip()
            for header in pckt_headers:
                if 'Tag: HT Capabilities' in header:
                    return header

    def activate_monitor_mode(self, interface=''):
        """Activate wireless monitor mode"""

        with subprocess.Popen(['sudo', 'service', 'network-manager', 'stop'],
                              stdout=subprocess.PIPE):
            time.sleep(5)
        with subprocess.Popen(['sudo', 'airmon-ng', 'start', '%s' % interface],
                              stdout=subprocess.PIPE):
            time.sleep(5)
        with subprocess.Popen(['sudo', 'service', 'network-manager', 'start'],
                              stdout=subprocess.PIPE):
            time.sleep(5)

    def get_monitor_mode(self):
        """Return wireless monitor mode interface"""
        with subprocess.Popen(['tshark', '-D'],
                              stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE) as terminal:
            raw_output = terminal.communicate()
            output = raw_output[0].decode("utf-8").split("\n")
            proc_list = [s.split(None, 1)[-1] for s in output if s]

        mon_iface = None

        for line in proc_list:
            if "mon" in line:
                mon_iface = line
                break

        return mon_iface

    def stop_monitor_mode(self, interface=''):
        """Stop wireless monitor mode"""

        with subprocess.Popen(['sudo', 'airmon-ng', 'stop', interface],
                              stderr=subprocess.STDOUT) as monitor_mode:
            if monitor_mode.stderr:
                print(monitor_mode.stderr)

        with subprocess.Popen(['sudo', 'service', 'network-manager', 'stop']):
            time.sleep(5)

        with subprocess.Popen(['sudo', 'service', 'network-manager', 'start']):
            time.sleep(10)

    def init_docker(self):
        """init docker compose"""

        file = 'docker-compose.yaml'
        if os.path.isfile(file):
            with subprocess.Popen(['docker-compose up'],
                                  stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE) as terminal:
                raw_output = terminal.communicate()
                final_output = [line.decode('utf-8').strip() for line in raw_output]

        return final_output

    def quit_docker(self):
        """init docker compose"""

        file = 'docker-compose.yaml'
        if os.path.isfile(file):
            with subprocess.Popen(['docker-compose up'],
                                  stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE) as terminal:
                raw_output = terminal.communicate()
                final_output = [line.decode('utf-8').strip() for line in raw_output]

        return final_output
