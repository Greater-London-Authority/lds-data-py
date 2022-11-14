from lds_data import ldsagent
from lds_data.cli import copy, empty
from argparse import ArgumentParser
import os

parser = ArgumentParser()
parser.add_argument("-i", "--input", help="Dataset to read from (input)")
parser.add_argument("-o", "--output", help="Dataset to write to (output)")
parser.add_argument("-a", "--action", help="Action to run")
parser.add_argument("--confirm", help="This is needed to perform damaging actions (such as delete)", action='store_true')
args = parser.parse_args()

# Basic CLI Exception to track general user feedback
class CliInvocationException(Exception):
    def __init__(self, message):
        self.message = message

def handle_invocation(args):
    if args.action == 'copy':
        # API check
        if 'DATASTORE_API' not in os.environ:
            raise CliInvocationException("DATASTORE_API environment variable must be specified")

        if args.input == None:
            raise CliInvocationException("Input dataset must be specified")
        if args.output == None:
            raise CliInvocationException("Output dataset must be specified")
        copy.dataset_copy(args.input, args.output)

        
    elif args.action == 'download':
        # API check
        if 'DATASTORE_API' not in os.environ:
            raise CliInvocationException("DATASTORE_API environment variable must be specified")

        if args.input == None:
            raise CliInvocationException("Input dataset must be specified")
        copy.dataset_download(args.input)


    elif args.action == 'delete':
        if 'DATASTORE_API' not in os.environ:
            raise CliInvocationException("DATASTORE_API environment variable must be specified")

        if args.input == None:
            raise CliInvocationException("Input dataset must be specified")
        if args.confirm == None:
            raise CliInvocationException("You must also confirm the action (provide a --confirm argument)")
        empty.dataset_empty(args.input)
    else:
        parser.print_help()



try:
    handle_invocation(args)
except CliInvocationException as ex:  
    print("Error: %s" % ex.message)