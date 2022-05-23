#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ebook.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    import re
    from nltk import word_tokenize
    from nltk.stem import PorterStemmer

    def tokenize(data):
        data = re.sub("(<.*?>)", "", data)
        data = re.sub(r'http\S+', '', data)
        data = re.sub(r"(#[\d\w\.]+)", '', data)
        data = re.sub(r"(@[\d\w\.]+)", '', data)
        data = re.sub("(\\W|\\d)", " ", data)
        data = data.strip()
        data = word_tokenize(data)
        porter = PorterStemmer()
        stem_data = [porter.stem(word) for word in data]
        return stem_data
    main()
