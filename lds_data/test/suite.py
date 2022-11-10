from .. import ldsagent
import os

def test():
    api_key=os.environ['DATASTORE_API']
    dataset = 'lds-api-test-area'

    agent = ldsagent.LdsAgent(api_key)
    resources = agent.get_resources(dataset)
    #assert resources

    # TODO create a clean environment and do proper assertions

    # Create a test local dir:
    if not os.path.exists("lds-api-test-area"):
        os.mkdir("lds-api-test-area")

    agent.sync_dir(dataset, "lds-api-test-area")


#    os.remove("lds-api-test-area/a.html")
#    os.rmdir("lds-api-test-area")

    