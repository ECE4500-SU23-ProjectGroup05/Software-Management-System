import re
import winreg


def get_installed_software():
    """
    Get a list of all installed software programs in Windows (support win2000)
    :return: a list of software names and other information
    """
    return get_installed_helper(winreg.KEY_WOW64_32KEY) + get_installed_helper(
        winreg.KEY_WOW64_64KEY)


def get_installed_helper(access):
    """
    Helper function that extracts the software list in Windows Registry
    with given access rights
    :param access: access right to the Windows Registry
    :return: a list of software names and other information
    """
    _software_list = []
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

                _software_list.append(_software)

            except EnvironmentError:
                continue

    except FileNotFoundError:
        pass

    return _software_list
