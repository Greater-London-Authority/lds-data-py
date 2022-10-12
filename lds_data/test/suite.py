from .. import ldsagent
import os

def test():
    api_key=os.environ['DATASTORE_API']
    dataset = 'test-files'

    agent = ldsagent.LdsAgent(api_key)
    resources = agent.get_resources(dataset)
    #assert resources

    # TODO create a clean environment and do proper assertions

    # Create a test local dir:
    if not os.path.exists("test-files"):
        os.mkdir("test-files")

    agent.sync_dir(dataset, "test-files")


#    os.remove("test-files/a.html")
#    os.rmdir("test-files")

    