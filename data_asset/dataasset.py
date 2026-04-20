from azure.ai.ml import MLClient
from azure.identity import DefaultAzureCredential
from azure.ai.ml.entities import Data
from azure.ai.ml.constants import AssetTypes

class TestDataAsset:

    def __init__(self) -> None:
        self.mlclient = MLClient.from_config(credential=DefaultAzureCredential())
    
    def create_DataAsset(self, name: str, path: str, type: str):
        data = Data(
            name=name,
            path=path,
            type=type
        )

        self.mlclient.data.create_or_update(data=data)
        print(f"Data asset created successfully.")

if __name__ == "__main__":
    test = TestDataAsset()
    test.create_DataAsset(
        name="myTestDataAsset",
        path="azureml://subscriptions/c94d6fba-0d29-48cd-9cbb-1f115e688235/resourcegroups/ai-300/workspaces/myworkspace/datastores/myblobdatastore/paths/data/home-rental.csv",
        type=AssetTypes.URI_FILE
    )