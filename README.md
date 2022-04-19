# Hodgeys KJV DB
A SQLite database (v3.35.5) of the King James Bible, as compiled by me from [Project Gutenberg](https://www.gutenberg.org/files/10/10-h/10-h.htm); and an accompanying wrapper module.

### Installation
```
pip install hodgeys-kjv-db
```

### Get started
How to do a thing:

```Python
from hodgeys_kjv_db import KJV

# Instantiate...
kjv = KJV()

# ...and drill down...
books = kjv.fetch_books()
for book in books:
    print(book)

chapters = kjv.fetch_chapters(1, 1)
for k, v in chapters.items():
    print(k, v)

verse = kjv.fetch_passage(1, 1, 1, 31)
print(verse)

# ...and don't forget how to count.
no_such_verse = kjv.fetch_passage(1, 1, 1, 32) #raises KJVIndexError
```