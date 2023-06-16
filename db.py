import pymongo


MAX_RETRIES = 3


class DBException(Exception):
    pass


def retry(num_tries, exceptions):
    def decorator(func):
        def f_retry(*args, **kwargs):
            for i in range(num_tries):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    continue

        return f_retry

    return decorator


# Retry on AutoReconnect exception, maximum 3 times
retry_auto_reconnect = retry(MAX_RETRIES, (pymongo.errors.AutoReconnect,))


class MongoConnector(object):
    def __init__(self):
        self._client = pymongo.MongoClient(
            "mongodb://localhost:27017")
        scannerDb = self._client["webscanner"]
        scannerDb["subscribers"].create_index(
            [
                ("blockchain", pymongo.ASCENDING),
                ("wallet_address", pymongo.ASCENDING),
                ("webhook_url", pymongo.ASCENDING),
            ],
            unique=True,
        )
        scannerDb["transactions"].create_index(
            [
                ("subscriber_id", pymongo.ASCENDING),
                ("txn_hash", pymongo.ASCENDING),
            ],
            unique=True,
        )

    @property
    def client(self):
        return self._client

    @retry_auto_reconnect
    def getDB(self, dbName: str):
        return self.client[dbName]
