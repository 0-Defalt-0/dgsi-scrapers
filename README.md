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
