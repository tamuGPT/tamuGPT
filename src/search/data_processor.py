import re

import nltk

from bs4 import BeautifulSoup

from nltk.tokenize import word_tokenize

nltk.download('punkt')


def clean_html(html):
    soup = BeautifulSoup(html, 'html.parser')

    for script in soup(["script", "style"]):
        script.extract()

    text = soup.get_text()

    # Replace multiple whitespace characters with single space
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'\n', ' ', text)  # Replace newline characters with space
    # Replace multiple spaces with single space
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^\w\s]', '', text)  # Remove non-alphanumeric characters

    return text


def truncate_html_with_nltk(html_content, max_tokens=10000):
    tokens = word_tokenize(html_content)
    truncated_tokens = tokens[:max_tokens]
    truncated_html = ' '.join(truncated_tokens)
    return truncated_html
