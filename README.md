# One-shot command-line RSS reader

Version 4.1.3

## Build

Update build tools before installation `python3 -m pip install --upgrade pip setuptools wheel`

Run from root folder `python setup.py sdist bdist_wheel`

##  Install 

After running build, run `python3.7 -m pip install --verbose --index-url https://test.pypi.org/simple/ --no-deps rss-reader-alex`

## Launch

Print all newsitems from RSS 

### From sources

`python3 main.py https://news.yahoo.com/rss`

### From python packages

`python3 main.py rss_reader https://news.yahoo.com/rss`

### From console

`rss-reader https://news.yahoo.com/rss`

Options

Print version
`--version`

Dump data to JSON
`--json`

Limit printed data
`--limit 42`

Display cached data for specific day
`--date 20191214`

Covert to fb2
`--to-fb2`

Output path
`--output-path ./dir/file`


## Data cache

Converting data to json format and writing it to YYYYMMDD.json.