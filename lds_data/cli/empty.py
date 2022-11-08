from .. import ldsagent
import os

# Empty a dataset (use with extreme caution!)


def dataset_empty(input_dataset):

    api_key = os.environ['DATASTORE_API']

    agent = ldsagent.LdsAgent(api_key)
    input_resources = agent.get_resources(input_dataset)

    for key in input_resources:
        resource = input_resources[key]
        print("Deleting %s %s" % (resource['title'], key))
        agent.delete_resource(input_dataset, key)
        

#    os.remove("test-files/a.html")
#    os.rmdir("test-files")
