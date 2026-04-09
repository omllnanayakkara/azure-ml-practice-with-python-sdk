from azure.ai.ml import MLClient
from azure.ai.ml.entities import Workspace
from azure.identity import DefaultAzureCredential


class TestWorkspace:

    def __init__(self):
        self.mlClient = MLClient(credential=DefaultAzureCredential(), subscription_id="c94d6fba-0d29-48cd-9cbb-1f115e688235", resource_group_name="ai-300")

    # Create
    def create_workspace(self):
        workspace = Workspace(
            name="myworkspace",
            resource_group="ai-300",
            display_name="My Workspace"
        )

        result = self.mlClient.workspaces.begin_create(workspace=workspace).result()
        print(f"Workspace created successfully with the name: {result.display_name}")

    # Get
    def get_workspace(self, name:str) -> Workspace | None:
        try:
            wp = self.mlClient.workspaces.get(name=name)
            print(f"Workspace with name {wp.name} fetched successfully")
            return wp
        except Exception as e:
            print(f"Failed to fetch workspace: {e}")
            return None
        
    def delete_workspace(self, name:str) -> None :
        try:
            self.mlClient.workspaces.begin_delete(name=name, delete_dependent_resources=True).result()
            print(f"Workspace with name {name} deleted successfully")
        except Exception as e:
            print(f"Failed to delete workspace: {e}")
        

if __name__ == "__main__":
    test = TestWorkspace()
    wp = test.get_workspace(name="myworkspace")
    test.delete_workspace(name=wp.name)
