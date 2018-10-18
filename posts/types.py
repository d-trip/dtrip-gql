import graphene

from graphene.relay import Node
from graphene_mongo import MongoengineObjectType
from graphene.types.generic import GenericScalar

from posts.models import PostModel


class Post(MongoengineObjectType):
    json_metadata = GenericScalar()

    class Meta:
        description = '''
            All posts.
            Pagination - posts is divided into pages,
            use page param: page=2
        '''
        model = PostModel
        interfaces = (Node,)

    def resolve_json_metadata(self, info):
        return self.json_metadata
