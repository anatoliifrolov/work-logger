import argparse
import datetime
import re
import typing

_DATE_PATTERN = r'\d{4}-\d{2}-\d{2}'


class DateRangeError(Exception):
    pass


class SinceAction(argparse.Action):
    _MATCHER = re.compile(_DATE_PATTERN)

    def __call__(self, parser, namespace, values, option_string=None):
        match = self._MATCHER.match(values)
        if not match:
            raise DateRangeError(f'bad starting date argument: {values}')

        date_from = match.group()
        date_from = datetime.date.fromisoformat(date_from)
        date_to = datetime.date.today()
        setattr(namespace, self.dest, lambda: (date_from, date_to))


class DateRangeAction(argparse.Action):
    _PATTERN = f'({_DATE_PATTERN})/({_DATE_PATTERN})'
    _MATCHER = re.compile(_PATTERN)

    def __call__(self, parser, namespace, values, option_string=None):
        match = self._MATCHER.match(values)
        if not match:
            raise DateRangeError(f'bad date range argument: {values}')

        date_from = match.group(1)
        date_to = match.group(2)
        date_from = datetime.date.fromisoformat(date_from)
        date_to = datetime.date.fromisoformat(date_to)
        setattr(namespace, self.dest, lambda: (date_from, date_to))


class Args:
    def __init__(self):
        parser = argparse.ArgumentParser(
            description='Generates various types of work report',
            prog='work-logger')

        parser.add_argument('-c',
                            '--config',
                            default='config.yaml',
                            help='The configuration file path')
        parser.add_argument('-s',
                            '--secrets',
                            default='secrets.yaml',
                            help='The secrets file path')

        dates = parser.add_mutually_exclusive_group()
        dates.add_argument('-T',
                           '--this-week',
                           action='store_const',
                           const=self._this_week,
                           default=self._this_week,
                           dest='dates_computer',
                           help='Process the current week (default)')
        dates.add_argument('-L',
                           '--last-week',
                           action='store_const',
                           const=self._last_week,
                           dest='dates_computer',
                           help='Process the last week')
        dates.add_argument('-S',
                           '--sliding-week',
                           action='store_const',
                           const=self._sliding_week,
                           dest='dates_computer',
                           help='Process the last seven days')
        dates.add_argument('--since',
                           action=SinceAction,
                           dest='dates_computer',
                           help='An explicit starting date in the form '
                                '"2020-04-27"')
        dates.add_argument('--date-range',
                           action=DateRangeAction,
                           dest='dates_computer',
                           help='An explicit date range in the form '
                                '"2020-04-27/2020-04-30"')

        parser.add_argument('--load-cache',
                            action='store_true',
                            dest='load_cache',
                            help='Read cached responses during this session')

        self._args = parser.parse_args()

    @property
    def config_path(self) -> str:
        return self._args.config

    @property
    def secrets_path(self) -> str:
        return self._args.secrets

    def dates(self) -> typing.Tuple[datetime.date, datetime.date]:
        return self._args.dates_computer()

    @classmethod
    def _this_week(cls) -> typing.Tuple[datetime.date, datetime.date]:
        today = datetime.date.today()
        this_weekday = today.weekday()
        date_from = today - datetime.timedelta(days=this_weekday)
        date_to = date_from + datetime.timedelta(days=6)
        return date_from, date_to

    @classmethod
    def _last_week(cls) -> typing.Tuple[datetime.date, datetime.date]:
        date_from, date_to = cls._this_week()
        date_from -= datetime.timedelta(weeks=1)
        date_to -= datetime.timedelta(weeks=1)
        return date_from, date_to

    @classmethod
    def _sliding_week(cls) -> typing.Tuple[datetime.date, datetime.date]:
        date_to = datetime.date.today()
        date_from = date_to - datetime.timedelta(weeks=1)
        return date_from, date_to

    @property
    def load_cache(self) -> bool:
        return self._args.load_cache
