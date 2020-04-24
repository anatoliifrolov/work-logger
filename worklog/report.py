import datetime
import logging
import os
import typing

import worklog.config
import worklog.task
import worklog.trello.card
import worklog.trello.list

log = logging.getLogger(__name__)


class Builder:
    def __init__(self,
                 cfg: worklog.config.Params,
                 lists: typing.Iterable[worklog.trello.list.Model],
                 cards: typing.Iterable[worklog.trello.card.Model]):
        log.info('Generating report for %s..%s', cfg.date_from, cfg.date_to)
        self._cfg = cfg

        lists_by_id = {l.id: l for l in lists}

        self._tasks = []
        for card in cards:
            try:
                card_list = lists_by_id[card.idList]
                task = worklog.task.Model(card_list,
                                          card,
                                          cfg.date_from,
                                          cfg.date_to)
            except worklog.task.Error as err:
                log.warning('Task excluded from report: %s', err)
            else:
                self._tasks.append(task)

    def jira(self) -> str:
        line = f'{self._cfg.author_name}:'
        lines = [line]
        for task in self._tasks:
            line = f'* {task.id} ({task.name}) - {task.list_name}'
            lines.append(line)
        return os.linesep.join(lines)

    def human(self) -> str:
        lines = []
        for task in self._tasks:
            line = f'{task.id} "{task.name}":'
            lines.append(line)
            for record in task.logs:
                line = self._format_time(record.date, record.duration)
                lines.append(line)
                lines.extend(f'* {a}' for a in record.actions)
            lines.append('')
        return os.linesep.join(lines)

    def summary(self):
        by_date = {}
        for task in self._tasks:
            for record in task.logs:
                if record.date in by_date:
                    by_date[record.date] += record.duration
                else:
                    by_date[record.date] = record.duration
        lines = []
        for date in sorted(by_date.keys()):
            if date.weekday() in (5, 6):
                log.warning('Worked on weekends')
            duration = by_date[date]
            if duration != datetime.timedelta(hours=8):
                log.warning('Worked %s on %s', duration, date)
            line = self._format_time(date, duration)
            lines.append(line)
        return os.linesep.join(lines)

    @classmethod
    def _format_time(cls,
                     date: datetime.date,
                     duration: datetime.timedelta) -> str:
        date = date.strftime('%A, %m.%d')
        return f'{date}, {duration}'
