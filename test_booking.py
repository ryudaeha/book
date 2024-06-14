import unittest
from datetime import datetime, timedelta

from booking_scheduler import BookingScheduler
from schedule import Customer
from schedule import Schedule

NOT_ON_HOUR = datetime.strptime('2021/03/26 09:05', "%Y/%m/%d %H:%M")
ON_HOUR = datetime.strptime('2021/03/26 09:00', "%Y/%m/%d %H:%M")
CUSTOMER = Customer("Fake name", "010-5444-4523")
UNDER_CAPACITY = 1
CAPACITY_PER_H = 3
class BookingSchedulerTest(unittest.TestCase):

    def setUp(self):
        super().setUp()
        self.booking_sch  = BookingScheduler(CAPACITY_PER_H)
    def test_예약은_정시에만_가능하다_정시가_아닌경우_예약불가(self):
        schedule = Schedule(NOT_ON_HOUR, UNDER_CAPACITY, CUSTOMER)
        with self.assertRaises(ValueError):
            self.booking_sch.add_schedule(schedule)
    def test_예약은_정시에만_가능하다_정시인_경우_예약가능(self):
        schedule = Schedule(ON_HOUR, UNDER_CAPACITY, CUSTOMER)
        self.booking_sch.add_schedule(schedule)
        self.assertTrue(self.booking_sch.has_schedule(schedule))
    def test_시간대별_인원제한이_있다_같은_시간대에_Capacity_초과할_경우_예외발생(self):
        schedule = Schedule(ON_HOUR, CAPACITY_PER_H, CUSTOMER)
        self.booking_sch.add_schedule(schedule)
        with self.assertRaises(ValueError) as context:
            new_sch = Schedule(ON_HOUR, UNDER_CAPACITY, CUSTOMER)
            self.booking_sch.add_schedule(new_sch)
        self.assertEqual("Number of people is over restaurant capacity per hour", str(context.exception))

    def test_시간대별_인원제한이_있다_같은_시간대가_다르면_Capacity_차있어도_스케쥴_추가_성공(self):
        schedule = Schedule(ON_HOUR, CAPACITY_PER_H, CUSTOMER)
        self.booking_sch.add_schedule(schedule)

        diff_time = ON_HOUR + timedelta(hours=1)
        new_sch = Schedule(diff_time, UNDER_CAPACITY, CUSTOMER)
        self.booking_sch.add_schedule(new_sch)

        self.assertTrue(self.booking_sch.has_schedule(schedule))



    def test_예약완료시_SMS는_무조건_발송(self):
        pass

    def test_이메일이_없는_경우에는_이메일_미발송(self):
        pass

    def test_이메일이_있는_경우에는_이메일_발송(self):
        pass

    def test_현재날짜가_일요일인_경우_예약불가_예외처리(self):
        pass

    def test_현재날짜가_일요일이_아닌경우_예약가능(self):
        pass


if __name__ == '__main__':
    unittest.main()