import datetime
import re

import worklog.trello
import worklog.trello.check


class Error(Exception):
    pass


class Record:
    _PATTERN = r'^(?P<month>\d{2})' \
               r'\.(?P<day>\d{2})' \
               r',\s+(?P<quantity>\d)' \
               r'(?P<unit>d|h)$'
    _MATCHER = re.compile(_PATTERN)

    def __init__(self, checklist: worklog.trello.check.List):
        match = self._MATCHER.match(checklist.name)
        if not match:
            raise Error(f'unexpected checklist name "{checklist.name}"')

        month = int(match.group('month'))
        day = int(match.group('day'))
        quantity = int(match.group('quantity'))
        unit = match.group('unit')

        self.date = datetime.date.today().replace(month=month, day=day)
        self.duration = {
            "d": datetime.timedelta(hours=8 * quantity),
            "h": datetime.timedelta(hours=quantity),
        }[unit]
        self.actions = [i.name for i in checklist.items]
