from services import FirebaseClient


class OrderManager(object):
    def __init__(self):
        self.firebase_client = FirebaseClient()
        self.firebase_client = self.firebase_client.get_firebase_instance

    def getdata(self):
        user_collection = self.firebase_client.collection('user').get()
        print(user_collection)


if __name__ == '__main__':
    a = OrderManager()
    a = a.getdata()
