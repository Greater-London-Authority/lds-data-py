from .. import ldsagent
import os

# Copy an entire dataset (including resource metadata)


def dataset_copy(input_dataset, output):

    api_key = os.environ['DATASTORE_API']

    agent = ldsagent.LdsAgent(api_key)
    input_resources = agent.get_resources(input_dataset)

    # Create a test local dir (need a better way of doing this...)
    if not os.path.exists("temp-xfer"):
        os.mkdir("temp-xfer")
    filepath = "temp-xfer/scratch"

    for key in input_resources:
        resource = input_resources[key]
        # Could eventually dump this in memory
        agent.download_resource(input_dataset, key, filepath)

        # Use the resource metadata to send the file back to the server

#    os.remove("test-files/a.html")
#    os.rmdir("test-files")
