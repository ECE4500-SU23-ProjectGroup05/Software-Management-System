import unittest
import utils


class Test(unittest.TestCase):
    def test_get_router_ip(self):
        Your_IP = "192.168.31.236"  # Change it according to your IP.
        self.assertTrue(utils.get_router_ip() == Your_IP)

    def test_get_mac_addr(self):
        self.assertTrue(utils.get_mac_addr() is not None)


if __name__ == '__main__':
    unittest.main()
