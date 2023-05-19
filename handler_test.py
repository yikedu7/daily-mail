import handler
import unittest
import datetime


class TestHandler(unittest.TestCase):
    def test_arweave_data(self):
        date = datetime.datetime.today() - datetime.timedelta(days=1)
        result = handler.arweave_data('/tx?network=mainnet', date)
        print(result)
        self.assertTrue(result.isdigit())
