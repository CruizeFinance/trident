import hvac
from decouple import config

from utilities import cruize_constants


class VaultSecurity:
    def get_vault_client(self):
        client = hvac.Client(
            url=cruize_constants.VAULT_URL,
            token=config("VAULT_TOKEN"),
            namespace="admin",
        )
        return client

    def save(self, path, data):
        client = self.get_vault_client()
        response = client.secrets.kv.v2.create_or_update_secret(
            path=path, secret={path: data}
        )
        print("Successfully saved data: {}".format(response))

    def fetch(self, path):
        client = self.get_vault_client()
        read_response = client.secrets.kv.read_secret_version(path=path)
        data = read_response["data"]["data"]
        return data


if __name__ == "__main__":
    a = VaultSecurity()
    a.save("PRIVATE_KEY", "123")
    # print(a.fetch("PRIVATE_KEY"))
