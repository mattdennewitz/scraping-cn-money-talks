# Scraping art museum data with Scrapy

## Assumptions and requirements

- Python 3+
- Familiarity with Python virtual environments and `pipenv`
- Scrapy, a robust Python scraping framework

Python-specific execution demonstrated under "Usage" assumes an activated virtual environment.

## Setup

This project's setup routine should look familiar to anyone with Python experience:
clone the codebase, create a virtual environment, and install projects requirements.

### Terraforming the Python environment

To begin, clone this repository, and set up and activate a virtual environment

```
$ git clone git@github.com:mattdennewitz/scraping-cn-money-talks.git
$ cd scraping-cn-money-talks
$ python3 -m venv .    # or however you prefer to create
$ source bin/activate  # again, season to taste based on your environment
```

Then, install this project's requirements

```
$ pip install -r requirements.txt
```

## Usage

This project makes use of Scrapy, a community-blessed framework
for building data scrapers. Running Scrapy as directed here
will emit a CSV file per spider.

### Fetching Data

#### Running Scrapy

From the root of the repository, enter the project's code path

```
$ cd ondisplay
```

and execute the AIC crawler, `artic`, specifying output should be written to
a file named `artic.csv`.

```
$ scrapy crawl artic -o artic.csv
```

Scrapy will start and crawl `artic.edu` for Agnes Martin artworks,
writing its output to `./artic.csv`.
