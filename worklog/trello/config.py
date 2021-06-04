import collections

import marshmallow

File = collections.namedtuple('File', ('board_name',
                                       'exclude_pattern',
                                       'host',
                                       'member_id',
                                       'protocol',
                                       'version'))


class FileSchema(marshmallow.Schema):
    board_name = marshmallow.fields.Str(required=True)
    exclude_pattern = marshmallow.fields.Str()
    host = marshmallow.fields.Str(required=True)
    member_id = marshmallow.fields.Str(required=True)
    protocol = marshmallow.fields.Str(required=True)
    version = marshmallow.fields.Int(required=True)

    @marshmallow.post_load
    def _unmarshal(self, data, **kwargs):
        return File(**data)


Secrets = collections.namedtuple('Secrets', ('key', 'token'))


class SecretsSchema(marshmallow.Schema):
    key = marshmallow.fields.Str(required=True)
    token = marshmallow.fields.Str(required=True)

    @marshmallow.post_load
    def _unmarshal(self, data, **kwargs):
        return Secrets(**data)


class Params:
    def __init__(self, file: File, secrets: Secrets, load_cache: bool):
        self._file = file
        self._secrets = secrets
        self._load_cache = load_cache

    @property
    def board_name(self) -> str:
        return self._file.board_name

    @property
    def exclude_pattern(self) -> str:
        return self._file.exclude_pattern

    @property
    def host(self) -> str:
        return self._file.host

    @property
    def key(self) -> str:
        return self._secrets.key

    @property
    def load_cache(self) -> bool:
        return self._load_cache

    @property
    def member_id(self) -> str:
        return self._file.member_id

    @property
    def protocol(self) -> str:
        return self._file.protocol

    @property
    def token(self) -> str:
        return self._secrets.token

    @property
    def version(self) -> int:
        return self._file.version
