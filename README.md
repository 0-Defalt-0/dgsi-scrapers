# Rulings of Supreme Court of Justice Scraper

## Introduction

This Scrapy project is designed to scrape data from the [Supreme Court of Justice](http://www.dgsi.pt) website and store it in a SQLite database. It extracts information about legal rulings, including document contents, links, and dates.

## Setup

### Prerequisites

Before running the scraper, make sure you have the following installed:

- Python (3.7 or higher)
- Scrapy (`pip install scrapy`)
- SQLite (for storing scraped data)

### Configuration

1. **Clone the Repository**

    ```bash
    git clone https://github.com/yourusername/rulings_of_supreme_court_of_justice.git
    ```

2. **Navigate to the Project Directory**

    ```bash
    cd rulings_of_supreme_court_of_justice
    ```

3. **Install Dependencies**

    ```bash
    pip install -r requirements.txt
    ```

4. **Configure Database Connection**

    Open `pipeline.py` and modify the following line to specify your database connection details:

    ```python
    self.conn = sqlite3.connect('your_database_name.db')
    ```

## Usage

To run the scraper, execute the following command from the project directory:

```bash
scrapy crawl cases
```

This will initiate the scraping process. The scraped data will be stored in the SQLite database.

## Project Structure
 - rulings_of_supreme_court_of_justice/spiders/cases.py: Main spider file containing the scraping logic.
 - rulings_of_supreme_court_of_justice/items.py: Item class definition for storing scraped data.
 - rulings_of_supreme_court_of_justice/pipelines.py: Pipeline for processing and storing scraped items in the database.
 - rulings_of_supreme_court_of_justice/settings.py: Scrapy project settings, including middleware and pipeline configurations.

## Database Table
You can change the database name here is pipeline.py
```bash
self.conn = sqlite3.connect('YOUR_DB_NAME.db')
```
<br>

The database table structure is defined in pipeline.py. Modify the CREATE TABLE statement to match your requirements.
```bash
CREATE TABLE IF NOT EXISTS rulings (
    link TEXT PRIMARY KEY,
    date TEXT,
    document_contents TEXT
);
```
<br>
you can enable or disable database pipeline by commenting or uncommenting this code in settings.py file

```bash
ITEM_PIPELINES = {
    "rulings_of_supreme_court_of_justice.pipelines.RulingsOfSupremeCourtOfJusticePipeline": 300,
}
```
If you are just testing code you can disable the database pipeline by commenting the code above.
<br>

## Modify how certain fields get stored

in items.py file you can modify if a certain field you want to store as a list below we are adding Descritores: as a list other wise its stored as a text
```bash
if cleaned_key == 'Descritores:':
    cleaned_data[cleaned_key] = [clean_text(v) for v in value]
```

## Checking for New Data
Once you are done scraping the whole database and want to check for new data pls enable the code below in cases.py <br>
<br>
Its disabled as it checks for links on homepage and sees if they are in database if so it terminates the spider, if you enable the code before scraping the whole database it will stop as it would see that homepage links are already in database
```bash
homepage_links = response.xpath('(//table)[2]//font/a/@href').getall()
if check_links_in_database(homepage_links):
    raise CloseSpider("All links are in the database. Stopping execution.")
```
<br>
Once you enable it will check for new links on each page if there are new links it will be stored in database if none the spider will be terminated.
<br>
when you are done scraping database and want to enable this I suggest setting concurrent requests to 1 in settings.py so that it will follow linear requests which is safer to check new data as it will go page1, page2 etc.

```bash
# CONCURRENT_REQUESTS = 32
# set this to 1
CONCURRENT_REQUESTS = 1
```

<br>
<br>
you can test this script by disabling the pagination part in the cases.py

```bash
# Code for handling the pagination of the website
urls = response.xpath('(//tr)[108]//a//font/text()').getall()
for items in urls:
    if items == 'Seguinte':
        url = response.xpath(f'(//tr)[108]//a[{urls.index(items)+1}]/@href').get()
        absolute_url = f'http://www.dgsi.pt{url}'
        yield scrapy.Request(
            url= absolute_url,
            headers=self.HEADERS,
            callback=self.parse
        )
```
This way you can only store first 100 items of home page in the database and if there is new link on the homepage it will store it otherwise it will stop the spider

## Rate Limiting

You can modify this by going into settings.py file
<br>
By default concurrent requests is 16 if you want to modify this you can change CONCURRENT_REQUESTS
```bash
#CONCURRENT_REQUESTS = 32
CONCURRENT_REQUESTS = 1
```
Recommend to set it to 1 after you have finished scraping the whole website.
<br>
<br>

### Delaying Requests
I have enabled AUTOTHROTTLE_ENABLED = True in settings.py it automatically throttles the crawling speed based on the load of website you are crawling
```bash
AUTOTHROTTLE_ENABLED = True
```

# Setting Cron Jobs for Automatically running the spider
Since you are using linux you can set this up very easily
<br>
To check if you have any cron jobs you type
```bash
crontab -l
```
<br>
To set up the cron job, open the crontab file for editing:

```bash
crontab -e
```
<br>
Then add the cron expression with the full path to your Scrapy project and the command to run the spider:

```bash
0 2 * * * cd /path/to/myproject && scrapy crawl cases
```
Save the file, and the cron job will now run your Scrapy spider every day at 2 AM.
