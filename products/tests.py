from django.test import TestCase

# Create your tests here.

class FirstTestCase(TestCase):
    def setUp(self):
        pass

    def test_equal(self):
        self.assertEqual(1,1)

    def test_book_serailzer(self):
        pass