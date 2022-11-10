from .. import ldsagent
import os

def test():
    api_key=os.environ['DATASTORE_API']
    dataset = 'lds-api-test-area'

    agent = ldsagent.LdsAgent(api_key)
    resources = agent.get_resources(dataset) # This will issue a 404 if not found
    
    #agent.debug_traffic = True # Enables HTTP traffic debugging
    for resource_id in resources.keys():
        agent.delete_resource(dataset, resource_id)
    
    # Create a test local dir:
    if not os.path.exists("lds-api-test-area"):
        os.mkdir("lds-api-test-area")

    # Ensure the local dir is empty so we can properly test it:
    for filename in os.listdir(dataset):
        filepath = os.path.join(dataset, filename)
        if os.path.isfile(filepath):
            os.unlink(filepath)

    # Create a file locally and send it to the server:
    filepath = os.path.join(dataset, "test-file.txt")
    f = open(filepath, 'w')
    f.write("Test file")
    f.close()

    # Upload this test file
    print("Uploading %s" % filepath)
    agent.add_resource(dataset, filepath, "text/plain")

    # Observe the file on the server:
    resources = agent.get_resources(dataset)
    
#    if len(resources) == 0:
#        raise Exception("No resources on server. Looks like file upload did not work.")
#    if len(resources) > 1:
#        raise Exception("%d resources on server. Only expected 1." % len(resources))

    resource_id = list(resources.keys())[0]
    file = resources[resource_id]
    
    # Check hash is intact
    hash = file['check_hash']
    if hash != 'edc900745c5d15d773fbcdc0b376f00c': # md5 of "Test file"
        raise Exception("Hash is incorrect, was %s" % hash)

    # Delete the resource on the server:
    print("Deleting file")
    agent.delete_resource(dataset, resource_id)



    #agent.sync_dir(dataset, "lds-api-test-area")


#    os.remove("lds-api-test-area/a.html")
#    os.rmdir("lds-api-test-area")

    