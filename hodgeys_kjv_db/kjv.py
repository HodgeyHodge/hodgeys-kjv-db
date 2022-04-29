#! c:\[path to Python 2.5]\python.exe


import os
from contextlib import contextmanager
import sqlite3
from typing import NamedTuple
from enum import Enum

from .exceptions import *

class KJV:
    """
    Instantiate the wrapper.
    """

    def __init__(self, datapath=None):
        if datapath is None:
            this_file = os.path.abspath(os.path.dirname(__file__))
            self.datapath = os.path.join(this_file, 'DATA', 'Bible.db')
        else:
            self.datapath = datapath
    
    @contextmanager
    def db_cursor(self, factory=None):
        """
        A custom context manager, because `with sqlite3.connect(...)` does not call conn.close()!
        """
        con = sqlite3.connect(self.datapath)
        if factory:
            con.row_factory = factory
        cur = con.cursor()
        yield cur
        con.commit()
        con.close()

    def fetch_books(self):
        """
        Get every book, as a list of Book objects.
        """
        query = """
            SELECT
                b.TestamentID,
                b.BookID,
                b.ShortName,
                b.LongName,
                bs.NumChapters
            FROM
                Books b
            JOIN
                BookStats bs ON b.TestamentID = bs.TestamentID AND b.BookId = bs.BookId;
        """
        with self.db_cursor(sqlite3.Row) as cur:
            res = cur.execute(query)
            rows = res.fetchall()
        return [Book(*row) for row in rows]
    
    def fetch_chapters(self, testamentId: int, bookId: int):
        """
        Get a dict of chapter lengths for the given book.
        """
        query = f"""
            SELECT
                c.ChapterID,
                c.NumVerses
            FROM
                ChapterStats c
            WHERE
                c.TestamentID = {testamentId} AND
                c.BookID = {bookId}
        """
        with self.db_cursor(sqlite3.Row) as cur:
            res = cur.execute(query)
            rows = res.fetchall()
            if not rows:
                raise KJVIndexError(f"Can't retrieve information for testament {testamentId}, book {bookId}!")
            return {row[0]: row[1] for row in rows}

    def fetch_passage(self, testamentId: int, bookId: int, chapterId: int, verseId: int):
        """
        Get a Passage object, since some verses come pre-joined in compound passages.
        """
        query = f"""
            SELECT
                b.Index_,
                b.Passage1,
                b.Passage2
            FROM
                Bible b
            JOIN
                Books k ON b.TestamentID = k.TestamentID AND b.BookID = k.BookID
            WHERE
                b.TestamentID = {str(testamentId)} AND
                b.BookID = {str(bookId)} AND
                (
                    (
                        b.ChapterID = {str(chapterId)} AND
                        b.VerseID = {str(verseId)}
                    ) OR
                    (
                        b.IndexTypeID > 0 AND
                        b.ChapterID IN ({str(chapterId)}, {str(chapterId - 1)}) AND
                        (
                            b.Passage1 LIKE '% {str(chapterId)}:{str(verseId)} %' OR
                            b.Passage2 LIKE '%{str(chapterId)}:{str(verseId)} %'
                        )
                    )
                );
        """
        with self.db_cursor(sqlite3.Row) as cur:
            res = cur.execute(query)
            row = res.fetchone()
            if not row:
                raise KJVIndexError(f"Can't find {chapterId}:{verseId} in book {bookId} of testament {testamentId}!")
            return Passage(testamentId, bookId, *row)

class Book(NamedTuple):
    Testament: int
    Book: int
    ShortName: str
    LongName: str
    ChapterCount: int

class Passage(NamedTuple):
    Testament: int
    Book: int
    Attribution: str
    Passage1: str
    Passage2: str
