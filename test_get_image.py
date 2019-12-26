from all_functions import get_image
import unittest


class TestGetItemCheck(unittest.TestCase):

    def test_get_item_1(self):
        test_data = '<description>useless info <img src="image"></description>'
        test_answer = "image"
        self.assertEqual(get_image(test_data), test_answer)

    def test_get_item_2(self):
        test_data = '<description>useless info <img src="image1"></description>'
        test_answer = "image1"
        self.assertEqual(get_image(test_data), test_answer)

    def test_get_item_3(self):
        test_data = '<description>useless info <img src="image2"></description>'
        test_answer = "image3"
        self.assertEqual(get_image(test_data), test_answer)


if __name__ == "__main__":
    unittest.main()
