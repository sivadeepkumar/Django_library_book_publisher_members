from django.test import TestCase
from .models import Borrowing
# Create your tests here.



class FirstTestCase(TestCase):

    def test_equal(self):
        self.assertEqual(1,1)

    def test_book_serailzer(self):
        objs = Borrowing.objects.all()
        for obj in objs:
            if obj.returned_date:
                cost = (obj.returned_date-obj.borrowed_date) * 3
                self.assertEqual(obj.overdue_charge,cost)

            # else:
            #     self.assertEqual(obj.overdue_charge,None)


