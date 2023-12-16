import sqlite3
import json
from itemadapter import ItemAdapter

class RulingsOfSupremeCourtOfJusticePipeline:
    def __init__(self):

        # Also change name below in check_links_in_database
        self.conn = sqlite3.connect('test6.db')
        self.cursor = self.conn.cursor()

        # Create the table if it doesn't exist
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS rulings (
                link TEXT PRIMARY KEY,
                date TEXT,
                document_contents TEXT
            )
        ''')
        self.conn.commit()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        # Convert document_contents to a JSON string with UTF-8 encoding
        document_contents_json = json.dumps(adapter['document_contents'], ensure_ascii=False).encode('utf-8')

        # Check if the link already exists in the database
        link = adapter['link']
        query = "SELECT link FROM rulings WHERE link = ?;"
        self.cursor.execute(query, (link,))
        existing_link = self.cursor.fetchone()

        if not existing_link:
            # Insert link, date, and document_contents into the database
            self.cursor.execute('''
                INSERT INTO rulings (link, date, document_contents) VALUES (?, ?, ?)
            ''', (link, adapter['date'], document_contents_json))
            self.conn.commit()
        else:
            print(f"URL already present in the database: {link}")

        return item

    def close_spider(self, spider):
        self.conn.close()


def check_links_in_database(links):
    conn = sqlite3.connect('test6.db')
    cursor = conn.cursor()

    try:
        for link in links:
            # Ensure that the link starts with "http://www.dgsi.pt"
            if not link.startswith("http://www.dgsi.pt"):
                link = f"http://www.dgsi.pt{link}"

            query = "SELECT link FROM rulings WHERE link = ?;"
            cursor.execute(query, (link,))
            existing_link = cursor.fetchone()

            if not existing_link:
                print(f"URL not present in the database: {link}")
                return False

        print("All links are in the database.")
        return True

    finally:
        conn.close()
