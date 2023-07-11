import re
import uuid
import winreg
import socket


def get_installed_software():
    """
    Get a dict of all installed software programs in Windows (support win2000)
    :return: a dict of software names and other information
    """
    win64_software = get_installed_helper(winreg.KEY_WOW64_64KEY)
    win64_software.update(get_installed_helper(winreg.KEY_WOW64_32KEY))
    return win64_software


def get_installed_helper(access):
    """
    Helper function that extracts the software list in Windows Registry
    with given access rights
    :param access: access right to the Windows Registry
    :return: a dict of software information in the form of
            software_dict = {name1: info1, name2: info1, ...}
            info1 = {"Name": name1, "Version": version1, ...}
    """
    _software_dict = {}
    _subkey_str = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"

    _query_info = ['Version', 'Publisher', 'Install date',
                   'Install location', 'Uninstall string']
    _query_name = ['DisplayVersion', 'Publisher', 'InstallDate',
                   'InstallLocation', 'UninstallString']

    try:
        _reg = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
        _key = winreg.OpenKey(_reg, _subkey_str, 0, winreg.KEY_READ | access)

        count_subkey = winreg.QueryInfoKey(_key)[0]

        for i in range(count_subkey):
            _software = {}

            try:
                _subkey_name = winreg.EnumKey(_key, i)
                _subkey = winreg.OpenKey(_key, _subkey_name)
                _pattern = r'^[a-zA-Z0-9]+|^[\u4e00-\u9fff\uac00-\ud7af]+'
                _name = winreg.QueryValueEx(_subkey, "DisplayName")[0]
                if re.match(_pattern, _name):
                    _software['Name'] = _name
                else:
                    continue

                for _query, _value in zip(_query_info, _query_name):
                    try:
                        _software[_query] = winreg.QueryValueEx(_subkey, _value)[0]
                    except EnvironmentError:
                        _software[_query] = 'Undefined'
                    finally:
                        if len(_software[_query]) == 0:
                            _software[_query] = 'Undefined'

                _software_dict.update({_name: _software})

            except EnvironmentError:
                continue

    except FileNotFoundError:
        pass

    return _software_dict


def get_router_ip():
    """
    Get the temporary IPv4 address assigned by the NAT of router
    :return: current IP address of the device
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            # Connect to a random external server
            s.connect(('6.6.6.6', 80))
            ip_addr = s.getsockname()[0]
            return ip_addr

    except socket.error:
        return None


def get_mac_addr():
    """
    Get the globally unique MAC address of the device
    :return: MAC address of the device
    """
    try:
        mac_address = uuid.getnode()
        mac_address = ':'.join(('%012X' % mac_address)[i:i + 2] for i in range(0, 12, 2))
        return mac_address

    except Exception as e:
        print("ERROR occurred while trying to retrieve MAC address: ", str(e))
        return None
