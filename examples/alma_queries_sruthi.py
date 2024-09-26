import sruthi
import argparse
import tomli
import yaml
import pymarc

'''
This script provides an example of how to used the forked version of the sruthi package
with the Alma server.
'''

# initialize argument parser
argParser = argparse.ArgumentParser()

# Adding required argument operation
argParser.add_argument('-o', '--operation', type=str,
                       help="SRU Operation (ex. explain, searchRetrieve)",
                       required=True)

# Adding optional argument query
argParser.add_argument('-q', '--query', type = str,
                       help = "SRU query#")

argParser.print_help()

# Read arguments from command line
args = argParser.parse_args()

# A query is required for the searchRetrieve operation, but not the explain operation
if (args.operation == "searchRetrieve"):
    if(not args.query):
        print("missing conditionally required parameter --query")
        quit()
    print("Using query: % s " % args.query)

if args.operation:
    print("\nInvoking ExLibris Alma SRU API Operation: % s" % args.operation)

def dump(d):
    print(yaml.dump(d, allow_unicode=True, default_flow_style=False))

params = {}
with open("alma_sru_config.toml", mode="rb") as fp:
    config = tomli.load(fp)
    params["url"] = config[args.operation]['url']
    if(args.operation == "searchRetrieve"):
        params["query"] = config["searchRetrieve"][args.query]
        if "output_format" in config["searchRetrieve"]:
            params["output_format"] = config[args.operation]["output_format"]
            print(f"output_format set to: {params['output_format']}")
        if "record_schema" in config["searchRetrieve"]:
            params["record_schema"] = config[args.operation]["record_schema"]

print("\nurl="+params["url"])

if(args.operation == "searchRetrieve"):
    records = sruthi.searchretrieve(**params)
    # Check type of returned object
    print("Type check: ", isinstance(records[0], pymarc.record.Record))
    for record in records:
        if isinstance(record, pymarc.record.Record):
            print("Record author: ", record.author)
        elif isinstance(record, dict):
            print("Record keys: ", record.keys())

if (args.operation == "explain"):
    info = sruthi.explain(**params)
    print("Server: ", info.server)
    print("Index info:")
    dump(info.index)

