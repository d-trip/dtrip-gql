import os
import json
import argparse

from funcy.flow import silent
from steem.post import Post
from mongoengine import connect
from steem.blockchain import Blockchain

from main import DB_HOST, DB_NAME
from posts.models import PostModel


parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description="Command line tool to interact with the DTrip Backend")


parser.add_argument(
    '--resync',
    nargs='?',
    const=True,
    help='Resync database'
)

args = parser.parse_args()


APP_TAG = os.getenv('APP_TAG', 'dtrip')

mongo = connect(DB_NAME, host=DB_HOST)

if args.resync:
    mongo.drop_database(DB_NAME)


class Settings:
    def __init__(self, mongo):
        self._settings = mongo[DB_NAME]['settings']

        if not self._settings.find_one():
            self._settings.insert_one({
                "last_block": None,
            })

    def last_block(self):
        return self._settings.find_one().get('last_block', 1)

    def update_last_block(self, block_num):
        return self._settings.update_one({}, {"$set": {'last_block': block_num}})


settings = Settings(mongo)
blockchain = Blockchain()

BLOCK_NUM = settings.last_block() or blockchain.get_current_block_num()
print(BLOCK_NUM)

# BLOCK_NUM = 26052441
# print(BLOCK_NUM)  # POST 26052437


def fix_legacy_json(json):
    # Coordinates
    if 'location' in json and isinstance(json['location'], dict):
        if json['location'].keys() >= {'name', 'lat', 'lng'}:
            json['location'] = {
                'geometry': {
                  'type': 'Point',
                  'coordinates': [
                      json['location']['lng'],
                      json['location']['lat']
                  ]
                },
                'properties': {
                  'name': json['location']['name']
                }
            }

    return json


def handle_post(post):
    meta = silent(json.loads)(post['json_metadata']) or {}

    if not isinstance(meta, dict):
        return

    meta.setdefault('tags', post['parent_permlink'])

    if APP_TAG in meta['tags']:
        post = Post(post).export()
        if post['depth'] > 0:
            return

        del post['id']
        post['tags'] = list(post['tags'])
        post['json_metadata'] = fix_legacy_json(meta)
        PostModel.objects(url=post['url']).update(upsert=True, **post)

        print('saved', post['url'])


def get_posts(query):
    return blockchain.steem.get_discussions_by_created(query)


def parse():
    if args.resync:
        query = {'tag': APP_TAG, 'limit': 100}
        posts = get_posts(query)

        while True:
            for post in posts:
                handle_post(post)

            query['start_author'] = post['author']
            query['start_permlink'] = post['permlink']

            posts = get_posts(query)

            if len(posts) == 1 and posts[0]['url'] == post['url']:
                break

        print('Posts Synced')

    for op in blockchain.stream(filter_by=['comment'], start_block=BLOCK_NUM):
        handle_post(op)
        settings.update_last_block(op['block_num'])


if __name__ == '__main__':
    try:
        parse()
    except KeyboardInterrupt:
        print('Exit...')
