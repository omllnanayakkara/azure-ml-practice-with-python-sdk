# Run a job without using data assets and datastores

from azure.ai.ml import MLClient, command, Input, Output
from azure.ai.ml.constants import AssetTypes, InputOutputModes
from azure.ai.ml.entities import ManagedIdentityConfiguration, UserIdentityConfiguration
from azure.identity import DefaultAzureCredential, ManagedIdentityCredential
import random

mlclient = MLClient.from_config(
    credential=DefaultAzureCredential(logging_enable=True),
    # file_name="..\\config.json"
)

path = "wasbs://mycontainer@lahirustorageaccount0411.blob.core.windows.net/data/home-rental.csv" # private file
# out_path must be a datastore uri
out_path = "wasbs://mycontainer@lahirustorageaccount0411.blob.core.windows.net/data/home-rental-copy.csv" # write path

inputs = {
    "input_data": Input(
        path=path,
        type=AssetTypes.URI_FILE,
        mode=InputOutputModes.RO_MOUNT
    )
}

outputs = {
    "output_data": Output(
        type=AssetTypes.URI_FILE,
        path=out_path,
        mode=InputOutputModes.UPLOAD
    )
}

job_no = random.randint(10, 100)

job1 = command(
    command="head ${{inputs.input_data}}",
    compute="amlcluster",
    display_name=f"Test {job_no} run without data assets",
    name=f"test-{job_no}-without-data-assets",
    inputs=inputs,
    environment="my-test-environment:2",
    experiment_name="my-test-experiments",
)

job2 = command(
    command="cp ${{inputs.input_data}} {{outputs.output_data}}",
    compute="amlcluster",
    display_name=f"Test {job_no} run without data assets - write",
    name=f"test-{job_no}-without-data-assets--write",
    inputs=inputs,
    outputs=outputs,
    environment="my-test-environment:2",
    experiment_name="my-test-experiments",
)

job3 = command(
    command="head ${{inputs.input_data}}",
    compute="amlcluster",
    display_name=f"Test {job_no} run with data assets - read",
    name=f"test-{job_no}-with-data-assets--read",
    inputs={
        "input_data": Input(
            path=mlclient.data.get(
                name="myTestDataAsset",
                version="1"
            ).id,
            type=AssetTypes.URI_FILE,
            mode=InputOutputModes.RO_MOUNT
        )
    },
    environment="my-test-environment:2",
    experiment_name="my-test-experiments",
    identity=ManagedIdentityConfiguration(
        object_id="22c26bd4-67e9-4d51-b362-e5144e925f85"
    )
)


result = mlclient.jobs.create_or_update(job3)
print(f"Monitor your job at: {result.studio_url}")