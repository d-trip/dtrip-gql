from mongoengine import DynamicDocument
from mongoengine.fields import (
    DictField,
    StringField,
    IntField,
    DateTimeField,
    BooleanField,
    FloatField,
    ObjectId,
    ListField
)


class PostModel(DynamicDocument):
    url = StringField()
    abs_rshares = IntField()
    active = DateTimeField()
    allow_curation_rewards = BooleanField()
    allow_replies = BooleanField()
    allow_votes = BooleanField()
    active_votes = DictField()
    author = StringField()
    author_rewards = IntField()
    body = StringField()
    cashout_time = DateTimeField()
    category = StringField()
    children = IntField()  # TODO сделать вывод количества всех комментариев
    children_abs_rshares = IntField()
    children_rshares2 = IntField()
    created = DateTimeField()
    curator_payout_symbol = StringField()
    curator_payout_value = DictField()
    depth = IntField()
    json_metadata = DictField()
    last_payout = DateTimeField()
    last_update = DateTimeField()
    max_accepted_payout_symbol = StringField()
    max_accepted_payout_value = FloatField()
    max_cashout_time = DateTimeField()
    mode = StringField()
    net_rshares = IntField()
    net_votes = IntField()
    parent_author = StringField()
    parent_permlink = StringField()
    percent_steem_dollars = IntField()
    permlink = StringField()
    removed = BooleanField()
    reward_weight = IntField()
    root_comment = ObjectId()
    title = StringField()
    total_payout_symbol = StringField()
    total_payout_value = FloatField()
    total_vote_weight = IntField()
    vote_rshares = IntField()
    author_reputation = IntField()
    beneficiaries = ListField(DictField())
    body_length = IntField()
    community = StringField()
    identifier = StringField()
    max_accepted_payout = DictField()
    patched = BooleanField()
    pending_payout_value = DictField()
    promoted = DictField()
    reblogged_by = ListField(StringField())
    replies = ListField(StringField())  # TODO StringField?
    root_author = StringField()
    root_identifier = StringField()
    root_permlink = StringField()
    root_title = StringField()
    tags = ListField(StringField())
    total_payout_value = DictField()
    total_pending_payout_value = DictField()
    total_vote_weight = IntField()
    vote_rshares = IntField()

    meta = {
        'ordering': ['-created'],

        'indexes': [
            'author',
            'permlink',
            'created',
            'category',
            'json_metadata.location',
            'depth',
            'root_comment',
            'parent_permlink',
            'parent_author',
            'mode',
        ],

        'auto_create_index': True,
        'index_background': True
    }
