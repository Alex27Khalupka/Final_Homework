import base64
import re
import json
import urllib.request


def verbose(_str, verb):
    if verb:
        print(_str)


def change_special_symbols(_str):
    _str = _str.replace("&amp;", "&")
    _str = _str.replace("&gt;", ">")
    _str = _str.replace("&lt;", "<")
    return _str


# getting URL of image from data
def get_image(data):
    description = re.search("<description>" + ".+" + "</description>", data).group()
    image = description.split("img src=")[1].split('"')
    return image[1]


# getting item(something between tags) from data.
def get_item(item, data):
    if item == "image":
        return get_image(data)

    open_item = "<" + item + ">"
    close_item = "</" + item + ">"
    tmp = re.search(open_item + ".+" + close_item, data).\
        group().\
        replace(open_item, "").\
        replace(close_item, "")

    return re.sub("<[^>]+>", "", tmp)


# printing parsed data to the console or to the file
def print_parsed_data(parsed_data, output_path):
    if not output_path:
        try:
            print("Feed: {}\n".format(parsed_data["feed"]))
        except Exception:
            print("Print error: nothing to print")
            pass
        for item in parsed_data["items"]:
            print("Title: {}".format(item["title"]))
            print("Description: {}".format(item["description"]))
            print("Image: {}".format(item["image"]))
            print("Link: {}".format(item["link"]))
            print("Date: {}".format(item["date"]))
            print("\n")
    else:
        with open(output_path, "w") as file:
            try:
                file.write("Feed: {}\n".format(parsed_data["feed"]))
            except Exception:
                print("Print error: nothing to print")
                pass
            for item in parsed_data["items"]:
                file.write("Title: {}\n".format(item["title"]))
                file.write("Description: {}\n".format(item["description"]))
                file.write("Image: {}\n".format(item["image"]))
                file.write("Link: {}\n".format(item["link"]))
                file.write("Date: {}\n".format(item["date"]))
                file.write("\n")


# converting date to format YYYYMMDD
def date_convert(date):
    date_split = date.split(" ")
    number = date_split[1]
    month = date_dct.get(date_split[2])
    year = date_split[3]
    return str(year + month + number)


# caching parsed data to json files by dates
# they will be placed in working directory
def caching_parsed_data(parsed_data):
    for item in parsed_data["items"]:
        date = date_convert(item["date"]) + ".json"
        try:
            with open(date, "r") as file:
                cached_data = json.loads(file.read())

            if item not in cached_data["items"]:
                cached_data["items"].append(item)

            with open(date, "w") as write_file:
                json.dump(cached_data, write_file)

        except Exception:
            dct_to_write = dict()
            dct_to_write["feed"] = parsed_data["feed"]
            dct_to_write["items"] = []
            dct_to_write["items"].append(item)

            with open(date, "w") as write_file:
                json.dump(dct_to_write, write_file)


def read_cached_data(date, output_path):
    date += ".json"
    try:
        with open(date, "r") as file:
            tmp = file.read()
            cached_data = json.loads(tmp)
    except Exception:
        return False
    print_parsed_data(cached_data, output_path)
    return True


# creating tags to convert to fb2 format
def create_tags(data, i):
    data_in_tags = "<section>"
    data_in_tags += '<title><p>' + data["title"] + "</p></title>"
    data_in_tags += '<p>' + data["description"] + "</p>"
    data_in_tags += '<p>Link: ' + data["link"] + "</p>"
    data_in_tags += '<p>Date: ' + data["date"] + "</p>"
    if data["image"]:
        data_in_tags += '<image l:href="#pic' + str(i) + '.jpg"/>'
    data_in_tags += "</section>"
    return data_in_tags


# converting to fb2 format
# creating constant tags
def convert_to_fb2(parsed_data, output_path):
    with open(output_path, "w") as file:
        begin = '<?xml version="1.0" encoding="windows-1251"?>' \
               '<FictionBook xmlns="http://www.gribuser.ru/xml/fictionbook/2.0" xmlns:l="http://www.w3.org/1999/xlink">'
        begin += '<body name ="Parsed news">'
        end = '</FictionBook>'
        file.write(begin)
        data_in_tags = ""
        image_list = list()
        i = 0
        for item in parsed_data["items"]:
            if item["image"]:
                image_list.append(urllib.request.urlopen(item["image"]).read())
                i += 1
            data_in_tags += create_tags(item, i)

        file.write(data_in_tags)
        file.write("</body>")
        for i in range(len(image_list)):
            file.write('<binary id="pic' + str(i) + '.jpg" content-type="image/jpeg">')
            file.write(str(base64.b64encode(image_list[i])).strip("b'"))
            file.write('</binary>')
            i += 1
        file.write(end)


# this dict is for converting date to YYYYMMDD format
date_dct = {"Jan": "01",
            "Feb": "02",
            "Mar": "03",
            "Apr": "04",
            "May": "05",
            "Jun": "06",
            "Jul": "07",
            "Aug": "08",
            "Sep": "09",
            "Oct": "10",
            "Nov": "11",
            "Dec": "12"}
