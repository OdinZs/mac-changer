#!/usr/bin/env python
import subprocess
import optparse
import re


def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface to chance its MAC address")
    parser.add_option("-m", "--mac", dest="new_mac", help="New MAC address")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("[-] Please specify an interface, use --help for more info")
    elif not options.new_mac:
        parser.error("[-] Please specify a new  MAC, use --help for more info")
    return options


def change_mac(interface, new_mac):
    print("[+] Changing MAC address for " + interface + " to " + new_mac)

    try:
        subprocess.check_output(['ifconfig', interface])
        subprocess.call(["ifconfig", interface, "down"])
        subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
        subprocess.call(["ifconfig", interface, "up"])
    except subprocess.CalledProcessError:
        print("[-] Não foi possível encontrar a interface " + interface)


def get_current_mac(interface):
    try:
        subprocess.check_output(['ifconfig', interface])
        ifconfig_result = subprocess.check_output(('ifconfig', interface)).decode('utf-8')
        mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)
        if mac_address_search_result:
            return mac_address_search_result.group(0)
        else:
            print("[-] Não foi possível mudar o MAC")
    except subprocess.CalledProcessError:
        print("[-] Não foi possível encontrar a interface " + interface)


options = get_arguments()

change_mac(options.interface, options.new_mac)
current_mac = get_current_mac(options.interface)
print("Current MAC = " + str(current_mac))
if current_mac == options.new_mac:
    print("[+} MAC address foi alterado com sucesso para " + current_mac)
else:
    print("[-] MAC address não foi alterado")

