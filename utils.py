import time
import socket
import netifaces


def get_router_ip():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            # Connect to a random external server
            s.connect(('6.6.6.6', 80))
            ip_addr = s.getsockname()[0]
            return ip_addr

    except socket.error:
        return None


def get_mac_addr():
    try:
        # Get all network interfaces
        interfaces = netifaces.interfaces()

        # Find the first non-virtual interface
        for interface in interfaces:
            if not interface.startswith("lo"):
                return netifaces.ifaddresses(interface)[netifaces.AF_LINK][0]['addr']

    except Exception as e:
        print("ERROR occurred while trying to retrieve MAC address: ", str(e))
        return None


def sleep_for_some_time(hours=72):
    print("The thread will sleep for " + str(hours) + " hours.")
    time.sleep(hours)
