from pymongo import MongoClient
import datetime

class Vault(object):

    def __init__(self):
        self.client = MongoClient('mongodb://localhost:27017/')
        self.rabot_db = self.client.rabot32

    def store(self, message, tags=["`store`"], author='rabot32'):
        import datetime
        post = [
            {
                "author": author,
                "message": message,
                "tags": tags,
                "date": datetime.datetime.now(),
                "date_updated": datetime.datetime.now(),
            }
        ]
        posts = self.rabot32_db.posts
        results = posts.insert_many(post)
        results.inserted_ids

    def get_recent_activity(self, limit=10):
        doc_list = []
        recent_activity = self.rabot_db.posts.find().limit(limit).sort('date_updated', -1)
        for doc in recent_activity:
            doc_list.append(doc)
        return doc_list


if __name__ == '__main__':
    vault = Vault()
    vault.store("some test message", ["twitter", "personal", "python"])
