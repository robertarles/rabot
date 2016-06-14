from pymongo import MongoClient
import datetime

class Vault(object):

    def __init__(self):
        pass

    def store(self, message, tags):
        client = MongoClient('mongodb://localhost:27017/')
        db = client['rabot32']
        import datetime
        post = [
            {
                "author": "rabot",
                "message": message,
                "tags": tags,
                "date": datetime.datetime.now(),
                "date_updated": datetime.datetime.now(),
            }
        ]
        posts = db.posts
        results = posts.insert_many(post)
        results.inserted_ids

if __name__ == '__main__':
    vault = Vault()
    vault.store("some test message", ["twitter", "personal", "python"])
