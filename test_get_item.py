from all_functions import get_item
import unittest


class TestGetItemCheck(unittest.TestCase):

    def test_get_item_title(self):
        test_item = "title"
        test_data = "<title>This is title</title>"
        test_answer = "This is title"
        self.assertEqual(get_item(test_item, test_data), test_answer)

    def test_get_item_date(self):
        test_item = "date"
        test_data = "<date>This is date</date>"
        test_answer = "This is date"
        self.assertEqual(get_item(test_item, test_data), test_answer)

    def test_get_item_link_check(self):
        test_item = "link"
        test_data = "<link>This is link</link>"
        test_answer = "This is link"
        self.assertEqual(get_item(test_item, test_data), test_answer)

    def test_get_item_description_check(self):
        test_item = "description"
        test_data = "<description><a></a>This is description<p></p></description>"
        test_answer = "This is description"
        self.assertEqual(get_item(test_item, test_data), test_answer)

    def test_get_item_image_check(self):
        test_item = "description"
        test_data = "<description><a></a>This is description<p></p></description>"
        test_answer = "This is description"
        self.assertEqual(get_item(test_item, test_data), test_answer)


if __name__ == "__main__":
    unittest.main()
