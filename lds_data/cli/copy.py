from .. import ldsagent
import os
import json

# metadata contains:
# title (file name as shown to user)
# url (link to AWS excluding any tokens)
# format (html, pdf, etc)
# order: numerical file order (0 = topmost)
# check_http_status: some kind of http status response, maybe pre-scanned
# check_timestamp: presuming this is when the file was last checked (see http_status)
# check_hash: MD5 of the file contents
# check_size: byte size of the file
# check_mimetype: mime type of the file in question
# description: editor's description of the file
# london_res_geo: presumed to be applicable geography


# Download an entire dataset (including resource metadata)
def dataset_download(input_dataset):
    api_key = os.environ['DATASTORE_API']

    agent = ldsagent.LdsAgent(api_key)
    input_resources = agent.get_resources(input_dataset)

    working_dir = "temp-xfer"

    # Check the local folder exists and is empty:
    if not os.path.exists(working_dir):
        os.mkdir(working_dir)
    # We won't empty it automatically since we want the user to check
    if len(os.listdir(working_dir)) != 0:
        raise Exception("%s folder is not empty. Please delete this folder or empty it before proceeding." % working_dir)

    # Write the resource list out to a JSON file:
    filepath = os.path.join(working_dir, ".metadata.json")
    with open(filepath, "w") as json_file:
        json.dump(input_resources, json_file)
    
    for key in input_resources:
        resource = input_resources[key]
        filepath = os.path.join(working_dir, resource["generated_filename"])
        agent.download_resource(input_dataset, key, filepath)



# Copy an entire dataset (including resource metadata)


def dataset_copy(input_dataset, output_dataset):
    raise NotImplementedError("Currently withholding this function while we develop separate download/upload functions")
    
    api_key = os.environ['DATASTORE_API']

    agent = ldsagent.LdsAgent(api_key)
    input_resources = agent.get_resources(input_dataset)

    working_dir = "temp-xfer" # This is where we'll download files (configurable in future)

    # Create a test local dir (need a better way of doing this...)
    if not os.path.exists(working_dir):
        os.mkdir(working_dir)

    # for key in input_resources:
    #     resource = input_resources[key]
    #     # Could eventually dump this in memory
    #     # Here's an issue - "title" isn't necessarily a sensible filename. It's tacked onto the end of the S3 URL.
    #     # Note that check_mimetype is not reliable.

    #     filepath = os.path.join(working_dir, resource["title"])
    #     agent.download_resource(input_dataset, key, filepath)

        
        #
        # Worth nothing that the original file is preserved in the URL. This is useful for downloading with the correct file extension.

        agent.add_resource(output_dataset, filepath, resource['check_mimetype'])
        agent.update_metadata(output_dataset, key, 'title', resource['title'])
        agent.update_metadata(output_dataset, key, 'order', resource['order'])
        

#    os.remove("test-files/a.html")
#    os.rmdir("test-files")
