import calendar

from django.utils import timezone


class Day:
    def __init__(self, number, past, month, year):
        self.number = number
        self.past = past
        self.month = month
        self.year = year

    def __str__(self):
        return str(self.number)


class Calendar(calendar.Calendar):
    def __init__(self, year, month):

        super().__init__(firstweekday=6)

        self.year = year
        self.month = month
        self.day_names = ("Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat")
        self.months = (
            "January",
            "February",
            "March",
            "April",
            "May",
            "June",
            "July",
            "August",
            "September",
            "October",
            "November",
            "December",
        )

    def get_days(self):
        weeks = self.monthdays2calendar(self.year, self.month)
        now = timezone.now()
        today = now.day

        days = []
        for week in weeks:
            # for day, _ in week: 라고 표현할 수도 있다.
            # _ 는 week_day 값이 무엇이든 사용하지 않을 것이다라는 의미. null 처럼 사용
            for day, week_day in week:
                new_day = Day(
                    number=day,
                    past=bool(day <= today),
                    month=self.month,
                    year=self.year,
                )
                days.append(new_day)
        return days

    def get_month(self):
        return self.months[self.month - 1]
