from all_functions import date_convert
import unittest


class TestGetItemCheck(unittest.TestCase):

    def test_date_convert_1(self):
        test_date = "Mon, 23 Dec 2019 19:29:47 -0500"
        test_answer = "20191223"
        self.assertEqual(date_convert(test_date), test_answer)

    def test_date_convert_2(self):
        test_date = "Mon, 01 Jan 2019 19:29:47 -0500"
        test_answer = "20190101"
        self.assertEqual(date_convert(test_date), test_answer)

    def test_date_convert_3(self):
        test_date = "Wen, 30 Apr 2020 19:29:47 -0500"
        test_answer = "20200430"
        self.assertEqual(date_convert(test_date), test_answer)


if __name__ == "__main__":
    unittest.main()
