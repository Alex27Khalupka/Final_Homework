from all_functions import get_image
import unittest


class TestGetItemCheck(unittest.TestCase):

    def test_get_item_1(self):
        test_data = "<description>img src=`https://another-useless-link/-https://image`</description>"
        test_answer = "https://image"
        self.assertEqual(get_image(test_data), test_answer)

    def test_get_item_2(self):
        test_data = "<description>img src=`https://another-useless-link/-https://image2`</description>"
        test_answer = "https://image2"
        self.assertEqual(get_image(test_data), test_answer)

    def test_get_item_3(self):
        test_data = "<description>img src=`https://another-useless-link/-https://image3`</description>"
        test_answer = "https://image3"
        self.assertEqual(get_image(test_data), test_answer)


if __name__ == "__main__":
    unittest.main()
