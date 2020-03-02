import base64
import re
import json
import urllib.request
import sqlite3


def verbose(_str, verb):
    if verb:
        print(_str)


def change_special_symbols(_str):
    _str = _str.replace("&amp;", "&")
    _str = _str.replace("&gt;", ">")
    _str = _str.replace("&lt;", "<")
    _str = _str.replace("&#39;", "`")
    _str = _str.replace("'", "`")
    _str = _str.replace('"', "`")
    return _str


# getting URL of image from data
def get_image(data):
    if "<description>" not in data:
        return ""
    description = re.search("<description>" + ".+" + "</description>", data).group()
    image = description.split("img src=")[1].split('`')[1].split("http")
    return "http" + image[2]


# getting item(something between tags) from data.
def get_item(item, data):
    if item == "image":
        return get_image(data)

    open_item = "<" + item + ">"
    close_item = "</" + item + ">"

    if open_item not in data:
        return ""

    tmp = re.search(open_item + ".+" + close_item, data).\
        group().\
        replace(open_item, "").\
        replace(close_item, "")

    return re.sub("<[^>]+>", "", tmp)


# printing parsed data to the console or to the file
def print_parsed_data(parsed_data, output_path, limit):
    print(limit)
    if not output_path:
        try:
            print("Feed: {}\n".format(parsed_data["feed"]))
        except Exception:
            print("Print error: nothing to print")
            pass
        for item in parsed_data["items"][:limit]:
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
            for item in parsed_data["items"][:limit]:
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


def caching_parsed_data(parsed_data):
    conn = sqlite3.connect('date_database.db')
    cursor = conn.cursor()
    for item in parsed_data["items"]:
        date = "'" + date_convert(item["date"]) + "'"
        cursor.execute("create table if not exists" + date + "(title varchar(255), description varchar(255), "
                                                             "image varchar(255), link varchar(255), "
                                                             "date varchar(255));")
        conn.commit()
        cursor.execute("select * from " + date + ";")
        cached_data = cursor.fetchall()
        title_list = list()
        for cached_items in cached_data:
            title_list.append(cached_items[0])
        
        if item["title"] not in title_list:
            cursor.execute("insert into " + date + "(title, description, image, link, date) values ('{}', '{}', "
                                                   "'{}', '{}', '{}');".format(item["title"],
                                                                               item["description"],
                                                                               item["image"],
                                                                               item["link"],
                                                                               item["date"]))

            conn.commit()
    conn.close()


def read_cached_data(date, output_path, limit):
    conn = sqlite3.connect('date_database.db')
    cursor = conn.cursor()
    date = "'" + date + "'"
    cursor.execute("select * from " + date)
    data = cursor.fetchall()
    cached_data = dict()
    cached_data["feed"] = ""
    cached_data["items"] = list()
    if not limit:
        limit = len(data)
    
    for item in data:
        dct_news = dict()
        dct_news["title"] = item[0]
        dct_news["description"] = item[1]
        dct_news["image"] = item[2]
        dct_news["link"] = item[3]
        dct_news["date"] = item[4]
        cached_data["items"].append(dct_news)
    print_parsed_data(cached_data, output_path, limit)


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
def convert_to_fb2(parsed_data, output_path, limit):
    with open(output_path, "w") as file:
        begin = '<?xml version="1.0" encoding="windows-1251"?>' \
               '<FictionBook xmlns="http://www.gribuser.ru/xml/fictionbook/2.0" xmlns:l="http://www.w3.org/1999/xlink">'
        begin += '<body name ="Parsed news">'
        end = '</FictionBook>'
        file.write(begin)
        data_in_tags = ""
        image_list = list()
        i = 0
        print("getting images")
        for item in parsed_data["items"][:limit]:
            if item["image"]:
                image_list.append(urllib.request.urlopen(item["image"]).read())
                i += 1
            data_in_tags += create_tags(item, i)

        file.write(data_in_tags)
        file.write("</body>")
        for i in range(len(image_list)):
            file.write('<binary id="pic' + str(i + 1) + '.jpg" content-type="image/jpeg">')
            file.write(str(base64.b64encode(image_list[i])).strip("b'"))
            file.write('</binary>')
        print("Data was successfully converted. Amount of news: {}".format(limit))
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
