import hvac


class VaultSecurity:

    def get_vault_client(self):
        client = hvac.Client(url="https://cruize-finance-cluster-public-vault-ffad0228.95440b3b.z1.hashicorp.cloud:8200", token="hvs.CAESIK-PMyo7Hw4UKbiiiazync4HAxj9JC4WHeiSAdfvk5zeGicKImh2cy5rVGFDanBTbWh6VndWV2dMeUhYUldpbFcuYmNPbmgQ2w0")
        return client

    def save(self, credential_path, credential):
        client = self.get_vault_client()
        create_response = client.secrets.kv.v2.create_or_update_secret(
            path=credential_path, secret={credential_path: credential}
        )
        print(create_response)

    def fetch(self, credential_path):
        client = self.get_vault_client()
        read_response = client.secrets.kv.read_secret_version(path=credential_path)
        print(read_response)
        credential = read_response["data"]["data"]
        print(credential)


if __name__ == "__main__":
    a = VaultSecurity()
    a.save("PRIVATE_KEY", "4sd80b2ec698047b62328aa5e0746f44e7d2ecbdb05d2d5bae0c439147abede23")
    # a.save("PRIVATE_KEY2", "4sd80b2ec698047b62328aa5e0746f44e7d2ecbdb05d2d5bae0c439147abede23")
    # a.fetch("PRIVATE_KEY")
