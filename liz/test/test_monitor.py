import unittest
import unittest.mock as mock
import collections

from liz import monitor

def dummy(*args, **kwargs):
    pass

def mock_psutil_virtual_memory_percent(num):
    keys = [
        'total',
        'available',
        'percent',
        'used',
        'free',
        'active',
        'inactive',
        'wired'
    ]
    v = collections.namedtuple('virtual_memory_result', keys)
    v.percent = num
    monitor.psutil.virtual_memory = mock.create_autospec(dummy, return_value=v)

class TestMonitoring(unittest.TestCase):
    def test_mem(self):
        mock_psutil_virtual_memory_percent(84.2)
        self.assertEqual(monitor.gather_mem(), 84.2)

    def test_cpu(self):
        monitor.psutil.cpu_percent = mock.create_autospec(dummy, return_value=34.3)
        self.assertEqual(monitor.gather_cpu(), 34.3)

    def test_stats(self):
        mock_psutil_virtual_memory_percent(35)
        monitor.psutil.cpu_percent = mock.create_autospec(dummy, return_value=85.4)
        expected = {
            "cpu": 85.4,
            "mem": 35,
        }
        self.assertEqual(monitor.gather_stats(), expected)

if __name__ == '__main__':
    unittest.main()
