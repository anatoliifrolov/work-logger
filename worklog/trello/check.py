import collections

import marshmallow

Item = collections.namedtuple('Item', ('name', 'state'))


class ItemSchema(marshmallow.Schema):
    name = marshmallow.fields.Str(required=True)
    state = marshmallow.fields.Str(required=True)

    class Meta:
        unknown = marshmallow.EXCLUDE

    @marshmallow.post_load
    def _unmarshal(self, data, **kwargs):
        return Item(**data)


List = collections.namedtuple('List', ('name', 'items'))


class ListSchema(marshmallow.Schema):
    name = marshmallow.fields.Str(required=True)
    items = marshmallow.fields.List(
        marshmallow.fields.Nested(ItemSchema),
        required=True,
        data_key="checkItems"
    )

    class Meta:
        unknown = marshmallow.EXCLUDE

    @marshmallow.post_load
    def _unmarshal(self, data, **kwargs):
        return List(**data)
