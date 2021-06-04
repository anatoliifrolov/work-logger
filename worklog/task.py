import logging
import re

import worklog.config
import worklog.log
import worklog.trello.card
import worklog.trello.list

log = logging.getLogger(__name__)


class Error(Exception):
    pass


class Model:
    _PATTERN = r'^(?P<id>[A-Z]+-\d+)\s+(?P<name>.+)$'
    _MATCHER = re.compile(_PATTERN)

    def __init__(self,
                 card_list: worklog.trello.list.Model,
                 card: worklog.trello.card.Model,
                 cfg: worklog.config.Params = None):
        match = self._MATCHER.match(card.name)
        if not match:
            raise Error(f'unexpected card name "{card.name}"')

        self.id = match.group('id')
        self.name = match.group('name')
        self.title = card.name
        self.status = card_list.name
        self.activity_date = card.dateLastActivity.date()
        self.logs = []
        for checklist in card.checklists:
            try:
                record = worklog.log.Record(checklist)
            except worklog.log.Error as err:
                log.warning('In card %s: %s', card.name, err)
            else:
                if record.date < cfg.date_from:
                    continue

                if cfg.date_to < record.date:
                    continue

                self.logs.append(record)
