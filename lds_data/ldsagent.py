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
        # Fail if the API key is not set (for now...)
        if api_key == None:
            raise 'API Key not set'
        self.api_key = api_key
        self.site = 'https://data.london.gov.uk'
        


    # Returns a list of resources
    def get_resources(self, dataset):
        url='%s/api/dataset/%s' % (self.site, dataset)
        r = requests.get(url, headers={'Authorization': self.api_key})
        r.raise_for_status()
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

    # Downloads a resource in this dataset
    def download_resource(self, dataset, key, destfile):
        # Despite the public URL showing otherwise, we don't need the filename at the end. This is enough:
        url = '%s/download/%s/%s' % (self.site, dataset, key)
        response = requests.get(url,
            headers = {'Authorization': self.api_key})
        open(destfile, "wb").write(response.content)


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


    # Downloads all resources in a dataset to a local folder
    def download_dataset(self, dataset, dest):
        filemap = {} # This will contain a list of client-side keys using the filename as index

        # Create a dict of local hashes
        for file in os.listdir(dest):
            filepath = ("%s/%s" % (dest, file))
            filehash = self.md5(filepath)
            filemap[file] = filehash

        # Iterate over the server resources and decide what to download
        resources = self.get_resources(dataset)
        for key in resources:
            resource = resources[key]
            serverhash = resource['check_hash']
            filename = resource["title"]

            # We need to rewrite the doc title back into something useful for Windows
            format = (".%s" % resource["format"])
            # If the title already contains the suffix, don't bother replacing it:
            if filename.endswith(format):
                pass # Already have a happy ending
            else:
                filename = ("%s%s" % (filename, format))


            print("Considering file %s for download" % (filename))

            filepath = ("%s/%s" % (dest, filename))

            if filename in filemap.keys():
                filehash = filemap[filename]
                if serverhash != filehash:
                    print ("- Server hash %s differs from client hash %s. Download required." % (serverhash, filehash))
                    self.download_resource(dataset, key, filepath)
                else:
                    print ("- Server hash %s matches client hash, so no download required" % (serverhash))
            else:
                print ("- File %s does not exist client side, so download is required" % (filename))
                self.download_resource(dataset, key, filepath)


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



        

