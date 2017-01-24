from pymongo import MongoClient
import datetime


class Vault(object):

    def __init__(self):
        self.client = MongoClient('mongodb://localhost:27017/')
        self.rabot_db = self.client.rabot32

    def store(self, message, tags=["`store`", "message"], author='rabot32'):
        post = [
            {
                "author": author,
                "message": message,
                "tags": tags,
                "date": datetime.datetime.now(),
                "date_updated": datetime.datetime.now(),
            }
        ]
        posts = self.rabot_db.posts
        results = posts.insert_many(post)
        results.inserted_ids

    def store_trends(self, trend_list, tags=["`store`", "trends"], author='rabot32'):
        trends = self.rabot_db.trends
        inserted_ids = []
        for trend in trend_list:
            trend["author"] = author
            trend["tags"] = tags
            trend["date"] = datetime.datetime.now()
            trend["date_updated"] = datetime.datetime.now()
            results = trends.insert_one(trend)
            inserted_ids.append(results.inserted_id)
        return inserted_ids

    def get_recent_activity(self, limit=10, author='rabot32', author_contains=None):
        doc_list = []
        recent_activity = None
        if author_contains is not None:
            recent_activity = self.rabot_db.posts.find(
                {"author": {"$regex": ".*" + author_contains + ".*"}}
            ).limit(limit).sort('date_updated', -1)
        else:
            recent_activity = self.rabot_db.posts.find(
                {"author": {"$eq": author}}
            ).limit(limit).sort('date_updated', -1)
        for doc in recent_activity:
            doc_list.append(doc)
        return doc_list


if __name__ == '__main__':
    vault = Vault()
    vault.store("some test message", ["twitter", "personal", "python"])
    doc_list = vault.get_recent_activity(limit=1, author_contains='32')
    for doc in doc_list:
        print(doc)
