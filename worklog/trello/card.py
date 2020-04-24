import collections

import marshmallow

import worklog.trello.check

FIELDS = ('name', 'checklists', 'idList')

Model = collections.namedtuple('Model', FIELDS)


class Schema(marshmallow.Schema):
    name = marshmallow.fields.Str(required=True)
    checklists = marshmallow.fields.List(
        marshmallow.fields.Nested(worklog.trello.check.ListSchema),
        required=True
    )
    idList = marshmallow.fields.Str(required=True)

    class Meta:
        unknown = marshmallow.EXCLUDE

    @marshmallow.post_load
    def _unmarshal(self, data, **kwargs):
        return Model(**data)
