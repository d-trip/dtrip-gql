from mongoengine import connect, DynamicDocument
from mongoengine.fields import (
    DictField,
    StringField,
)


class PostModel(DynamicDocument):
    body = StringField()
    title = StringField()
    author = StringField()
    permlink = StringField()
    json_metadata = DictField()
    url = StringField(unique=True)

    meta = {
        'ordering': ['-created'],

        'indexes': [
            'author',
            'permlink',
            'created',
            'category',
            'json_metadata.location',
        ],

        'auto_create_index': True,
        'index_background': True
    }
