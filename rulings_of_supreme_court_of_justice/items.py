import scrapy
import re
from itemloaders.processors import Compose, TakeFirst

def clean_text(text):
    # Replace various unwanted characters with spaces
    cleaned_text = re.sub(r'[\xa0]+', ' ', text)

    # Encode and decode to handle specific Unicode characters
    cleaned_text = cleaned_text.encode('utf-8', 'ignore').decode('utf-8')

    return cleaned_text.strip()

def clean_document_data(document_data_list):
    cleaned_data_list = []
    for document_data in document_data_list:
        cleaned_data = {}
        for key, value in document_data.items():
            cleaned_key = clean_text(key)
            if cleaned_key == 'Descritores:':
                # Don't join the list for this key
                cleaned_data[cleaned_key] = [clean_text(v) for v in value]
            elif isinstance(value, list):
                # Join the list items into a single text string for other keys
                cleaned_data[cleaned_key] = ' '.join([clean_text(v) for v in value])
            else:
                cleaned_data[cleaned_key] = clean_text(value)
        cleaned_data_list.append(cleaned_data)
    return cleaned_data_list

class RulingsOfSupremeCourtOfJusticeItem(scrapy.Item):
    document_contents = scrapy.Field(
        input_processor = Compose(clean_document_data)
    )
    link = scrapy.Field(
        output_processor = TakeFirst()
    )
    date = scrapy.Field(
        output_processor = TakeFirst()
    )