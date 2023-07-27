import unittest
import data_collection as dc


class Test(unittest.TestCase):
    def test_existence(self):
        self.assertTrue(dc.get_installed_software() is not None)

    def test_non_empty(self):
        for _software in dc.get_installed_software().values():
            self.assertTrue(_software.values() != "")

    def test_output(self):
        print_installed_software()
        self.assertTrue(True)

    def test_get_router_ip(self):
        Your_IP = "192.168.31.236"  # Change it according to your IP.
        self.assertTrue(dc.get_router_ip() == Your_IP)

    def test_get_mac_addr(self):
        self.assertTrue(dc.get_mac_addr() is not None)


def print_installed_software():
    """
    Print all installed software names in the Windows Registry, including their
    versions and publishers.
    """
    _software_list = dc.get_installed_software()

    def format_name(name, cnt):
        return name[:cnt - 3] + '...' if len(name) > cnt else name

    print("{:<70} {:<20} {:<30}".format('SoftwareName', 'Version', 'Publisher'))
    print("{:<70} {:<20} {:<30}".format('------------', '-------', '---------'))

    for _software in _software_list.values():
        _name = format_name(_software['Name'], 70)
        _publisher = format_name(_software['Publisher'], 30)
        GBK_count = sum(1 for char in _software['Name'][:70]
                        if ord(char) >= 128 and ord(char) != 174)
        name_len = 70 - GBK_count
        print(f"{_name.ljust(name_len)[:name_len]} "
              f"{_software['Version']:<20} {_publisher}")

    print('-' * 120)
    print('Total number of installed applications: [%s]' % len(_software_list))


if __name__ == '__main__':
    unittest.main()
