# One-shot command-line RSS reader

Version 1.0.1

## About project

Objective of the project is to create an utility that parses rss feed, caches parsed data and converts it to fb2 format.

## Getting started

### Installing

Clone this repository:
  `git clone https://github.com/Alex27Khalupka/Pyhon-Django-Project.git`

### Working with utility

To parse data from [https://news.yahoo.com/rss/](https://news.yahoo.com/rss/) use: `python3 main.py`


To parse data from any website use: `python3 main.py 'web_site_url'` (It may not work :) )


####Options

Print version
`--version`

Dump data to JSON
`--json`

Limit printed data
`--limit 42`

Display cached data for specific day
`--date "20191214"`

Covert to fb2
`--to-fb2`

Output path
`--output-path ./dir/file`

Options can work together


#### Data caching

Writing data to a database "date_database.sqlite3" (adding data to a table called "YYYYMMDD"(according to publication date)).