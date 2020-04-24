import collections
import typing

import marshmallow
import yaml

import worklog.command
import worklog.trello.config

File = collections.namedtuple('File', ('author_name', 'trello'))


class FileSchema(marshmallow.Schema):
    author_name = marshmallow.fields.Str(required=True)
    trello = marshmallow.fields.Nested(worklog.trello.config.FileSchema,
                                       required=True)

    @marshmallow.post_load
    def _unmarshal(self, data, **kwargs):
        return File(**data)


Secrets = collections.namedtuple('Secrets', ('trello',))


class SecretsSchema(marshmallow.Schema):
    trello = marshmallow.fields.Nested(worklog.trello.config.SecretsSchema,
                                       required=True)

    @marshmallow.post_load
    def _unmarshal(self, data, **kwargs):
        return Secrets(**data)


class Params:
    def __init__(self, args: worklog.command.Args):
        self._config = self._load(args.config_path, FileSchema())
        self._secrets = self._load(args.secrets_path, SecretsSchema())
        self._date_from, self._date_to = args.dates()
        self._trello = worklog.trello.config.Params(self._config.trello,
                                                    self._secrets.trello,
                                                    args.load_cache)

    @classmethod
    def _load(cls, path: str, schema: marshmallow.Schema) -> typing.Any:
        with open(path) as file:
            data = file.read()
            content = yaml.load(data, Loader=yaml.FullLoader)
            return schema.load(content)

    @property
    def author_name(self):
        return self._config.author_name

    @property
    def date_from(self):
        return self._date_from

    @property
    def date_to(self):
        return self._date_to

    @property
    def trello(self):
        return self._trello
