import logging
import typing

import marshmallow
import requests

import worklog.trello
import worklog.trello.board
import worklog.trello.cache
import worklog.trello.card
import worklog.trello.config
import worklog.trello.list
import worklog.trello.url

log = logging.getLogger(__name__)


class NoBoardError(Exception):
    pass


class Session:
    def __init__(self,
                 cfg: worklog.trello.config.Params,
                 urls: worklog.trello.url.Builder):
        self._cfg = cfg
        self._urls = urls
        self._session = requests.Session()

    def get_board(self) -> worklog.trello.board.Model:
        log.info('Getting Trello boards...')
        url = self._urls.boards(self._cfg.member_id)
        schema = worklog.trello.board.Schema(many=True)
        boards = self._get(url, schema)
        try:
            return next(b for b in boards
                        if b.name == self._cfg.board_name and not b.closed)
        except StopIteration:
            raise NoBoardError(f'no active board "{self._cfg.board_name}"')

    def get_lists(
            self,
            board: worklog.trello.board.Model
    ) -> typing.Iterable[worklog.trello.list.Model]:
        log.info('Getting Trello lists...')
        url = self._urls.lists(board.id)
        schema = worklog.trello.list.Schema(many=True)
        return self._get(url, schema)

    def get_cards(
            self,
            board: worklog.trello.board.Model
    ) -> typing.Iterable[worklog.trello.card.Model]:
        log.info('Getting Trello cards...')
        url = self._urls.cards(board.id)
        schema = worklog.trello.card.Schema(many=True)
        return self._get(url, schema)

    def _get(self, url: str, schema: marshmallow.Schema) -> typing.Any:
        cache = worklog.trello.cache.File(url)
        if self._cfg.load_cache:
            try:
                data = cache.load()
            except FileNotFoundError:
                pass
            else:
                log.debug('Cache found for %s', url)
                return schema.loads(data)

        reply = self._session.get(url)
        reply.raise_for_status()
        log.debug('Reply: %s', reply.text)
        cache.store(reply.text)
        return schema.loads(reply.text)
