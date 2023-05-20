import handler
import unittest
import datetime


class TestHandler(unittest.TestCase):
    def test_arweave_data(self):
        date = datetime.datetime.today() - datetime.timedelta(days=1)
        result = handler.arweave_data('/tx?network=mainnet', date)
        print(result)
        self.assertTrue(result.isdigit())

    def test_cgc_global_data(self):
        result = handler.cgc_global_data('total_volume')
        print(result)
        self.assertTrue(result.isdigit())

    def test_fetch_data(self):
        data = handler.fetch_data(handler.get_yesterday())
        print(data.to_markdown())
        self.assertIsNotNone(data)

    def test_run(self):
        handler.run()
        self.assertTrue(True)
