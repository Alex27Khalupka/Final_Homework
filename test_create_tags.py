from all_functions import create_tags
import unittest


class TestCreateTagsCheck(unittest.TestCase):

    def test_create_tags_1(self):
        test_dict = {"title": "Title",
                     "description": "Description",
                     "date": "Date",
                     "link": "Link",
                     "image": "Image"}

        test_answer_data_in_tags = "<section>"
        test_answer_data_in_tags += '<title><p>Title</p></title>'
        test_answer_data_in_tags += '<p>Description</p>'
        test_answer_data_in_tags += '<p>Link: Link</p>'
        test_answer_data_in_tags += '<p>Date: Date</p>'
        test_answer_data_in_tags += '<image l:href="#pic1.jpg"/>'
        test_answer_data_in_tags += "</section>"
        self.assertEqual(create_tags(test_dict, 1), test_answer_data_in_tags)


if __name__ == "__main__":
    unittest.main()
