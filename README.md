# Hodgeys KJV DB
A SQLite database of the King James Bible, as compiled by me from [Project Gutenberg](https://www.gutenberg.org/files/10/10-h/10-h.htm); and an accompanying wrapper module, which I have [put up on PyPI](https://pypi.org/project/hodgeys-kjv-db/).

### Installation
```
pip install hodgeys-kjv-db
```

### Usage

```Python
# Import...
from hodgeys_kjv_db import KJV

# ...instantiate...
kjv = KJV()

# ...and drill down.
books = kjv.fetch_books()
for book in books:
    print(book)

chapters = kjv.fetch_chapters(1, 1)
for k, v in chapters.items():
    print(k, v)

verse = kjv.fetch_passage(1, 1, 1, 1)
print(verse)
```
