# lds-data-py
Package of tools to interrogate London Datastore with Python

Vaguely inspired by https://github.com/Greater-London-Authority/ldndatar although won't be API-compatible for a while.

# Warning
This is an extremely unstable implementation. Classes and functions are likely to change rapidly.

If you're interested in using it, please contact Sven <sven.latham@london.gov.uk> and we can work together!

# Usage
Get the latest version:
```
pip install git+ssh://git@github.com/Greater-London-Authority/lds-data-py.git
```

Run the CLI (basic interactions):
```
python cli.py -a {action} -i {input dataset} [-o {output dataset}]
```


# Example

```python
from lds_data import ldsagent
# api_key is the API key of your user from https://data.london.gov.uk/user
agent = LdsAgent(api_key)

# To get a list of resources
# dataset -> the dataset's slug (string)
resources = agent.get_resources(dataset)

# To add a new resource
# title -> the title of the file (string)
# srcpath -> the path to the file locally (string)
agent.add_resource(dataset, title, srcpath)

# To replace an existing resource
# key -> server-side identifier for the resource (obtained from get_resources)
# srcpath -> the path of the replacement file
agent.update_resource(dataset, key, srcpath)

# To sync a local folder remotely (copy local files to remote if newer)
# Note this doesn't currently delete files on the server
# dataset -> the dataset's slug
# localdir -> local directory to mirror (without closing slash)
agent.sync_dir(dataset, localdir)
```