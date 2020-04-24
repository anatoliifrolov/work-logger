import worklog.trello.board
import worklog.trello.card
import worklog.trello.config
import worklog.trello.list


class Builder:
    def __init__(self, cfg: worklog.trello.config.Params):
        self._root = f'{cfg.protocol}://{cfg.host}/{cfg.version}'
        self._params = {
            'key': cfg.key,
            'token': cfg.token,
        }

    def boards(self, member_id: str) -> str:
        path = f'/members/{member_id}/boards'
        fields = ','.join(worklog.trello.board.FIELDS)
        params = {'fields': fields}
        return self._build(path, params)

    def lists(self, board_id: str) -> str:
        path = f'/boards/{board_id}/lists'
        fields = ','.join(worklog.trello.list.FIELDS)
        params = {'fields': fields}
        return self._build(path, params)

    def cards(self, board_id: str) -> str:
        path = f'/boards/{board_id}/cards/visible'
        fields = ','.join(worklog.trello.card.FIELDS)
        params = {
            "checklists": "all",
            "fields": fields,
        }
        return self._build(path, params)

    def _build(self, path: str, params=None):
        params = params or {}
        params.update(self._params)
        query = "&".join("=".join(p) for p in params.items())
        return f"{self._root}{path}?{query}"
