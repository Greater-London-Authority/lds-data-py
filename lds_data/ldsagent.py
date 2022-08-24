import requests
import os
import json
import hashlib

class EmptyResponseException(Exception):
    pass

class LdsAgent:
    def md5(self, file):
        with open(file, 'rb') as filehandle:
            hash = hashlib.md5()
            # Load data in chunks to avoid memory issues
            # This MUST be a multiple of 128 bytes to use MD5 properly
            for datablock in iter(lambda: filehandle.read(8192), b''):
                hash.update(datablock)
        return hash.hexdigest()

    def __init__(self, api_key):
        self.api_key = api_key
        self.site = 'https://data.london.gov.uk'
        


    # Returns a list of resources
    def get_resources(self, dataset):
        url='%s/api/dataset/%s' % (self.site, dataset)
        r = requests.get(url, headers={'Authorization': self.api_key})
        detail = json.loads(r.text)
        if not 'resources' in detail:
            raise EmptyResponseException()
        return detail['resources']


    # Update an existing resource in this dataset
    def update_resource(self, dataset, key, srcfile):
        url = '%s/api/dataset/%s/resources/%s' % (self.site, dataset, key)
        requests.post(url,
            files = {'file': open(srcfile, 'rb')},
            headers = {'Authorization': self.api_key},
            data = {})

    # Add a new resource to this dataset
    # Don't use this if the file already exists. The server will duplicate it.
    def add_resource(self, dataset, title, srcfile):
        metadata = {}
        url = '%s/api/dataset/%s/resources/' % (self.site, dataset)
        metadata['title'] = title
        requests.post(url,
            files = {'file': open(srcfile, 'rb')},
            headers = {'Authorization': self.api_key},
            data = {})


    # Syncs a local directory with the remote dataset
    # Use with caution! Note, it doesn't delete server-side yet
    def sync_dir(self, dataset, src):
        filemap = {} # This will contain a list of server-side keys using the filename as index
        hash = {} # This will contain a list of hashes (using the filename as index)
        resources = self.get_resources(dataset)
        for k in resources:
            resource = resources[k]
            filemap[resource["title"]] = k
            hash[resource["title"]] = resources[k]['check_hash']

        # Work through the local filesystem
        for file in os.listdir(src):
            metadata = {} # We will use this to update/check relevant metadata

            filepath = ("%s/%s" % (src, file))
            filehash = self.md5(filepath)

        print("Considering file %s for upload" % (file))
        needsPush = False

        if file in filemap.keys():
            key = filemap[file]
            if hash[file] != filehash:
                print ("- Server hash %s differs from client hash %s. Upload required." % (hash[file], filehash))
                self.update_resource(dataset, key, filepath)
            else:
                print ("- Server hash %s matches client hash, so no update required" % (hash[file]))
        else:
            self.add_resource(dataset, file, filepath)



        

