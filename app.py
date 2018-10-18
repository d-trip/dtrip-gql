from flask import Flask
from flask_graphql import GraphQLView
from flask_cors import CORS
from mongoengine import connect
from main import DB_HOST, DB_NAME

import graphene
from raven.contrib.flask import Sentry

import query

app = Flask(__name__)
app.debug = True
CORS(app)
Sentry(app)

connect(DB_NAME, host=DB_HOST)

schema = graphene.Schema(query=query.Queries)
app.add_url_rule('/graphql', view_func=GraphQLView.as_view('graphql',
                                                           schema=schema,
                                                           graphiql=True))

if __name__ == '__main__':
    app.run()
