import graphene

from posts.types import Post
from posts.models import PostModel
from posts.utils import CustomMongoengineConnectionField
from posts.utils import qs_ab_filter


class Geometry(graphene.ObjectType):
    type = graphene.String()
    coordinates = graphene.List(graphene.Float)


class PostFilters(graphene.InputObjectType):
    type = graphene.String()
    country = graphene.List(graphene.Float)


class PostOrderingEnum(graphene.Enum):
    created_ASC = '-created'
    created_DESC = 'created'
    total_payout_value_ASC = '-total_payout_value'
    total_payout_value_DESC = 'total_payout_value'


class PostQuery(graphene.ObjectType):
    posts = CustomMongoengineConnectionField(
        Post,
        filters=PostFilters(),
        orderBy=PostOrderingEnum(),
    )

    geo_objects = graphene.List(
        Post,
        bbox=graphene.List(
            graphene.List(graphene.Float)
        )
    )

    def resolve_geo_objects(self, info, bbox):
        return PostModel.objects(
            json_metadata__location__geometry__geo_within_box=bbox
        )

    def resolve_posts(self, info, args):
        qs = PostModel.objects()

        if 'orderBy' in args:
            qs = qs.order_by(args['orderBy'])
        if 'type' in args['filters']:
            qs = qs.filter(json_metadata__type__=args['filters']['type'])

        return qs_ab_filter(qs, args)

    def resolve_post(self, context, identifier=None):
        author, permlink = identifier[1:].split('/')

        return PostModel.objects(author=author, permlink=permlink).first()
