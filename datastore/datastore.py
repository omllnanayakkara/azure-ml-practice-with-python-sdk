from azure.ai.ml import MLClient
from azure.identity import DefaultAzureCredential
from azure.ai.ml.entities import AzureBlobDatastore

class TestDatastore:

    def __init__(self) -> None:
        self.mlClient = MLClient.from_config(credential=DefaultAzureCredential())

    def create_store(self):
        datastore = AzureBlobDatastore(
            name="mytestdatastore",
            account_name="lahirustorageaccount0411",
            container_name="mycontainer"
        )
        try:
            result = self.mlClient.datastores.create_or_update(datastore=datastore)
            print(f"Datastore with name {result.name} is created successfully.")
        except Exception as ex:
            print(f"Failed to create datastore: {ex}")


if __name__ == "__main__":
    test = TestDatastore()
    test.create_store()