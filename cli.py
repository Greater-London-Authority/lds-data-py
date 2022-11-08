from lds_data import ldsagent
from lds_data.cli import copy, empty
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("-i", "--input", help="Dataset to read from (input)")
parser.add_argument("-o", "--output", help="Dataset to write to (output)")
parser.add_argument("-a", "--action", help="Action to run")
parser.add_argument("--confirm", help="This is needed to perform damaging actions (such as delete)", action='store_true')
args = parser.parse_args()


if args.action == 'copy':
    if args.input == None:
        raise "Input dataset must be specified"
    if args.output == None:
        raise "Output dataset must be specified"
    copy.dataset_copy(args.input, args.output)
elif args.action == 'delete':
    if args.input == None:
        raise "Input dataset must be specified"
    if args.confirm == None:
        raise "You must also confirm the action (provide a --confirm argument)"
    empty.dataset_empty(args.input)
else:
    parser.print_help()



