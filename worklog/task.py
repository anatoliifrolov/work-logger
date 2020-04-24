import datetime
import logging
import re

import worklog.log
import worklog.trello.card
import worklog.trello.list

log = logging.getLogger(__name__)


class Error(Exception):
    pass


class FormatError(Error):
    pass


class EmptyError(Error):
    pass


class Model:
    _PATTERN = r'^(?P<id>[A-Z]+-\d+)\s+(?P<name>.+)$'
    _MATCHER = re.compile(_PATTERN)

    def __init__(self,
                 card_list: worklog.trello.list.Model,
                 card: worklog.trello.card.Model,
                 date_from: datetime.date,
                 date_to: datetime.date):
        match = self._MATCHER.match(card.name)
        if not match:
            raise FormatError(f'unexpected card name "{card.name}"')

        self.logs = []
        for checklist in card.checklists:
            try:
                record = worklog.log.Record(checklist)
            except worklog.log.Error as err:
                log.warning('Cannot make a task: %s', err)
            else:
                if record.date < date_from:
                    continue
                if date_to < record.date:
                    continue
                self.logs.append(record)

        if len(self.logs) == 0:
            raise EmptyError(
                f'no matching checklists in card "{card.name}"'
            )

        self.id = match.group('id')
        self.name = match.group('name')
        self.list_name = card_list.name
