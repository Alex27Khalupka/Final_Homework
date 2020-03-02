# https://gist.github.com/belovmd/11eec9e26185e0425468fb712c374fba
# https://news.yahoo.com/rss/
import argparse
import json
import urllib.request
from all_functions import get_item
from all_functions import print_parsed_data
from all_functions import change_special_symbols
from all_functions import verbose
from all_functions import caching_parsed_data
from all_functions import read_cached_data
from all_functions import convert_to_fb2
from all_functions import get_image

version = "Version 1.0.2"

parser = argparse.ArgumentParser()
parser.add_argument("echo", nargs="?", default="https://news.yahoo.com/rss/", help="echo URL")
parser.add_argument("--version", action="store_true", help="Print version info")
parser.add_argument("--json", action="store_true", help="Print result as JSON in stdout")
parser.add_argument("--verbose", action="store_true", help="Outputs verbose status messages")
parser.add_argument("--limit", help="Limit news topics if this parameter provided")
parser.add_argument("--date", help="Check cached data")
parser.add_argument("--output-path", help="Set output directory")
parser.add_argument("--to-fb2", action="store_true", help="Convert to fb2")

args = parser.parse_args()
output_path = ""
output_path_json = "parsed_data.json"
output_path_fb2 = "rss.fb2"
if args.output_path:
    output_path = args.output_path
    output_path_json = args.output_path
    output_path_fb2 = output_path
    
limit = 0
if args.limit:
    limit = int(args.limit)
    
if args.date:
    verbose("reading cached data, date - " + args.date, args.verbose)
    if not output_path:
        print("Cached data: ")
    else:
        print("Cached data has been writen to {}".format(output_path))
    try:
        read_cached_data(str(args.date), output_path, limit)
        exit()
    except Exception:
        print("Error: there is no cached data")
        exit()

if args.version:
    print("Program version: {}".format(version))

verbose("requesting data from: " + args.echo, args.verbose)
response = None

try:
    response = urllib.request.urlopen(args.echo)
    verbose("url is opened, code: " + str(response.getcode()), args.verbose)
except Exception:
    print("url open error")
    exit()

verbose("reading data ", args.verbose)
rss_data = str(response.read())
draft_items = rss_data.split("<item>")
item_list = []
item_amount = len(draft_items)


verbose("parsing data ", args.verbose)
item = dict()
for i in range(item_amount):
    draft_items[i] = change_special_symbols(draft_items[i])
    item["title"] = get_item("title", draft_items[i])
    item["description"] = get_item("description", draft_items[i])
    if i:
        item["image"] = get_item("image", draft_items[i])
    item["link"] = get_item("link", draft_items[i])
    item["date"] = get_item("pubDate", draft_items[i])
    item_list.append(item)
    item = {}

parsed_data = dict()
parsed_data["feed"] = item_list[0]["description"]
parsed_data["items"] = item_list[1:]

caching_parsed_data(parsed_data)

if not args.limit:
    limit = len(parsed_data["items"])

if args.to_fb2:
    print("converting to fb2 to {}".format(output_path_fb2))
    convert_to_fb2(parsed_data, output_path_fb2, limit)

elif args.json:
    verbose("converting to json", args.verbose)
    with open(output_path_json, "w") as write_file:
        json.dump(parsed_data, write_file)

else:
    verbose("printing parsed data", args.verbose)
    print_parsed_data(parsed_data, output_path, limit)
    

