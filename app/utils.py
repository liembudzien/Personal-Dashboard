from datetime import datetime, timedelta
from calendar import HTMLCalendar
from models.models import *

class Calendar(HTMLCalendar):
    def __init__(self, year=None, month=None):
        self.year = year
        self.month = month
        super(Calendar, self).__init__()

    def formatday(self, day, events):
        events_per_day_todo = events.filter(task_due_date__day=day, task_completion=False)
        events_per_day_complete = events.filter(task_due_date__day=day, task_completion=True)
        d = ''
        for event in events_per_day_todo:
            d += f'<li> {event.task_name} </li>'

        for event in events_per_day_complete:
            d += f'<li style=\'color: black\'> {event.task_name} </li>'

        if day != 0:
            return f"<td><span class='date'>{day}</span><ul> {d} </ul></td>"
        return '<td></td>'

    def formatweek(self, theweek, events):
        week = ''
        for d, weekday in theweek:
            week += self.formatday(d, events)
        return f'<tr> {week} </tr>'

    def formatmonth(self, withyear=True, user=None):
        events = TaskItem.objects.filter(task_due_date__year=self.year, task_due_date__month=self.month, task_list__task_user=user)
        cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
        cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        cal += f'{self.formatweekheader()}\n'
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f'{self.formatweek(week, events)}\n'
        cal += f'</table>' 
        return cal
    