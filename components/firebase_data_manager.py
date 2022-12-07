import time

# TODO : refactor this file .
from services.firebase_cloud_client import FirebaseClient
from settings_config import firebase_client

"""class :: FirebaseDataManager is used to manage the firebase db oprations such as storing,fetching and updating the 
data. """


class FirebaseDataManager(object):
    def __init__(self):
        self.firebase_client = firebase_client

    """method :: get_firebase_client -  is used to get the firebase client.
       return :: firebase client.
    """

    def get_firebase_client(self):
        if self.firebase_client is None:
            self.firebase_client = FirebaseClient().get_firebase_client
        return self.firebase_client

    """
    method :: update_data -  is used to update the data on firebase db 
    return :: None.
    """

    def update_data(self, order_id, collection, data):
        self.firebase_client = self.get_firebase_client()
        self.firebase_client.collection(collection).document(order_id).update(data)

    """
    method :: store_data -  is used to store the data on firebase db 
    return :: None.
    """

    def store_data(self, data, document, collection_name):
        self.firebase_client = self.get_firebase_client()
        self.firebase_client.collection(collection_name).document(document).set(data)

    """
      method :: bulk_store -  is used to store the data on firebase db  in bulk .
      return :: None.
      """

    def bulk_store(self, data, collection_name, field):
        self.firebase_client = self.get_firebase_client()
        batch = self.firebase_client.batch()
        for key, value in data.items():
            write = self.firebase_client.collection(collection_name).document(key)
            batch.set(write, {field: str(value)})
        batch.commit()

    """
        method :: store_sub_collections  -  is used to store sub_collections the data on firebase db  .
        return :: None.
    """

    def store_sub_collections(
        self, data, collection, document_name, sub_collection, sub_document
    ):
        self.firebase_client = self.get_firebase_client()
        data["timestamp"] = time.time()
        self.firebase_client.collection(collection).document(document_name).collection(
            sub_collection
        ).document(sub_document).set(data)

    """
        method :: fetch_sub_collections  - is used to fetch sub_collections from the firebase db  .
        return :: data of sub collection.
    """

    def fetch_sub_collections(self, collection, document_name, sub_collection):
        self.firebase_client = self.get_firebase_client()
        firebase_data = (
            self.firebase_client.collection(collection)
            .document(document_name)
            .collection(sub_collection)
            .get()
        )
        return firebase_data

    """
         method :: fetch_data  - is used to fetch data from the firebase db  .
         return ::  collection data.
     """

    def fetch_data(self, collection_name, document_name):
        self.firebase_client = self.get_firebase_client()
        firebase_data = (
            self.firebase_client.collection(collection_name)
            .document(document_name)
            .get()
        )
        if firebase_data is not None:
            firebase_data = vars(firebase_data)
        return firebase_data.get("_data", None)

    """
            method :: fetch_collections  - is used to fetch collections  from the firebase db  .
            return ::  collection .
        """

    def fetch_collections(self, collection_name):
        self.firebase_client = self.get_firebase_client()
        collection_obj = self.firebase_client.collection(collection_name)
        collection_data = collection_obj.stream()
        return collection_data


if __name__ == "__main__":
    a = FirebaseDataManager()
    # a = a.fetch_sub_collections(collection="ETHBUSD",document_name="ETHBUSD",sub_collection="prices")
    # for price_floor_detail in a:
    #     print(price_floor_detail.to_dict())
    # a = a.fetch_sub_collections(collection='Price_data',document_name="ETHUSD",sub_collection="Prices")
    # for price_floor_detail in a:
    #     a = price_floor_detail.to_dict()
    #     print(a['prices'])

    # print(a.fetch_collections())
