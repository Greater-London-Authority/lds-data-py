from .. import ldsagent
import os

# Copy an entire dataset (including resource metadata)


def dataset_copy(input_dataset, output_dataset):

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
        #
        # Worth nothing that the original file is preserved in the URL. This is useful for downloading with the correct file extension.

        agent.add_resource(output_dataset, filepath, resource['check_mimetype'])
        agent.update_metadata(output_dataset, key, 'title', resource['title'])
        agent.update_metadata(output_dataset, key, 'order', resource['order'])
        

#    os.remove("test-files/a.html")
#    os.rmdir("test-files")
