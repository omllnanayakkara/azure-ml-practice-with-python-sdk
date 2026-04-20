from azure.ai.ml import MLClient
from azure.identity import DefaultAzureCredential, ManagedIdentityCredential
from azure.ai.ml.entities import AzureBlobDatastore

class TestDatastore:

    def __init__(self) -> None:
        self.mlClient = MLClient.from_config(credential=DefaultAzureCredential())
        wps = self.mlClient.workspaces.list()
        for wp in wps:
            print(f"Workspace name: {wp.name}")

    def create_store(self):
        datastore = AzureBlobDatastore(
            name="mytestdatastore",
            account_name="lahirustorageaccount0411",
            container_name="mycontainer",
        )
        try:
            result = self.mlClient.datastores.create_or_update(datastore=datastore)
            print(f"Datastore with name {result.name} is created successfully.")
        except Exception as ex:
            print(f"Failed to create datastore: {ex}")

    def update_store_credential_type(self, name:str):
        ds = self.mlClient.datastores.get(name=name)
        
        # update credentials to managed identity (pseudo-structure - set fields required by your SDK version)
        ds.properties["credentials"] = {
        "credentialsType": "ManagedIdentity",
        "managedIdentity": {
            "resourceId": "/subscriptions/c94d6fba-0d29-48cd-9cbb-1f115e688235/resourcegroups/ai-300/providers/Microsoft.MachineLearningServices/workspaces/myworkspace"
        }
        }
        # push update (call/method name depends on SDK version)
        self.mlClient.datastores.create_or_update(ds)

if __name__ == "__main__":
    test = TestDatastore()
    # test.update_store_credential_type("MyBlobDatastore")
    