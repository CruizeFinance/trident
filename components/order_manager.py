from settings_config import firebase_client


class OrderManager(object):
    def __init__(self):
        self.firebase_client = firebase_client

    def getdata(self):
        user_collection = self.firebase_client.collection("user").get()
        print(user_collection)


if __name__ == "__main__":
    a = OrderManager()
    a = a.getdata()
