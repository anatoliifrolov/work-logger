import collections

import marshmallow

FIELDS = ('closed', 'id', 'name')

Model = collections.namedtuple('Model', FIELDS)


class Schema(marshmallow.Schema):
    closed = marshmallow.fields.Bool(required=True)
    id = marshmallow.fields.Str(required=True)
    name = marshmallow.fields.Str(required=True)

    @marshmallow.post_load
    def _unmarshal(self, data, **kwargs):
        return Model(**data)
